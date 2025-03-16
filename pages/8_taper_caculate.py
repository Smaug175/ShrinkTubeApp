import streamlit as st
from menu import menu_with_redirect
import tempfile
from bin.taper_bin.Taper import TaperClass,Taper_Mold
from bin.taper_bin.cutting_method.centerline_taper import center_analyze_taper
from bin.taper_bin.cutting_method.straighttube_taper import center_analyze_straight_taper
from bin.taper_bin.cutting_method.getInterpolationPoints import GetInterpolationPoints
import plotly.graph_objects as go
import time
import os


def display_stl_model(mesh):
    """使用Plotly在Streamlit中显示STL模型"""
    # 使用session_state检查3D模型是否已经显示过
    if 'taper_stl_model_displayed' not in st.session_state:
        st.session_state.taper_stl_model_displayed = False

    # 创建plotly图形
    fig = go.Figure()

    # 获取mesh的顶点和面
    vertices = mesh.vertices
    faces = mesh.faces

    # 有时候faces可能是2维的，需要确保它是正确的3D面
    if faces.shape[1] != 3:
        st.warning("无法正确显示模型，面数据格式不正确")
        return

    # 添加3D mesh，使用单一颜色
    fig.add_trace(go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color='lightblue',  # 使用单一颜色
        opacity=0.8,
    ))

    # 设置图形布局
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            xaxis=dict(title='X轴'),
            yaxis=dict(title='Y轴'),
            zaxis=dict(title='Z轴')
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        scene_camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )

    # 在Streamlit中显示图形并设置标志
    st.plotly_chart(fig, use_container_width=True)
    st.session_state.taper_stl_model_displayed = True

# 显示侧边
menu_with_redirect()

@st.fragment
def header():
    st.title("Taper模具自动设计")
    st.divider()


@st.fragment
def reload_page():
    if st.button("重新加载",
                 disabled=not st.session_state.taper_file_loaded,
                 use_container_width=True,
                 type="primary"):
        del st.session_state.taper_instance
        st.empty()
        st.rerun()


@st.cache_data
def read_dxf_file(uploaded_dxf_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_dxf_file.read())
        tmp_file.flush()
    return tmp_file.name

@st.cache_data
def read_stl_file(uploaded_stl_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_stl_file.read())
        tmp_file.flush()
    return tmp_file.name




@st.fragment
def show_tube_params():
    st.divider()
    st.write('#### 📏管件参数')
    st.dataframe(
        st.session_state.taper_tube_params,
        use_container_width=True,
        hide_index=True,
    )


def get_setting():
    st.divider()  # 确保这里正确使用了 st.divider()
    st.write('#### 🛠️参数设定')
    # 初始化 session_state
    if 'taper_calculated' not in st.session_state:
        st.session_state.taper_calculated = False


    machine_type = st.selectbox(
        "请选择管件加工的机床型号：",
        ("EC0120", "EC0121"),
        disabled=st.session_state.taper_calculated
    )



    mold_list = st.multiselect(
        "请选择需要制作的模具：",
        Taper_Mold[machine_type],
        default=Taper_Mold[machine_type],
        disabled=st.session_state.taper_calculated
    )

    # 添加tp抽形线长度的输入框
    tp_length = st.number_input(
        "输入用于过渡的tp抽形线长度：",
        value=25,  # 默认值为 25
        help="默认长度25"
    )

    settings = {
        'machine_type': machine_type,
        'tp_length':tp_length,
        'mold_list': mold_list
    }
    return settings


@st.fragment
def calculate(settings,line_data):
    st.session_state.taper_instance.calculate(
        user_name= st.session_state.user_name,
        machine_type=settings['machine_type'],
        mold_list=settings['mold_list'],
        tp_length=settings['tp_length'],
        line_data=line_data
    )
@st.fragment
def show_calculate_results():
    st.divider()
    st.write("### 📋计算结果")
    calculate_results = st.session_state.taper_instance.get_molds_params_df()

    names = list(calculate_results.keys())

    tabs_list = st.tabs(names)
    for i in range(len(tabs_list)):
        tab = tabs_list[i]
        with tab:
            edited_data = st.data_editor(calculate_results[names[i]],
                                         use_container_width=True,
                                         hide_index=True,
                                         column_config={
                                             "参数": st.column_config.TextColumn("参数", disabled=True),
                                             "描述": st.column_config.TextColumn("描述", disabled=True),
                                             "计算方法": st.column_config.TextColumn("计算方法", disabled=True),
                                         })
            calculate_results[names[i]] = edited_data  # 更新数据
            mold_name = names[i]
            keys = list(calculate_results[names[i]]['参数'])
            values = list(calculate_results[names[i]]['值'])
            # print(mold_name, keys, values)
            for i in range(len(keys)):
                st.session_state.taper_instance.modify_parameters(mold_name, keys[i], values[i])


