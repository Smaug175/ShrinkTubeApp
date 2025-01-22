import streamlit as st
from menu import menu_with_redirect
import tempfile
from tools.normal import logger, MOLDS
from bin.ShrinkTube import ShrinkTubeClass

# 显示侧边
menu_with_redirect()

@st.fragment
def header():
    st.title("普通抽模具自动设计")
    st.divider()

@st.fragment
def reload_page():
    if st.button("重新加载", disabled=not st.session_state.file_loaded, use_container_width=True, type="primary"):
        del st.session_state.shrink_tube_instance
        st.empty()
        st.rerun()

@st.cache_data
def read_dxf_file(uploaded_dxf_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_dxf_file.read())
        tmp_file.flush()
    return tmp_file.name

@st.fragment
def show_tube_params():
    st.divider()
    st.write('#### 📏管件参数')
    st.dataframe(
        st.session_state.tube_params,
        use_container_width=True,
        hide_index=True,
    )

def get_setting():
    st.divider()
    st.write('#### 🛠️参数设定')
    forming = st.toggle("额外壁厚",
                        value = True,
                        disabled=st.session_state.caculated )

    machine_type = st.selectbox(
        "请选择管件加工的机床型号：",
        ("DC0124", "DC0121", "DC0125"),
        disabled=st.session_state.caculated ,
    )

    mold_list = st.multiselect(
        "请选择需要制作的模具：",
        MOLDS[machine_type + (' forming' if forming else '')],
        default=MOLDS[machine_type + (' forming' if forming else '')],
        disabled=st.session_state.caculated ,
    )

    settings = {
        'forming': forming,
        'machine_type': machine_type,
        'mold_list': mold_list
    }
    return settings

@st.fragment
def calculate(settings):
    user_name = st.session_state.user_name
    forming = settings['forming']
    machine_type = settings['machine_type']
    mold_list = settings['mold_list']
    st.session_state.shrink_tube_instance.calculate(user_name, forming, mold_list, machine_type)

import pandas as pd

@st.fragment
def show_caculate_results():
    st.divider()
    st.write("### 📋计算结果")
    caculate_results = st.session_state.shrink_tube_instance.get_molds_params_df()

    names = list(caculate_results.keys())

    tabs_list = st.tabs(names)
    for i in range(len(tabs_list)):
        tab = tabs_list[i]
        with tab:
            edited_data = st.data_editor(caculate_results[names[i]],
                           use_container_width=True,
                           hide_index=True,
                           column_config={
                               "参数": st.column_config.TextColumn("参数", disabled=True),
                               "描述": st.column_config.TextColumn("描述", disabled=True),
                               "计算方法": st.column_config.TextColumn("计算方法", disabled=True),
                           })
            caculate_results[names[i]] = edited_data # 更新数据
            mold_name = names[i]
            keys = list(caculate_results[names[i]]['参数'])
            values = list(caculate_results[names[i]]['值'])
            # print(mold_name, keys, values)
            for i in range(len(keys)):
                st.session_state.shrink_tube_instance.modify_parameters(mold_name, keys[i], values[i])


@st.fragment
def save_params_and_files():
    st.session_state.shrink_tube_instance.save_all()
    out_root = 'local_cache'
    st.session_state.zip_file_path = st.session_state.shrink_tube_instance.output_zip_from_cache(out_root)



if 'shrink_tube_instance' not in st.session_state:
    st.session_state.shrink_tube_instance = ShrinkTubeClass(logger, None) # 重新加载
    st.session_state.file_loaded = False
    st.session_state.params_setted = False
    st.session_state.caculated = False
    st.session_state.saved = False
    st.session_state.outputed = False

if not st.session_state.file_loaded:
    header()
    st.write("### 📄导入DXF文件")
    st.session_state.uploaded_dxf_file = st.file_uploader('上传按照要求制作的 dxf 文件：',
        type='dxf',
        accept_multiple_files=False,
        key=None,
        help=None,
        disabled=st.session_state.file_loaded,
        label_visibility="visible",
        )
else:
    header()
    st.write('## 👍加载成功：' + st.session_state.uploaded_dxf_file.name)
    reload_page()

if not st.session_state.file_loaded:
    if st.session_state.uploaded_dxf_file:
        st.session_state.dxf_file = read_dxf_file(st.session_state.uploaded_dxf_file)
        st.session_state.file_loaded = True
        # 获取管件参数
        st.session_state.shrink_tube_instance.load_tube(st.session_state.dxf_file)
        st.session_state.tube_params = st.session_state.shrink_tube_instance.get_tube_params_df()
        st.rerun()
else:
    show_tube_params()
    if not st.session_state.params_setted:
        if st.button("参数设定", disabled=st.session_state.params_setted, use_container_width=True, type="primary", key="setted_button"):
            st.session_state.params_setted = True
            st.rerun()

if st.session_state.params_setted:
    settings = get_setting()
    if settings['mold_list'] != []:
        if not st.session_state.caculated:
            if st.button("计算", on_click=calculate, disabled=st.session_state.caculated, use_container_width=True, type="primary",
                         args=(settings,)):
                st.session_state.caculated = True
                st.rerun()
    else:
        st.write("⚠️请选择需要计算的模具！")



if st.session_state.caculated:
    show_caculate_results()
    if not st.session_state.saved:
        if st.button("保存", on_click=save_params_and_files, disabled=st.session_state.saved, use_container_width=True, type="primary"):
            st.session_state.saved = True
            st.rerun()
    else:
        st.divider()
        st.write('### 🎉保存成功！')



if st.session_state.saved:
    if not st.session_state.outputed:
        with open(st.session_state.zip_file_path, "rb") as file:
            btn = st.download_button(
                label="下载计算结果",
                data=file,
                file_name=st.session_state.zip_file_path,
                mime="application/zip",
                disabled=st.session_state.outputed,
                type="primary",
                key=None,
                use_container_width=True,
            )
            if btn:
                st.session_state.outputed = True
                st.rerun()
    else:
        st.divider()
        st.write('### 🎉下载成功！')