import streamlit as st
from menu import menu_with_redirect
import tempfile
from tools.normal import logger, config_setting_instance, MOLDS
from bin.ShrinkTube import ShrinkTubeClass
from bin.utils.SQLite_control import MoldControl

# 显示侧边
menu_with_redirect()

machine_big_graph_number = {
    "DC0124": ['AD03','DIEO','SS01','AD02','ADIE','ADBT','AD01'],
    "DC0121": ['AD03','AD04','DIEO','SS01','AD02','ADIE','ADBT','AD01'],
    "DC0125": ['AD06_F','AD06_S','DIEO','SS01','AD07','ADIE','ADBT']
    }


st.title("📊查找数据")
st.divider()

st.write('#### 选择相应的机床型号和模具图号：')

machine_type = st.selectbox(
    "请选择机床型号：",
    machine_big_graph_number.keys(),
)

mold_list = st.selectbox(
    "请选择模具图号：",
    machine_big_graph_number[machine_type],
)

def query_all_data(machine, big_graph_number):
    sqlite_control = MoldControl()
    st.session_state.results = sqlite_control.query(machine, big_graph_number)


if st.button("保存", on_click=query_all_data, use_container_width=True, type="primary",kwargs={'machine':machine_type, 'big_graph_number':mold_list}):
    st.divider()
    st.dataframe(st.session_state.results,
                 use_container_width=True,
                 hide_index=True,
                 )