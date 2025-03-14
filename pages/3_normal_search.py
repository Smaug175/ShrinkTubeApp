import streamlit as st
from menu import menu_with_redirect
from bin.normal_bin.utils.Normal_SQLite_Control import MoldControl
import time

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
    with st.spinner("正在查询数据..."):
        sqlite_control = MoldControl()
        try:
            # 执行查询并测量查询时间
            start_time = time.time()
            results = sqlite_control.query(machine, big_graph_number)
            query_time = time.time() - start_time

            # 保存查询结果到session_state
            st.session_state.results = results
            st.session_state.query_time = f"{query_time:.3f}"
            st.session_state.query_empty = results.empty

        except Exception as e:
            st.error(f"查询出错: {str(e)}")
            st.session_state.results = None
            st.session_state.query_error = str(e)


if st.button("查询", on_click=query_all_data, use_container_width=True, type="primary",
             kwargs={'machine': machine_type, 'big_graph_number': mold_list}):
    st.divider()

    # 显示查询时间（如果有）
    if 'query_time' in st.session_state:
        st.caption(f"查询耗时: {st.session_state.query_time} 秒")

    # 显示查询结果
    if 'results' in st.session_state and st.session_state.results is not None and not st.session_state.results.empty:
        if len(st.session_state.results) == 0:
            st.warning(f"没有找到数据记录")
        else:
            st.success(f"查询成功！找到 {len(st.session_state.results)} 条记录")

        # 直接显示数据表格，不需要搜索和排序功能
        st.dataframe(st.session_state.results, use_container_width=True, hide_index=True)

        # 添加数据下载按钮
        csv = st.session_state.results.to_csv(index=False)
        st.download_button(
            label="下载为CSV文件",
            data=csv,
            file_name=f"{machine_type}_{mold_list}_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        if 'query_empty' in st.session_state and st.session_state.query_empty:
            st.warning(f"未找到 {machine_type} 机床下 {mold_list} 模具的数据")
            st.write("可能的原因：")
            st.write("1. 数据库中没有相关数据")
            st.write("2. 模具尚未被保存到数据库")
            st.write("3. 数据库路径或表名配置错误")
        elif 'query_error' in st.session_state:
            st.error(f"查询发生错误: {st.session_state.query_error}")
        else:
            st.info("请点击查询按钮获取数据")