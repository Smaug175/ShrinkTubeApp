import numpy as np
import streamlit as st
from bin.tp_bin.cutting_method.center_line import GetCenterLine
import pandas as pd
import plotly.graph_objects as go
import tempfile
import os

def center_analyze_tube(stl_file, file_type=None):
    """对管件STL模型进行分析，提取中心线和半径信息"""
    # 判断是否已经分析过，如果分析过且保存了结果，则直接使用保存的数据显示
    if 'stl_analyzed' in st.session_state and st.session_state.stl_analyzed and 'analyzer_mesh' in st.session_state:
        # 从session_state中恢复数据
        if 'tube_radius_data' in st.session_state:
            tube_radius_data = st.session_state.tube_radius_data
        else:
            # 如果没有保存数据，重新进行分析
            analyzer = GetCenterLine(stl_file, file_type='stl')
            tube_radius_data = analyzer.get_Tube_Radius()
            # 保存分析数据和模型到session_state
            st.session_state.tube_radius_data = tube_radius_data
            st.session_state.analyzer_mesh = analyzer.mesh
    else:
        # 首次分析，执行完整流程
        # 使用文件对象并显式指定文件类型
        print(stl_file)
        analyzer = GetCenterLine(stl_file, file_type='stl')

        tube_radius_data = analyzer.get_Tube_Radius()
        # 保存分析数据和模型到session_state
        st.session_state.tube_radius_data = tube_radius_data
        st.session_state.analyzer_mesh = analyzer.mesh
        st.session_state.stl_analyzed = True

    st.session_state.tube_params = st.session_state.tp_shrink_tube_instance.get_tube_params_df()

    # 确保返回的是 DataFrame
    if isinstance(st.session_state.tube_params, pd.DataFrame):
        # 提取 T_D 和 D 的值
        T_D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'T_D', '值'].iloc[0]
        D = st.session_state.tube_params.loc[st.session_state.tube_params['参数'] == 'D', '值'].iloc[0]

        # 转换T_D为浮点数
        try:
            T_D = float(T_D)
        except (ValueError, TypeError):
            # 如果无法转换为浮点数，使用合理的默认值
            # print(f"警告: T_D参数值 '{T_D}' 无法转换为数字，将使用默认值")
            T_D = 10.0  # 设置一个默认值
            
        # 转换D为浮点数
        try:
            D = float(D)
        except (ValueError, TypeError):
            # 如果无法转换为浮点数，使用合理的默认值
            # print(f"警告: D参数值 '{D}' 无法转换为数字，将使用默认值")
            D = 8.0  # 设置一个默认值，通常D小于T_D
            
        # 现在可以安全地计算周长了
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
        filtered_data.loc[:, '直径(mm)'] = filtered_data.loc[:, '截面周长(mm)'] / np.pi

        # 创建一个新的 DataFrame 包含这些数据以及 T_D 和 D 对应的长度值
        result_data = pd.DataFrame({
            '中心线长度(mm)': [T_D_length, D_length],
            '直径(mm)': [T_D, D]
        }, index=['T_D', 'D'])

        result_data = pd.concat([result_data, filtered_data[['中心线长度(mm)', '直径(mm)']]], ignore_index=True)
        # 按照直径从小到大排序
        result_data = result_data.sort_values(by='直径(mm)', ascending=True).reset_index(drop=True)

        # 处理"中心线长度(mm)"列
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

        # 保存结果数据到session_state，以便页面刷新后恢复
        st.session_state.result_data = result_data
        st.session_state.T_D_length = T_D_length
        st.session_state.D_length = D_length

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

    # 关闭文件，但不在全新分析时关闭
    if not ('stl_analyzed' in st.session_state and st.session_state.stl_analyzed) and hasattr(analyzer, 'mesh') and hasattr(analyzer.mesh, 'file_obj'):
        analyzer.mesh.file_obj.close()

# def display_stl_model(mesh):
#     """使用Plotly在Streamlit中显示STL模型"""
#     # 使用session_state检查3D模型是否已经显示过
#     if 'stl_model_displayed' not in st.session_state:
#         st.session_state.stl_model_displayed = False
#
#     st.write('### 3D模型预览')
#     st.write('旋转优化后的管件模型：')
#
#     # 创建plotly图形
#     fig = go.Figure()
#
#     # 获取mesh的顶点和面
#     vertices = mesh.vertices
#     faces = mesh.faces
#
#     # 有时候faces可能是2维的，需要确保它是正确的3D面
#     if faces.shape[1] != 3:
#         st.warning("无法正确显示模型，面数据格式不正确")
#         return
#
#     # 添加3D mesh，使用单一颜色
#     fig.add_trace(go.Mesh3d(
#         x=vertices[:, 0],
#         y=vertices[:, 1],
#         z=vertices[:, 2],
#         i=faces[:, 0],
#         j=faces[:, 1],
#         k=faces[:, 2],
#         color='lightblue',  # 使用单一颜色
#         opacity=0.8,
#     ))
#
#     # 设置图形布局
#     fig.update_layout(
#         scene=dict(
#             aspectmode='data',
#             xaxis=dict(title='X轴'),
#             yaxis=dict(title='Y轴'),
#             zaxis=dict(title='Z轴')
#         ),
#         margin=dict(l=0, r=0, b=0, t=30),
#         scene_camera=dict(
#             eye=dict(x=1.5, y=1.5, z=1.5)
#         )
#     )
#
#     # 在Streamlit中显示图形并设置标志
#     st.plotly_chart(fig, use_container_width=True)
#     st.session_state.stl_model_displayed = True