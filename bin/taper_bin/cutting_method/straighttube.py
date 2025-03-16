import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from trimesh import load


class AxisSectionProcessor:
    def __init__(self, file_obj, file_type=None):
        # 加载模型
        if file_type:
            self.mesh = load(file_obj, file_type=file_type)
        else:
            self.mesh = load(file_obj)

        # 平移模型，使最小 Z 值为 0
        min_z = np.min(self.mesh.vertices[:, 2])
        self.mesh.apply_translation([0, 0, -min_z])

        # 获取中心线长度和截面周长数据
        self.Z_Radius, self.Tube_Radius = self.get_Z_Radius_and_Tube_Radius()

    def get_Z_Radius_and_Tube_Radius(self):
        # 切割间隔
        delta = 1
        # 存储 Z 轴高度和截面周长
        Z_ = []
        Perimeters = []
        centers = []

        # 获取模型的最小和最大 Z 值
        min_z = np.min(self.mesh.vertices[:, 2])
        max_z = np.max(self.mesh.vertices[:, 2])

        # 生成切割平面的 Z 值列表
        slide_list = np.linspace(min_z, max_z, int((max_z - min_z) / delta) + 1)

        # 获取中心线上的点
        self.cross_section_centers = self.get_cross_section_centers(slide_list)

        if len(self.cross_section_centers) < 2:
            print("Not enough points to calculate ConvexHull")
            return pd.DataFrame({'中心线长度(mm)': [], '截面周长(mm)': []})

        # 计算中心线长度
        center_positions = np.array(self.cross_section_centers)
        center_length = 0.0
        lengths = [0.0]

        for i in range(1, len(center_positions)):
            delta_length = np.linalg.norm(center_positions[i] - center_positions[i-1])
            center_length += delta_length
            lengths.append(center_length)

        centers = []
        perimeters = []

        # 计算每个截面的周长
        for z in slide_list:
            # 切割模型
            section = self.mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])

            if section is not None:
                intersection_points = section.vertices

                if len(intersection_points) >= 3:
                    # 计算凸包周长
                    try:
                        perimeter = self.calculate_convex_hull_perimeter(intersection_points)
                        perimeters.append(perimeter)
                    except Exception as e:
                        print(f"Failed to calculate ConvexHull at z={z}: {e}")
                        perimeters.append(0.0)
                else:
                    print(f"Not enough points at z={z}: {len(intersection_points)}")
                    perimeters.append(0.0)
            else:
                print(f"No intersection at z={z}")
                perimeters.append(0.0)

            centers.append(z)

        # 整理结果
        results = []
        for i in range(len(centers)):
            # 确保 center_lengths 和 perimeters 的索引对应
            if i < len(lengths) - 1:
                center_length_i = lengths[i]
            else:
                center_length_i = lengths[-1]

            if i < len(perimeters):
                perimeter_i = perimeters[i]
            else:
                perimeter_i = 0.0

            results.append((center_length_i, perimeter_i))

        # 转换为 DataFrame
        df = pd.DataFrame(results, columns=['中心线长度(mm)', '截面周长(mm)'])

        return df

    def get_cross_section_centers(self, slide_list):
        centers = []
        for z in slide_list:
            # 切割模型
            section = self.mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])

            if section is not None:
                intersection_points = section.vertices

                if len(intersection_points) >= 3:
                    # 计算截面的几何中心
                    center = np.mean(intersection_points, axis=0)
                    centers.append(center)
                else:
                    print(f"Not enough points at z={z} to compute center")
            else:
                print(f"No section at z={z}")
        return centers

    def calculate_convex_hull_perimeter(self, points):
        # 确保点集是二维的
        points_2d = points[:, :2]

        # 计算凸包
        hull = ConvexHull(points_2d, qhull_options='QJ')

        # 提取凸包顶点
        hull_points = points_2d[hull.vertices]

        # 按顺序计算周长
        perimeter = 0.0
        for i in range(len(hull_points)):
            point1 = hull_points[i]
            point2 = hull_points[(i + 1) % len(hull_points)]
            edge_length = np.linalg.norm(point1 - point2)
            perimeter += edge_length

        return perimeter

