import streamlit as st
from menu import menu_with_redirect
from bin.global_bin.utils.License_Check import *


st.write("# 🎉欢迎！")
st.write("账号是：", st.session_state.id_number)
st.write("密码是：", st.session_state.password)
st.write("姓名是：", st.session_state.user_name)
st.write("许可证是：", st.session_state.license)

result = license_check(st.session_state.license)

if result[0]:
    st.info("许可有效期："+result[1][0]+"开始，到"+result[1][1]+"结束。")
    st.session_state.license_valid = True
else:
    st.error(result[1])
    st.session_state.license_valid = False

st.write("权限是：", st.session_state.authority)

menu_with_redirect()

