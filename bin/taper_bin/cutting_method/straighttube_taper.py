import numpy as np
import streamlit as st
from bin.taper_bin.cutting_method.straighttube import AxisSectionProcessor
import pandas as pd

def center_analyze_straight_taper(stl_file, file_type=None):

    # 使用文件对象并显式指定文件类型
    analyzer = AxisSectionProcessor(stl_file, file_type='stl')
    tube_radius_data = analyzer.get_Z_Radius_and_Tube_Radius()

    st.dataframe(tube_radius_data)

    #这里有问题，tube_radius_data没有得到数据

    # 获取管件参数
    st.session_state.taper_instance.load_tube(st.session_state.dxf_file)
    st.session_state.tube_params = st.session_state.taper_instance.get_tube_params_df()

    # 确保返回的是 DataFrame
    if isinstance(st.session_state.tube_params, pd.DataFrame):
        # 提取 B_D 和 m_D 的值
        B_D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'B_D', '值'].iloc[0]
        m_D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'm_D', '值'].iloc[0]

        # 计算周长
        B_D = float(B_D)
        m_D = float(m_D)
        B_D_perimeter = B_D * np.pi
        m_D_perimeter = m_D * np.pi

        # 查找对应的中心线长度
        def find_closest_length(perimeter, tube_radius_data):
            distances = np.abs(tube_radius_data['截面周长(mm)'] - perimeter)
            closest_index = np.argmin(distances)
            return tube_radius_data.iloc[closest_index]['中心线长度(mm)']

        B_D_length = find_closest_length(B_D_perimeter, tube_radius_data)
        m_D_length = find_closest_length(m_D_perimeter, tube_radius_data)

        # 提取在 m_D 和 D 对应的周长值之间的数据
        filtered_data = tube_radius_data[
            (tube_radius_data['截面周长(mm)'] >= min(B_D_perimeter, m_D_perimeter)) &
            (tube_radius_data['截面周长(mm)'] <= max(B_D_perimeter, m_D_perimeter))
            ]

        # 计算 filtered_data 中的直径
        filtered_data.loc[:, '直径(mm)'] = filtered_data.loc[:, '截面周长(mm)'] / np.pi

        # 创建一个新的 DataFrame 包含这些数据以及 m_D 和 D 对应的长度值
        result_data = pd.DataFrame({
            '中心线长度(mm)': [B_D_length, m_D_length],
            '直径(mm)': [B_D_perimeter / np.pi, m_D_perimeter / np.pi]
        }, index=['B_D', 'D'])

        result_data = pd.concat([result_data, filtered_data[['中心线长度(mm)', '直径(mm)']]], ignore_index=True)
        # 按照直径从小到大排序
        result_data = result_data.sort_values(by='直径(mm)', ascending=False).reset_index(drop=True)

        # 处理“中心线长度(mm)”列
        # 1. 每个值减去该列最小值
        result_data['中心线长度(mm)'] = result_data['中心线长度(mm)'] - min(B_D_length, m_D_length)
        result_data = result_data[(result_data >= 0).all(axis=1)]
        result_data['中心线长度(mm)'] = (result_data['中心线长度(mm)'] - max(result_data['中心线长度(mm)'])).abs()

        # 判断中心线是否单调递增
        target_column = ['中心线长度(mm)']
        diff = result_data[target_column].diff().fillna(0)
        for index, row in diff.iterrows():
            if row[0] < 0:
                result_data.drop(index, inplace=True)
        result_data.drop([result_data.index[1], result_data.index[-2]], inplace=True)
        # print(result_data)

        # 修改表头
        result_data = result_data.rename(columns={'中心线长度(mm)': 'X', '直径(mm)': 'Y'})
        result_data = result_data.round({'X': 2, 'Y': 3})
        result_data = result_data.drop_duplicates(subset=['Y'])
        # np_radius = np.array(result_data)
        # sampled_data = np.linspace(0, len(np_radius) - 1, 15, dtype=int)  # 生成均匀分布的索引
        # print(sampled_data)
        # line = np_radius[sampled_data]
        # line = np.sort(line,axis=0)[::-1, :]
        # print(line)

        # 显示 m_D_length 和 D_length
        st.divider()
        st.write('#### 📏管件参数')
        # st.write(f"**Taper起点长度(mm):** {B_D_length:.2f}")
        # st.write(f"**Taper终点长度(mm):** {m_D_length:.2f}")
        st.write('##### Taper形线坐标')
        st.dataframe(result_data)

