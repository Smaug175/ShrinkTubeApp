import streamlit as st
from menu import menu
from bin.utils.SQLite_control import UserControl

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
    st.session_state.password = st.text_input(label="密码：", value="")

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
    if st.session_state.authority == 'user':
        st.switch_page("pages/user.py")
    elif st.session_state.authority == 'admin':
        st.switch_page("pages/admin.py")
    elif st.session_state.authority == 'super-admin':
        st.switch_page("pages/super-admin.py")


menu() # Render the dynamic menu