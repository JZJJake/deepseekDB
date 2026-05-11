import streamlit as st
import os

from rag_engine import ask_question
from vector_store_manager import VECTOR_STORE_DIR

st.set_page_config(page_title="政策问答 AI", layout="centered", page_icon="💬")

st.title("🏛️ 高新技术企业政策问答 AI")

if not os.path.exists(VECTOR_STORE_DIR):
    st.warning("⚠️ 知识库尚未初始化。请先通过管理后台(端口 8502)上传您的MD政策文档并生成知识库。")
else:
    st.markdown("欢迎使用政策问答小助手。你可以提出任何关于高新技术企业认定的问题，我会基于官方政策文件为您解答。")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("请输入您关于高新政策的问题..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Show a spinner while the model is reasoning
        with st.spinner("AI 正在检索政策库并分析作答，请稍候..."):
            try:
                response = ask_question(prompt)

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                error_msg = f"抱歉，系统处理时发生错误，请稍后重试。({str(e)})"
                with st.chat_message("assistant"):
                    st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
