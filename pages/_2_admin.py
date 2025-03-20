import streamlit as st
from menu import menu_with_redirect
from bin.global_bin.utils.User_SQLite_Control import UserControl
import time
import pandas as pd
from bin.global_bin.utils.License_Check import *

menu_with_redirect()

if st.session_state.authority != "admin":
    st.warning("你没有权限访问此网页！")
    st.stop()


def query_all_users():
    with st.spinner("正在查询数据..."):
        sqlite_control = UserControl()
        try:
            # 执行查询并测量查询时间
            start_time = time.time()
            results = sqlite_control.query_all()
            query_time = time.time() - start_time
            if not results[0]:
                st.error(f"查询出错: {str(results[1])}")
                st.session_state.users_results = None
                st.session_state.query_error = str(results[1])
                return

            # 保存查询结果到 session_state
            st.session_state.users_results = pd.DataFrame(results[1],
                                                          columns=['id', '姓名', '密码', '许可证', '权限'])
            st.session_state.query_time = f"{query_time:.3f}"
        except Exception as e:
            st.error(f"查询出错: {str(e)}")
            st.session_state.users_results = None
            st.session_state.query_error = str(e)


query_all_users()

st.title("📊 管理用户数据")
st.write('管理员可以对用户进行查询、删除和添加管理。')
st.divider()

st.write("## 查询所有用户：")
# 初始化 session_state
if 'queryed' not in st.session_state:
    st.session_state.users_results = None
    st.session_state.queryed = False

if st.button("查询所有用户", on_click=query_all_users, use_container_width=True, type="primary"):
    if st.session_state.users_results is None or len(st.session_state.users_results) == 0:
        st.warning(f"没有找到数据记录")
    else:
        st.session_state.queryed = True


if st.session_state.queryed:
    st.success(f"查询成功！找到 {len(st.session_state.users_results)} 条记录")
    st.write("### 所有用户数据：")
    if st.session_state.users_results is not None and not st.session_state.users_results.empty:
        selected = st.dataframe(
            st.session_state.users_results,
            use_container_width=True,
            hide_index=True,
            selection_mode="multi-row",
            on_select="rerun"
        )

        if selected:
            selected_rows = selected['selection']["rows"]
            if selected_rows:
                if st.button("删除选中的用户", use_container_width=True, type="primary"):
                    users_ids = []
                    for index in selected_rows:
                        users_ids.append(st.session_state.users_results.iloc[index]['id'])
                    for user_id in users_ids:
                        if int(user_id) == int(st.session_state.id_number):
                            st.error("⚠️你不能删除自己！")
                            continue
                        user_control = UserControl()
                        result = user_control.delete(user_id)
                    st.success(f"删除用户成功！")
                    if st.button("刷新", use_container_width=True):
                        st.rerun()
            else:
                st.warning(f"没有选中任何用户记录")
    else:
        st.warning(f"没有找到数据记录")


st.divider()
st.write("## 添加新用户：")
# 添加新用户的表单
with st.expander("安照以下格式添加新用户"):
    new_user_id = st.number_input("用户 ID", min_value=1, step=1)
    new_user_name = st.text_input("姓名")
    new_user_password = st.text_input("密码", type="password")
    new_user_license = st.text_input("许可证")
    new_user_authority = st.selectbox("权限", ["user", "admin"])

    if st.button("添加新用户", use_container_width=True, type="primary"):
        new_user_data = {
            'id': new_user_id,
            'name': new_user_name,
            'password': new_user_password,
            'license': new_user_license,
            'authority': new_user_authority
        }
        result = license_check(new_user_license)
        if result[0] == False:
            st.error("⚠️" + result[1])
        else:
            user_control = UserControl()
            result = user_control.insert_data(new_user_data)
            if result[0]:
                st.success("新用户添加成功！")
                query_all_users()  # 重新查询数据以更新显示
                if st.button("刷新", use_container_width=True):
                    st.rerun()
            else:
                st.error(f"添加新用户失败: {result[1]}")