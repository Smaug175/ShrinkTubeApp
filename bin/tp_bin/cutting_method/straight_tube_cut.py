import numpy as np
import streamlit as st
from bin.tp_bin.cutting_method.straight_tube import AxisSectionProcessor
import pandas as pd

def center_analyze_straight_tube(stl_file, file_type=None):
    # 使用文件对象并显式指定文件类型
    analyzer = AxisSectionProcessor(stl_file, file_type='stl')
    tube_radius_data = analyzer.get_Z_Radius_and_Tube_Radius()

    st.dataframe(tube_radius_data)

    #这里有问题，tube_radius_data没有得到数据

    # 获取管件参数
    st.session_state.tube_params = st.session_state.tp_shrink_tube_instance.get_tube_params_df()

    # 确保返回的是 DataFrame
    if isinstance(st.session_state.tube_params, pd.DataFrame):
        # 提取 T_D 和 D 的值
        T_D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'T_D', '值'].iloc[0]
        D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'D', '值'].iloc[0]

        # 计算周长
        T_D = float(T_D)
        D = float(D)
        T_D_perimeter = T_D * np.pi
        D_perimeter = D * np.pi

        # 查找对应的中心线长度
        def find_closest_length(perimeter, tube_radius_data):
            distances = np.abs(tube_radius_data['截面周长(mm)'] - perimeter)
            closest_index = np.argmin(distances)
            return tube_radius_data.iloc[closest_index]['中心线长度(mm)']

        T_D_length = find_closest_length(T_D_perimeter, tube_radius_data)
        D_length = find_closest_length(D_perimeter, tube_radius_data)

        # 提取在 T_D 和 D 对应的周长值之间的数据
        filtered_data = tube_radius_data[
            (tube_radius_data['截面周长(mm)'] >= min(T_D_perimeter, D_perimeter)) &
            (tube_radius_data['截面周长(mm)'] <= max(T_D_perimeter, D_perimeter))
            ]

        # 计算 filtered_data 中的直径
        filtered_data['直径(mm)'] = filtered_data['截面周长(mm)'] / np.pi

        # 创建一个新的 DataFrame 包含这些数据以及 T_D 和 D 对应的长度值
        result_data = pd.DataFrame({
            '中心线长度(mm)': [T_D_length, D_length],
            '直径(mm)': [T_D_perimeter / np.pi, D_perimeter / np.pi]
        }, index=['T_D', 'D'])

        result_data = pd.concat([result_data, filtered_data[['中心线长度(mm)', '直径(mm)']]], ignore_index=True)
        # 按照直径从小到大排序
        result_data = result_data.sort_values(by='直径(mm)', ascending=True).reset_index(drop=True)

        # 处理“中心线长度(mm)”列
        # 1. 每个值减去该列最小值
        min_center_length = result_data['中心线长度(mm)'].min()
        result_data['中心线长度(mm)'] = result_data['中心线长度(mm)'] - min_center_length

        # 2. 每个值加9
        result_data['中心线长度(mm)'] = result_data['中心线长度(mm)'] + 9

        # 颠倒dataframe的顺序
        result_data['直径(mm)'] = result_data['直径(mm)'][::-1].values
        result_data['中心线长度(mm)'] = result_data['中心线长度(mm)'][::-1].values

        # 修改表头
        result_data = result_data.rename(columns={'中心线长度(mm)': 'X', '直径(mm)': 'Y'})

        # >>>刘宇 开始增加代码：生成3D需要的参数。points
        # 后续要使用这个变量，不要重复命名。
        # points 应该是以(T_L+9,T_D/2)开始，以结束(9,T_d/2)的，我会根据给的点自动计算其中的值。
        st.session_state.tp_gen3d_points = result_data
        # 刘宇 结束增加代码<<<

        # 显示 T_D_length 和 D_length
        # st.divider()
        # st.write('#### 📏管件参数')
        # st.write(f"**TP抽起点长度(mm):** {D_length:.2f}")
        # st.write(f"**TP抽终点长度(mm):** {T_D_length:.2f}")
        # st.write('##### TP抽段形线坐标')
        # st.dataframe(result_data)
