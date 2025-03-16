import streamlit as st
from menu import menu_with_redirect
import pandas as pd

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("软件功能介绍")

st.markdown("---")
st.markdown("### 3. Taper")
st.markdown("Taper涉及不同模具，涉及不同机床，其操作流程主要包括四部分，如下所示：")

st.image("bin/taper_bin/images/taper_process.png", caption="Taper操作流程", use_container_width=True)


st.markdown("#### 3.1 导入管件的DXF文件")
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
    ["BL","TAPER前管长"],
    ["D", "TAPER最大直径"],
    ["TL", "打TAPER操作长度"],
    ["m_D", "TAPER模型腔的最小直径"],
    ["B_D", "打taper前管直径"],
]

df = pd.DataFrame(table_data, columns=["参数", "描述"])

# 使用st.dataframe展示表格，隐藏索引列，并应用样式设置
st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("#### 3.2 计算模具参数")
st.write("- 可根据TL长度选择不同的加工机床，影响可选模具计算列表")
#st.write("- 需要选择输出模具的机器类型，默认选择DC0124。")
st.write("- 可输入用于Taper模过渡的tp抽形线长度，范围为20~30mm，默认为25mm")
st.write("- 需要手动选择计算的模具，默认为空。点击全选后，将计算所有可选模具。")

st.markdown("#### 3.3 查看模具参数")
st.write("- 可以查看模具参数的计算结果。")
st.write("- 修改计算结果。")

st.markdown("#### 3.4 保存模具参数")
st.write("- 新模具的图号将在数据库最大图号的基础上叠加，所有数据将一键保存。")

st.markdown("#### 3.5 导出模具的DXF文件")
st.write("- 下载包含模具的 DXF 文件和汇总参数的 excel 表格的 zip 文件。")
st.write("- 模具使用图号命名。")
st.write("- 重复计算同一管件的模具参数，新的计算结果将会保存到数据库中，但是导出的文件将会覆盖之前的文件。")