@st.fragment
def save_params_and_files():
    st.session_state.taper_instance.save_all()
    out_root = 'local_cache'
    st.session_state.taper_zip_file_path = st.session_state.taper_instance.output_zip_from_cache(out_root)


# 检查 DXF 文件是否已上传
if 'taper_instance' not in st.session_state:
    st.session_state.taper_instance = TaperClass(None)  # 重新加载
    st.session_state.taper_file_loaded = False
    st.session_state.taper_stl_file_loading = False

    st.session_state.taper_choose_loading_method = False
    st.session_state.taper_get_3d_points = False

    st.session_state.taper_params_setted = False
    st.session_state.taper_uploaded_stl_file = None
    st.session_state.taper_stl_file_loaded = False
    st.session_state.taper_calculated = False
    st.session_state.taper_saved = False
    st.session_state.taper_outputed = False

# DXF 文件上传模块
if not st.session_state.taper_file_loaded:
    header()
    st.write("### 📄导入DXF文件")
    st.session_state.taper_uploaded_dxf_file = st.file_uploader('上传按照要求制作的 dxf 文件：',
                                                          type='dxf',
                                                          accept_multiple_files=False,
                                                          key=None,
                                                          help=None,
                                                          disabled=st.session_state.taper_file_loaded,
                                                          label_visibility="visible",
                                                          )
else:
    header()
    if st.session_state.taper_uploaded_dxf_file:
        st.write('## 👍加载成功：' + st.session_state.taper_uploaded_dxf_file.name)
        reload_page()
    else:
        st.write('## 👎加载失败，请重新上传！')
        reload_page()

if not st.session_state.taper_file_loaded:
    if st.session_state.taper_uploaded_dxf_file:
        st.session_state.taper_dxf_file = read_dxf_file(st.session_state.taper_uploaded_dxf_file)
        st.session_state.taper_file_loaded = True
        # 获取管件参数
        st.session_state.taper_instance.load_tube(st.session_state.taper_dxf_file)
        st.session_state.taper_tube_params = st.session_state.taper_instance.get_tube_params_df()  # 确保返回的是 DataFrame
        st.rerun()
else:
    show_tube_params()
    if not st.session_state.taper_choose_loading_method:
        if st.button("选择加载型线的方式", disabled=st.session_state.taper_choose_loading_method, use_container_width=True, type="primary"):
            st.session_state.taper_choose_loading_method = True
            st.rerun()

# 选择加载 stl 文件的方式
if st.session_state.taper_choose_loading_method:
    if not st.session_state.taper_get_3d_points:
        # 对后面的步骤进行截断
        st.session_state.taper_params_setted = False
        st.session_state.taper_analyzer_mesh = None
        #

        st.divider()
        st.write("### 📄选择加载型线的方式")
        taper_caculate_method = st.selectbox(
            "请选择加载型线的方式：",
            ['使用三维模型计算（STL模型）：使用原始成品管件', '使用三维模型计算（STL模型）：使用重绘后的直管',
             '使用手工测量值计算（使用XLS数值表）'],
            disabled=False,
        )
        if taper_caculate_method == '使用三维模型计算（STL模型）：使用原始成品管件' or taper_caculate_method == '使用三维模型计算（STL模型）：使用重绘后的直管':
            st.write("#### 📄导入STL文件")
            taper_uploaded_stl_file = st.file_uploader('上传 STL 文件：',
                                                 type='stl',
                                                 accept_multiple_files=False,
                                                 key="stl_file_uploader",
                                                 help=None,
                                                 disabled=st.session_state.taper_get_3d_points,
                                                 label_visibility="visible",
                                                 )
            if taper_uploaded_stl_file:  # 文件成功上传，需要进一步计算
                st.session_state.taper_uploaded_stl_file = taper_uploaded_stl_file
                st.write('#### 👍加载成功：' + st.session_state.taper_uploaded_stl_file.name)

                # 计算型线
                progress_text = "正在分析STL模型..."
                progress_bar = st.progress(0, text=progress_text)
                st.session_state.taper_stl_file_temp = read_stl_file(st.session_state.taper_uploaded_stl_file)

                progress_bar.progress(25, text="正在读取STL文件...")

                # 更新进度条到50%
                progress_bar.progress(50, text="正在计算管件中心线...")
                # 根据STL类型调用相应的分析函数
                progress_bar.progress(75, text="正在分析管件形状...")
                if taper_caculate_method == '使用三维模型计算（STL模型）：使用原始成品管件':
                    center_analyze_taper(st.session_state.taper_stl_file_temp, file_type='stl')
                elif taper_caculate_method == '使用三维模型计算（STL模型）：使用重绘后的直管':
                    center_analyze_straight_taper(st.session_state.taper_stl_file_temp, file_type='stl')

                # 完成进度条
                progress_bar.progress(100, text="分析完成！")
                time.sleep(0.5)  # 短暂显示完成状态
                progress_bar.empty()  # 清除进度条

                st.session_state.taper_get_3d_points = True
                st.rerun()
            else:
                pass

        elif taper_caculate_method == '使用手工测量值计算（使用XLS数值表）':
            st.write("#### 📄导入XLS文件")
            taper_uploaded_xls_file = st.file_uploader('上传包含手工测量值的 xls 文件：',
                                                 type='xls',
                                                 accept_multiple_files=False,
                                                 key=None,
                                                 help=None,
                                                 label_visibility="visible",
                                                 )
            if taper_uploaded_xls_file is not None:
                st.session_state.xls_file = taper_uploaded_xls_file
                st.write('### 👍XLS 文件加载成功：' + taper_uploaded_xls_file.name)
                # 调用 GetInterpolationPoints 类
                interpolation_processor = GetInterpolationPoints(taper_uploaded_xls_file)
                st.session_state.taper_get_3d_points = True

