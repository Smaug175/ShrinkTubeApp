import streamlit as st
from menu import menu_with_redirect
import pandas as pd

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("软件功能介绍")

st.markdown("---")
st.markdown("### 1. 普通抽")
st.markdown("普通抽涉及不同机床和模具，其操作流程主要包括四部分，如下所示：")

st.image("sources/normal_process.png", caption="普通抽操作流程", use_container_width=True)


st.markdown("#### 1.1 导入管件的DXF文件")
st.markdown(
    "- 导入计算的管件文件必须按照我们给定的标准设置相应的参数。"
    "标准规则见制作标准管件图纸示例视频。同时需要将“车种规格”在输入图中进行额外的注明。")

with st.expander("标准输入 DXF 的制作教程", expanded=False):
    st.markdown("##### a. 导入管件的 DXF 文件")
    st.write("将原本的 DWG 文件转换为 DXF 文件，备后续使用。")
    # video_file_1 = open('../sources/1导出管件为DXF.mp4', 'rb')
    # video_bytes_1 = video_file_1.read()
    # st.video(video_bytes_1)

    st.markdown("##### b. 制作一抽的 DXF 文件")
    # video_file_2 = open('../sources/2制作一抽DXF.mp4', 'rb')
    # video_bytes_2 = video_file_2.read()
    # st.video(video_bytes_2)

    st.markdown("##### c. 制作二抽的 DXF 文件")
    # video_bytes_3 = open('../sources/3制作二抽DXF.mp4', 'rb')
    # video_bytes_3 = video_bytes_3.read()
    # st.video(video_bytes_3)

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


st.markdown("- 不同壁厚管件所需参数表如下：")

table_data = [
    ["车种规格", "车种规格", "当前管件所属车种规格"],
    ["D", "D", "抽管外径"],
    ["L", "L", "抽管总长"],
    ["L1", "L1", "壁厚从厚开始，第一段长度"],
    ["T1", "T1", "第一段壁厚"],
    ["M1", "M1", "第一段过渡段长度"],
    ["L2", "L2", "壁厚从厚开始，第二段长度"],
    ["", "T2", "第二段壁厚"],
    ["", "M2", "第二段过渡段长度"],
    ["", "L3", "壁厚从厚开始，第三段长度"],
    ["", "T3", "第三段壁厚"]
]

df = pd.DataFrame(table_data, columns=["两段不同壁厚", "三段不同壁厚", "描述"])

# 使用st.dataframe展示表格，隐藏索引列，并应用样式设置
st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("#### 1.2 计算模具参数")
st.write("- 可选择是否增加额外壁厚，默认否。增加额外壁厚会自动加入成型模具。")
st.write("- 需要选择输出模具的机器类型，默认选择DC0124。")
st.write("- 需要手动选择计算的模具，默认为空。")

st.markdown("#### 1.3 查看模具参数")
st.write("- 可以查看模具参数的计算结果。")
st.write("- TODO: 修改计算结果。此功能还未实现。")

st.markdown("#### 1.4 保存模具参数")
st.write("- 新模具的图号将在数据库最大图号的基础上叠加，所有数据将一键保存。")

st.markdown("#### 1.5 导出模具的DXF文件")
st.write("- 下载包含模具的 DXF 文件和汇总参数的 excel 表格的 zip 文件。")
st.write("- 模具使用图号命名。")
st.write("- 重复计算同一管件的模具参数，新的计算结果将会保存到数据库中，但是导出的文件将会覆盖之前的文件。")

st.markdown("---")
st.markdown("### 2. TP抽")
st.write("- TP抽目前还未完善。")

