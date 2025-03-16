import numpy as np
import streamlit as st
from bin.taper_bin.cutting_method.centerline import GetCenterLine
import pandas as pd

def center_analyze_taper(stl_file, file_type=None):

    if 'taper_stl_analyzed' in st.session_state and st.session_state.stl_analyzed and 'taper_analyzer_mesh' in st.session_state:
        # 从session_state中恢复数据
        if 'taper_tube_radius_data' in st.session_state:
            taper_tube_radius_data = st.session_state.taper_tube_radius_data
        else:
            # 如果没有保存数据，重新进行分析
            taper_analyzer = GetCenterLine(stl_file, file_type='stl')
            taper_tube_radius_data = taper_analyzer.get_Tube_Radius()
            # 保存分析数据和模型到session_state
            st.session_state.taper_tube_radius_data = taper_tube_radius_data
            st.session_state.taper_analyzer_mesh = taper_analyzer.mesh
    else:
        # 首次分析，执行完整流程
        # 使用文件对象并显式指定文件类型
        print(stl_file)
        taper_analyzer = GetCenterLine(stl_file, file_type='stl')
    # 使用文件对象并显式指定文件类型
    taper_analyzer = GetCenterLine(stl_file, file_type='stl')
    taper_tube_radius_data = taper_analyzer.get_Tube_Radius()


    # 保存分析数据和模型到session_state
    st.session_state.taper_tube_radius_data = taper_tube_radius_data
    st.session_state.taper_analyzer_mesh = taper_analyzer.mesh
    st.session_state.taper_stl_analyzed = True

    st.session_state.taper_tube_params = st.session_state.taper_instance.get_tube_params_df()


    # 确保返回的是 DataFrame
    if isinstance(st.session_state.taper_tube_params, pd.DataFrame):
        # 提取 B_D 和 m_D 的值
        B_D = st.session_state.taper_tube_params.loc[st.session_state.taper_tube_params['参数'] == 'B_D', '值'].iloc[0]
        m_D = st.session_state.taper_tube_params.loc[st.session_state.taper_tube_params['参数'] == 'm_D', '值'].iloc[0]

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

        B_D_length = find_closest_length(B_D_perimeter, taper_tube_radius_data)
        m_D_length = find_closest_length(m_D_perimeter, taper_tube_radius_data)

        # 提取在 m_D 和 D 对应的周长值之间的数据
        filtered_data = taper_tube_radius_data[
            (taper_tube_radius_data['截面周长(mm)'] >= min(B_D_perimeter, m_D_perimeter)) &
            (taper_tube_radius_data['截面周长(mm)'] <= max(B_D_perimeter, m_D_perimeter))
            ]

        # 计算 filtered_data 中的直径
        filtered_data.loc[:, '直径(mm)'] = filtered_data.loc[:, '截面周长(mm)'] / np.pi

        # 创建一个新的 DataFrame 包含这些数据以及 m_D 和 D 对应的长度值
        taper_result_data = pd.DataFrame({
            '中心线长度(mm)': [B_D_length, m_D_length],
            '直径(mm)': [B_D_perimeter / np.pi,m_D_perimeter / np.pi]
        }, index=['B_D', 'D'])

        taper_result_data = pd.concat([taper_result_data, filtered_data[['中心线长度(mm)', '直径(mm)']]], ignore_index=True)
        # 按照直径从小到大排序
        taper_result_data = taper_result_data.sort_values(by='直径(mm)', ascending=False).reset_index(drop=True)


        # 处理“中心线长度(mm)”列
        # 1. 每个值减去该列最小值
        taper_result_data['中心线长度(mm)'] = taper_result_data['中心线长度(mm)'] - min(B_D_length, m_D_length)
        taper_result_data = taper_result_data[(taper_result_data >= 0).all(axis=1)]
        taper_result_data['中心线长度(mm)'] = (taper_result_data['中心线长度(mm)']-max(taper_result_data['中心线长度(mm)'])).abs()


        # 判断中心线是否单调递增
        target_column =['中心线长度(mm)']
        diff = taper_result_data[target_column].diff().fillna(0)
        for index,row in diff.iterrows():
            if row[0] < 0:
                taper_result_data.drop(index, inplace=True)
        taper_result_data.drop([taper_result_data.index[1],taper_result_data.index[-2]], inplace=True)
        #print(result_data)

        # 修改表头
        taper_result_data = taper_result_data.rename(columns={'中心线长度(mm)': 'X', '直径(mm)': 'Y'})
        taper_result_data = taper_result_data.round({'X':2,'Y':3})
        taper_result_data = taper_result_data.drop_duplicates(subset=['Y'])
        #np_radius = np.array(result_data)
        # sampled_data = np.linspace(0, len(np_radius) - 1, 15, dtype=int)  # 生成均匀分布的索引
        # print(sampled_data)
        # line = np_radius[sampled_data]
        # line = np.sort(line,axis=0)[::-1, :]
        # print(line)

        # 显示 m_D_length 和 D_length
        # st.divider()
        # st.write('#### 📏管件参数')
        # #st.write(f"**Taper起点长度(mm):** {B_D_length:.2f}")
        # #st.write(f"**Taper终点长度(mm):** {m_D_length:.2f}")
        # st.write('##### Taper形线坐标')
        st.session_state.taper_result_data = taper_result_data
        st.session_state.m_D_length = m_D_length
        st.session_state.B_D_length = B_D_length

        # >>>刘宇 开始增加代码：生成3D需要的参数。points
        # 后续要使用这个变量，不要重复命名。
        # points 应该是以(T_L+9,T_D/2)开始，以结束(9,T_d/2)的，我会根据给的点自动计算其中的值。
        st.session_state.taper_gen3d_points = taper_result_data
    # 关闭文件
    if (not ('taper_stl_analyzed' in st.session_state and st.session_state.taper_stl_analyzed) and
            hasattr(taper_analyzer, 'mesh') and hasattr(taper_analyzer.mesh, 'file_obj')):
        taper_analyzer.mesh.file_obj.close()
