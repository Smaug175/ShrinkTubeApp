import streamlit as st


def authenticated_menu_valid():
    st.sidebar.page_link("pages/0_main_page.py", label="主页")

    st.sidebar.divider()
    st.sidebar.header("普通抽")
    st.sidebar.page_link("pages/1_normal_introduce.py", label="📣普通抽介绍", disabled=not st.session_state.license_valid)
    st.sidebar.page_link("pages/2_normal_caculate.py", label="🧮普通抽计算", disabled=not st.session_state.license_valid)
    st.sidebar.page_link("pages/3_normal_search.py", label="🔎普通抽查找数据", disabled=not st.session_state.license_valid)
    st.sidebar.divider()

    # TP 界面
    st.sidebar.header("TP抽")
    st.sidebar.page_link("pages/4_tp_introduce.py", label="📣TP抽介绍", disabled=not st.session_state.license_valid)
    st.sidebar.page_link("pages/5_tp_caculate.py", label="🧮TP抽计算", disabled=not st.session_state.license_valid)
    st.sidebar.page_link("pages/6_tp_search.py", label="🔎TP抽查找数据", disabled=not st.session_state.license_valid)
    #

    st.sidebar.divider()

    st.sidebar.header("账户管理")
    st.sidebar.page_link("pages/_1_user.py", label="你的账户")

    if st.session_state.authority in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/_2_admin.py", label="用户管理")
        st.sidebar.page_link(
            "pages/_3_super-admin.py",
            label="用户许可管理",
            disabled=st.session_state.authority != "super-admin",
        )

    st.sidebar.divider()

    if st.sidebar.button("退出登录", use_container_width=True):
        st.session_state.authority = None
        st.session_state.logged_in = False
        st.rerun()

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="🔑登录")
    st.sidebar.page_link("pages/_0_sign_up.py", label="✍️注册")


def menu():
    # 确定用户是否已登录，然后显示正确的导航菜单
    if "authority" not in st.session_state or st.session_state.authority is None:
        unauthenticated_menu()
        return
    authenticated_menu_valid()


def menu_with_redirect():
    # 如果未登录，则将用户重定向到主页面，否则继续渲染导航菜单
    if "authority" not in st.session_state or st.session_state.authority is None:
        st.switch_page("app.py")
    menu()