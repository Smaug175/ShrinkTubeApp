import streamlit as st
from menu import menu_with_redirect
from bin.global_bin.utils.License_Check import *

st.title("主页")

result = license_check(st.session_state.license)

if result[0]:
    st.info("许可有效期："+result[1][0]+"开始，到"+result[1][1]+"结束。")
    st.session_state.license_valid = True
else:
    st.error(result[1])
    st.session_state.license_valid = False


st.divider()
st.write("### 📣普通抽")
st.page_link("pages/1_normal_introduce.py", label="普通抽介绍", disabled=not st.session_state.license_valid)
st.page_link("pages/2_normal_caculate.py", label="普通抽计算", disabled=not st.session_state.license_valid)
st.page_link("pages/3_normal_search.py", label="普通抽查找数据", disabled=not st.session_state.license_valid)
st.divider()

st.write("### 📣TP抽")
st.page_link("pages/4_tp_introduce.py", label="TP抽介绍", disabled=not st.session_state.license_valid)
st.page_link("pages/5_tp_caculate.py", label="TP抽计算", disabled=not st.session_state.license_valid)
st.page_link("pages/6_tp_search.py", label="TP抽查找数据", disabled=not st.session_state.license_valid)
st.divider()

st.write("### 📣Taper")
st.page_link("pages/7_taper_introduce.py", label="Taper介绍", disabled=not st.session_state.license_valid)
st.page_link("pages/8_taper_caculate.py", label="Taper计算", disabled=not st.session_state.license_valid)
st.page_link("pages/9_taper_search.py", label="Taper查找数据", disabled=not st.session_state.license_valid)
st.divider()

menu_with_redirect()