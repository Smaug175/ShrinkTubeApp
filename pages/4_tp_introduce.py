import streamlit as st
from menu import menu_with_redirect
import pandas as pd

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("软件功能介绍")

st.markdown("---")
st.markdown("### 2. TP抽")
st.markdown("TP抽涉及不同模具，不涉及不同机床，其操作流程主要包括四部分，如下所示：")

st.image("bin/tp_bin/images/TP_Process.png", caption="TP抽操作流程", use_container_width=True)


st.markdown("#### 1.1 导入管件的DXF文件")
st.markdown(
    "- 导入计算的管件文件必须按照我们给定的标准设置相应的参数。"
    )

with st.expander("标准输入 DXF 的制作教程", expanded=False):
    st.markdown("##### a. 导入管件的 DXF 文件")
    st.write("将原本的 DWG 文件转换为 DXF 文件，备后续使用。")
    # video_file_1 = open('../sources/1导出管件为DXF.mp4', 'rb')
    # video_bytes_1 = video_file_1.read()
    # st.video(video_bytes_1)

    '''
    st.divider()
    zip_file_path = "../sources/Standard_Example.zip"
    with open(zip_file_path, "rb") as f:
        zip_file_bytes = f.read()

    st.download_button(
        label="点击下载上述的示例文件",
        data=zip_file_bytes,
        file_name="Examples.zip",
        mime="application/zip",
        use_container_width=True
    )
    '''


st.markdown("- 管件参数表如下：")

table_data = [
    ["D", "普通抽直径"],
    ["L", "抽管总长"],
    ["L1", "普通抽第一段长度"],
    ["T1", "普通抽第一段壁厚"],
    ["M1", "普通抽第一过渡段长"],
    ["L2", "普通抽第二段长度"],
    ["T2", "普通抽第二段壁厚"],
    ["M2", "普通抽第二过渡段长"],
    ["L3", "普通抽第三段长度"],
    ["T3", "普通抽第三段壁厚"],
    ["T_D", "TP抽最大直径"],
    ["T_L", "TP抽长度"],
    ["T_LR", "抽管留存长度"]
]

df = pd.DataFrame(table_data, columns=["参数", "描述"])

# 使用st.dataframe展示表格，隐藏索引列，并应用样式设置
st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("#### 1.2 计算模具参数")
st.write("- 可选择是否后续涉及Taper工艺、是否有特殊壁厚情况，影响可选模具计算列表")
#st.write("- 需要选择输出模具的机器类型，默认选择DC0124。")
st.write("- 需要手动选择计算的模具，默认为空。")

st.markdown("#### 1.3 查看模具参数")
st.write("- 可以查看模具参数的计算结果。")
st.write("- 修改计算结果。")

st.markdown("#### 1.4 保存模具参数")
st.write("- 新模具的图号将在数据库最大图号的基础上叠加，所有数据将一键保存。")

st.markdown("#### 1.5 导出模具的DXF文件")
st.write("- 下载包含模具的 DXF 文件和汇总参数的 excel 表格的 zip 文件。")
st.write("- 模具使用图号命名。")
st.write("- 重复计算同一管件的模具参数，新的计算结果将会保存到数据库中，但是导出的文件将会覆盖之前的文件。")

