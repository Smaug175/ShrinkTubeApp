import streamlit as st
from menu import menu
from bin.global_bin.utils.User_SQLite_Control import UserControl
from bin.global_bin.utils.License_Check import *

# Initialize st.session_state.authority to None
if "authority" not in st.session_state or "login" not in st.session_state or st.session_state.login == False or st.session_state.authority == None:
    st.session_state.authority = None
    st.session_state.login = False
    
@st.fragment
def sign_up_wiget():
    # Widgets for login
    st.write("# ✍️📋注册")
    st.write("##### 请填写以下信息：")
  
    st.session_state.id_number = st.text_input(label="账号（只能使用数字）：", value="")
    st.session_state.password = st.text_input(label="密码：", value="")
    st.session_state.user_name = st.text_input(label="姓名：", value="")
    st.session_state.license = st.text_input(label="许可证：", value="")
    
if not st.session_state.login:
    sign_up_wiget()
    if st.button("注册", disabled=st.session_state.login, use_container_width=True, type="primary"):
        user_control = UserControl()
        input = {
            'id': st.session_state.id_number,
            'password': st.session_state.password,
            'name': st.session_state.user_name,
            'license': st.session_state.license,
            'authority': 'user'
        }

        if input['id'] == '' or input['password'] == '' or input['name'] == '' or input['license'] == '':
            st.error("⚠️输入信息不能为空！")
        else:
            result = license_check(st.session_state.license)
            if result[0] == False:
                st.error("⚠️"+result[1])
            else:
                # 注册
                result = user_control.insert_data(input)
                if result[0]:
                    st.session_state.login = True
                    st.session_state.authority = result[1]
                    st.rerun()
                else:
                    st.session_state.login = False
                    message = result[1]
                    st.error('⚠️'+message)
else:
    st.switch_page("pages/0_main_page.py")

menu() # Render the dynamic menu