import streamlit as st
from menu import menu_with_redirect
from bin.global_bin.utils.License_Check import *
from bin.global_bin.utils.User_SQLite_Control import UserControl

menu_with_redirect()

def update_users_data(new_data, type):
    user_control = UserControl()
    if type == 'password':
        input = {
            'id': st.session_state.id_number,
            'password': new_data,
            'name': st.session_state.user_name,
            'license': st.session_state.license,
            'authority': 'user'
        }
    elif type == 'license':
        input = {
            'id': st.session_state.id_number,
            'password': st.session_state.password,
            'name': st.session_state.user_name,
            'license': new_license,
            'authority': 'user'
        }
    else:
        st.error("⚠️请指定需要修改的项目！")

    if input['id'] == '' or input['password'] == '' or input['name'] == '' or input['license'] == '':
        st.error("⚠️输入信息不能为空！")
    else:
        result = user_control.update(input)
        if result[0]:
            return True
        else:
            message = result[1]
            st.error('⚠️' + message)
            return False

st.write("# 🎉欢迎！")
st.write("账号是：", st.session_state.id_number)
# st.write("密码是：", st.session_state.password)
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

if st.button("刷新",use_container_width=True,):
    st.rerun()

st.divider()
st.write("## 📝个人信息维护")
# 新增的修改密码部分
with st.expander("修改密码"):
    old_password = st.text_input("请输入旧密码", type="password")
    new_password = st.text_input("请输入新密码", type="password")
    confirm_new_password = st.text_input("请再次输入新密码", type="password")
    if st.button("确认修改密码",use_container_width=True,):
        # 验证旧密码是否正确
        if old_password != st.session_state.password:
            st.error("旧密码输入错误，请重新输入。")
            st.stop()
        if new_password == "":
            st.error("新密码不能为空，请重新输入。")
            st.stop()
        if new_password == confirm_new_password:
            update_result = update_users_data(new_password, "password")
            if update_result:
                st.success("密码修改成功！")
                st.session_state.password = new_password
            else:
                st.error("密码修改失败，请检查输入信息是否正确。")
        else:
            st.error("两次输入的新密码不一致，请重新输入。")

# 新增的修改许可证部分
with st.expander("修改许可证"):
    new_license = st.text_input("请输入新的许可证")
    result = license_check(new_license)
    if st.button("确认修改许可证", use_container_width=True, ):
        if new_license == "":
            st.error("许可证不能为空，请重新输入。")
        if result[0]:
            st.info("许可有效期：" + result[1][0] + "开始，到" + result[1][1] + "结束。")
            update_result = update_users_data(new_license, "license")
            if update_result:
                st.success("许可证修改成功！")
                st.session_state.license = new_license
            else:
                st.error("许可证修改失败，请检查输入信息是否正确。")
        else:
            st.error(result[1])