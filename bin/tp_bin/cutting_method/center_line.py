import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.interpolate import splprep, splev
from trimesh import load, Trimesh, Scene
from trimesh.convex import ConvexHull as TrimeshConvexHull
from trimesh.transformations import rotation_matrix, translation_matrix
import trimesh

class GetCenterLine:
    def __init__(self, file_obj, file_type=None):

        if file_type:
            self.mesh = trimesh.load(file_obj, file_type=file_type)
        else:
            self.mesh = trimesh.load(file_obj)

        # 通过分析模型在三个主轴方向上的尺寸来判断管子的方向
        # 计算模型在x、y、z三个方向上的长度
        try:
            x_min, y_min, z_min = np.min(self.mesh.vertices, axis=0)
            x_max, y_max, z_max = np.max(self.mesh.vertices, axis=0)
            x_length = x_max - x_min
            y_length = y_max - y_min
            z_length = z_max - z_min
        except:
            self.success = False
            return

        # 确定哪个方向是管子的主轴（应该最长）
        lengths = [x_length, y_length, z_length]
        main_axis = np.argmax(lengths)

        # 如果z轴不是主轴，需要旋转模型使z轴成为管子的中心轴
        if main_axis == 0:  # x轴是最长的
            # 将x轴旋转至z轴（绕y轴旋转-90度）
            self.mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-90), [0, 1, 0]))
        elif main_axis == 1:  # y轴是最长的
            # 将y轴旋转至z轴（绕x轴旋转90度）
            self.mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]))
        
        # 再次计算旋转后的尺寸，确保x和y方向的长度差异不大
        x_min, y_min, z_min = np.min(self.mesh.vertices, axis=0)
        x_max, y_max, z_max = np.max(self.mesh.vertices, axis=0)
        x_length = x_max - x_min
        y_length = y_max - y_min
        
        # 如果x和y长度差异较大，可能需要围绕z轴旋转来使横截面更均匀
        if x_length / y_length > 1.5 or y_length / x_length > 1.5:
            # 绕z轴旋转45度，使横截面更接近正圆
            self.mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(45), [0, 0, 1]))

        # Translate model to make the minimum Z value 0
        min_z = np.min(self.mesh.vertices[:, 2])
        self.mesh.vertices[:, 2] -= min_z

        # Get Z_Radius data
        self.Z_Radius = self.get_Z_Radius()

        # Get Tube_Radius data
        self.Tube_Radius = self.get_Tube_Radius()

        self.success = True



    def get_Z_Radius(self):
        # First cut to find the center of each cross-section
        delta = 1
        Z_, Centers = [], []

        min_z = np.min(self.mesh.vertices[:, 2])
        max_z = np.max(self.mesh.vertices[:, 2])

        slide_list = np.linspace(min_z, max_z, int((max_z - min_z) / delta) + 1)

        for z in slide_list:
            section = self.mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])

            if section is not None:
                intersection_points = section.vertices

                if len(intersection_points) >= 3:
                    try:
                        hull = ConvexHull(intersection_points, qhull_options='QJ')
                        Z_.append(z)
                        center = np.mean(intersection_points[hull.vertices], axis=0)
                        Centers.append(center)
                    except Exception as e:
                        print(f"z={z} ConvexHull calculation failed: {e}")
                else:
                    print(f"z={z} has less than 3 intersection points, skipping")
            else:
                print(f"z={z} section is empty, skipping")

        if len(Z_) == 0:
            print("Not enough points to calculate ConvexHull")
            return pd.DataFrame({'Z轴高度(mm)': []})

        z_max, z_min = np.max(Z_), np.min(Z_)
        Z = [z - z_min for z in Z_]

        # 存储几何中心坐标
        self.cross_section_centers = Centers

        # 曲线拟合
        tck, u = splprep([np.array(Centers)[:, 0], np.array(Centers)[:, 1], np.array(Centers)[:, 2]], s=8e6, k=3)
        u_fine = np.linspace(0, 1, num=300)
        x_fine, y_fine, z_fine = splev(u_fine, tck)

        # 更新中心点
        new_centers = []
        for z in Z_:
            # 找到最接近 z 的拟合点
            distances = np.abs(z_fine - z)
            closest_index = np.argmin(distances)
            new_center = [x_fine[closest_index], y_fine[closest_index], z]
            new_centers.append(new_center)

        self.cross_section_centers = new_centers

        return pd.DataFrame({'长度(mm)': Z})

    def get_Tube_Radius(self):
        if not hasattr(self, 'cross_section_centers') or len(self.cross_section_centers) < 10:
            print("Not enough points to calculate ConvexHull")
            return pd.DataFrame({'中心线长度(mm)': [], '截面周长(mm)': []})

        centers = np.array(self.cross_section_centers)
        lengths = []
        Perimeters = []

        for i in range(1, len(centers)):
            length = np.linalg.norm(centers[i] - centers[i - 1])
            lengths.append(lengths[-1] + length if lengths else length)

        for i in range(len(centers) - 1):
            point1 = centers[i]
            point2 = centers[i + 1]
            direction = point2 - point1
            direction = direction / np.linalg.norm(direction)
            normal = direction

            clipped = self.mesh.section(plane_origin=point2, plane_normal=normal)

            if clipped is not None:
                intersection_points = clipped.vertices
                if len(intersection_points) >= 3:
                    try:
                        local_points = self.get_local_2d_coordinates(intersection_points, normal, point2)
                        perimeter = self.calculate_2d_convex_hull_perimeter(local_points)
                        Perimeters.append(perimeter)
                    except Exception as e:
                        print(f"Plane {i} ConvexHull calculation failed: {e}")
                else:
                    print(f"Plane {i} has less than 3 intersection points, skipping")
            else:
                print(f"Plane {i} does not intersect with the model")

        '''
        # 舍去前10个和最后10个数据点
        start_idx = 10
        end_idx = -10 if len(lengths) > 20 else len(lengths)
        lengths = lengths[start_idx:end_idx]
        Perimeters = Perimeters[start_idx:end_idx]
        '''

        return pd.DataFrame({'中心线长度(mm)': lengths, '截面周长(mm)': Perimeters})

    def calculate_2d_convex_hull_perimeter(self, points):
        if len(points) < 3:
            return 0
        hull = ConvexHull(points)
        perimeter = 0
        for simplex in hull.simplices:
            point1 = hull.points[simplex[0]]
            point2 = hull.points[simplex[1]]
            edge_length = np.linalg.norm(point1 - point2)
            perimeter += edge_length
        return perimeter

    def get_local_2d_coordinates(self, points, normal, origin):
        if abs(normal[0]) < abs(normal[1]) and abs(normal[0]) < abs(normal[2]):
            v1 = np.array([1, 0, 0])
        elif abs(normal[1]) < abs(normal[2]):
            v1 = np.array([0, 1, 0])
        else:
            v1 = np.array([0, 0, 1])

        v1 = v1 - np.dot(v1, normal) * normal
        v1 = v1 / np.linalg.norm(v1)

        v2 = np.cross(normal, v1)
        v2 = v2 / np.linalg.norm(v2)

        local_points = []
        for point in points:
            vec = point - origin
            x = np.dot(vec, v1)
            y = np.dot(vec, v2)
            local_points.append([x, y])

        return np.array(local_points)