if st.session_state.taper_choose_loading_method and st.session_state.taper_get_3d_points:
    st.divider()
    st.write("### 📄成功加载型线")
    st.write('#### 👍加载成功：' + st.session_state.taper_uploaded_stl_file.name)
    # 重新加载模型
    if st.button("重新加载型线文件",
                 disabled=False,
                 use_container_width=True,
                 key='reload-stl-excel',
                 type="primary"):
        st.session_state.taper_get_3d_points = False
        st.rerun()

    # 查看型线
    try:
        st.write('#### 3D模型预览')
        st.write('旋转优化后的管件模型：')
        display_stl_model(st.session_state.taper_analyzer_mesh)
    except:
        st.write('#### 3D模型预览')
        st.write('所选方法暂时无法预览3D模型！')

    if hasattr(st.session_state, 'taper_result_data') and hasattr(st.session_state, 'B_D_length') and hasattr(
            st.session_state, 'm_D_length'):
        st.divider()
        st.write('#### 📏型线参数')
        st.write(f"**Taper起点长度(mm):** {st.session_state.m_D_length:.2f}")
        st.write(f"**Taper终点长度(mm):** {st.session_state.B_D_length:.2f}")
        st.write('##### Taper段形线坐标')
        st.dataframe(st.session_state.taper_result_data)
        st.session_state.line_data = st.session_state.taper_result_data

    if not st.session_state.taper_params_setted:
        if st.button("计算模具参数设定", disabled=st.session_state.taper_params_setted, use_container_width=True, type="primary",):
            st.session_state.taper_params_setted = True
            st.rerun()


if st.session_state.taper_params_setted:
    settings = get_setting()
    if settings['mold_list'] != []:
        if not st.session_state.taper_calculated:
            if st.button("计算", on_click=calculate, disabled=st.session_state.taper_calculated, use_container_width=True,
                         type="primary",
                         args=(settings,st.session_state.line_data,)):
                st.session_state.taper_calculated = True
                st.rerun()
    else:
        st.write("⚠️请选择需要计算的模具！")

if st.session_state.taper_calculated:
    if not st.session_state.taper_saved:
        if st.button("重新选择", disabled=st.session_state.taper_saved,
                     use_container_width=True,
                     type="primary"):
            st.session_state.taper_calculated = False
            st.rerun()
        show_calculate_results()
        if st.button("保存", on_click=save_params_and_files, disabled=st.session_state.taper_saved,
                     use_container_width=True,
                     type="primary"):
            st.session_state.taper_saved = True
            st.rerun()
    else:
        show_calculate_results()
        st.divider()
        st.write('### 🎉保存成功！')

if st.session_state.taper_saved:
    if not st.session_state.taper_outputed:
        with open(st.session_state.taper_zip_file_path, "rb") as file:
            btn = st.download_button(
                label="下载计算结果",
                data=file,
                file_name=st.session_state.taper_zip_file_path,
                mime="application/zip",
                disabled=st.session_state.taper_outputed,
                type="primary",
                key=None,
                use_container_width=True,
            )
            if btn:
                st.session_state.taper_outputed = True
                st.rerun()
    else:
        st.divider()
        st.write('### 🎉下载成功！')
