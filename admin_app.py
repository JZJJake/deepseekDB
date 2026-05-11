import streamlit as st
import os
import time
from dotenv import load_dotenv
from document_parser import read_and_parse_file
from vector_store_manager import create_vector_store, get_vector_store

load_dotenv()

st.set_page_config(page_title="政策问答 AI - 管理端", layout="wide")

st.title("🛡️ 政策问答 AI - 后台管理控制台")

# Check system status
st.header("系统运行状态")
status_col1, status_col2 = st.columns(2)

vector_store_exists = os.path.exists("vector_store")
with status_col1:
    if vector_store_exists:
        st.success("✅ 向量数据库已就绪")
        try:
            vs = get_vector_store()
            count = vs._collection.count()
            st.info(f"📊 当前数据库中包含 {count} 条问答记录。")
        except Exception as e:
            st.error(f"无法读取数据库: {e}")
    else:
        st.warning("⚠️ 向量数据库未创建或为空，请先上传 Markdown 文件进行处理。")

with status_col2:
    if os.getenv("DEEPSEEK_API_KEY"):
        st.success("✅ DeepSeek API Key 已配置")
    else:
        st.error("❌ 未找到 DEEPSEEK_API_KEY 环境配置！")

st.divider()

# Upload File Section
st.header("📂 更新政策文档")
st.markdown("上传新的 Markdown 格式文件（问答形式）。**注意：上传新文件将会清空旧的数据库重新生成！**")
uploaded_file = st.file_uploader("选择一个 .md 文件", type=["md"])

if uploaded_file is not None:
    if st.button("开始处理文档并更新向量库", type="primary"):
        # Save temp file
        temp_dir = "data"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, "uploaded_temp.md")

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        progress_bar = st.progress(0, text="正在读取文件...")
        time.sleep(0.5)

        try:
            progress_bar.progress(20, text="正在解析 Markdown 问答块...")
            docs = read_and_parse_file(temp_path)
            st.write(f"成功解析出 **{len(docs)}** 个问答块。")

            progress_bar.progress(50, text="正在调用本地 Embedding 模型构建向量... (这可能需要一些时间)")

            # Recreate vector store
            create_vector_store(docs)

            progress_bar.progress(100, text="向量数据库构建完成！")
            st.success("✨ 文档更新成功！请刷新页面查看最新状态。")

        except Exception as e:
            st.error(f"处理过程中出现错误: {str(e)}")
            progress_bar.empty()
