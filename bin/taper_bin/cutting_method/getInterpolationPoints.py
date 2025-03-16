import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb
from scipy.interpolate import interp1d
import pandas as pd
import streamlit as st

class GetInterpolationPoints:
    def __init__(self, file_obj, file_type=None):
        # 加载 XLS 文件
        if file_type:
            self.data = pd.read_excel(file_obj, usecols=[1, 2], names=["长度", "周长"])  # 读取手工测量的形线数据
        else:
            self.data = pd.read_excel(file_obj, usecols=[1, 2], names=["长度", "周长"])  # 读取手工测量的形线数据

        st.write("##### 手工测量数据")
        st.dataframe(self.data, use_container_width=True)  # 显示原始的手工测量的形线数据
        # 获取插值后的点
        interPointsList = self.InterPointPicture()
        # 插值后的数据
        data = pd.DataFrame(interPointsList, columns=["长度", "周长"])
        st.write("##### 插补计算后数据")
        st.dataframe(data, use_container_width=True)  # 显示插值后的形线数据

    # 三次样条插值
    @staticmethod
    def getInterpolationPoints(controlPoints, tList):
        n = len(controlPoints) - 1
        interPoints = []
        for t in tList:
            Bt = np.zeros(2, np.float64)
            for i in range(len(controlPoints)):
                # 确保 comb(n, i) 是标量
                comb_value = comb(n, i)
                # 确保 np.power(1 - t, n - i) 和 np.power(t, i) 是标量
                power_value = np.power(1 - t, n - i) * np.power(t, i)
                # 确保 controlPoints[i] 是一个二维数组的行，形状为 (2,)
                control_point = np.array(controlPoints[i])
                # 计算 Bt
                Bt += comb_value * power_value * control_point
            interPoints.append(list(Bt))
        return interPoints

    # 插值并绘制图片
    def InterPointPicture(self):
        controlPoints = self.data.values.tolist()  # 使用当前对象的数据
        controlPoints = np.array(controlPoints)
        n = len(controlPoints) - 1
        # 参数t的取值范围
        tList = np.linspace(0, 1, 1000)
        # 获取插值点
        interPointsList = self.getInterpolationPoints(controlPoints, tList)
        # 绘制曲线
        '''
        x1 = np.array(interPointsList)[:, 0]
        y1 = np.array(interPointsList)[:, 1]
        plt.plot(x1, y1, color='b')
        plt.scatter(controlPoints[:, 0], controlPoints[:, 1], color='r')
        plt.xlabel('长度')
        plt.ylabel('周长')
        plt.title('插值后的形线数据')
        st.pyplot(plt)  # 使用 streamlit 显示图像
        plt.close()  # 关闭图像以释放内存
        '''
        return interPointsList

    def comparePoints(self, readPoints, interPointsList):
        x1 = np.array(interPointsList)[:, 0]
        y1 = np.array(interPointsList)[:, 1]
        x2 = np.array(readPoints)[:, 0]
        y2 = np.array(readPoints)[:, 1]

        # 使用线性插值统一长度
        f1 = interp1d(x1, y1, kind='linear', fill_value="extrapolate")
        y1_resampled = f1(x2)
        f2 = interp1d(x2, y2, kind='linear', fill_value="extrapolate")
        y2_resampled = f2(x1)

        # 计算欧氏距离
        distance1 = np.linalg.norm(y1_resampled - y2)
        distance2 = np.linalg.norm(y1 - y2_resampled)

        # 可以取两者中的较小值或平均值作为最终的相似度度量,计算每个控制点的平均周长差,,需添加控制点最大可能的周长差！！！
        final_distance = min(distance1, distance2)
        final_avedistance = final_distance / max(len(y1_resampled), len(y2_resampled))
        print(f"Resampled Euclidean Distance: {final_avedistance}")
        return final_avedistance
