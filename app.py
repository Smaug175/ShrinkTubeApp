import streamlit as st
from menu import menu
from bin.global_bin.utils.User_SQLite_Control import UserControl

try:
    if "authority" not in st.session_state or "login" not in st.session_state or st.session_state.login == False or st.session_state.authority == None:
        st.session_state.authority = None
        st.session_state.login = False
except:
    st.session_state.authority = None
    st.session_state.login = False

@st.fragment
def login_wiget():
    # Widgets for login
    st.write("# ⌨️🔑登录")
    st.write("##### 请输入账号和密码：")
    st.session_state.id_number = st.text_input(label="账号：", value="")
    st.session_state.password = st.text_input(label="密码：", value="", type="password")

if not st.session_state.login:
    login_wiget()
    if st.button("登录", disabled=st.session_state.login, use_container_width=True, type="primary"):
        user_control = UserControl()
        input = {
            'id': st.session_state.id_number,
            'password': st.session_state.password
        }
        
        if input['id'] == '' or input['password'] == '':
            st.error("⚠️账号或密码不能为空！")
        else:
            # ('id', 'name', 'password', 'license', 'authority')
            result = user_control.query(input)
            if result[0]:
                st.session_state.login = True
                st.session_state.user_name = result[1][1]
                st.session_state.license = result[1][3]
                st.session_state.authority = result[1][4]
                st.rerun()
            else:
                st.session_state.login = False
                message = result[1]
                st.error('⚠️'+message)
else:
    st.switch_page("pages/0_main_page.py")

menu() # Render the dynamic menu