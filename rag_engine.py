import os
from typing import List
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from vector_store_manager import get_vector_store

load_dotenv()

# We need the API key for DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")

def get_llm():
    """Returns the DeepSeek LLM instance."""
    # We use ChatOpenAI because DeepSeek's API is compatible with OpenAI's format
    return ChatOpenAI(
        model="deepseek-v4-pro",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_API_BASE,
        temperature=0.0, # Zero temperature to avoid hallucination
        max_tokens=2048,
    )

import streamlit as st

@st.cache_resource
def setup_rag_chain():
    """Sets up the Retrieval-Augmented Generation chain."""
    llm = get_llm()
    vectorstore = get_vector_store()

    # Retrieve top 3 most relevant Q&A blocks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # The prompt STRICTLY limits the AI to the provided context.
    system_prompt_template = """你是一个严谨的高新技术企业认定政策问答助手。
请严格基于以下检索到的【政策问答库内容】来回答用户的问题。

【政策问答库内容】：
{context}

回答要求：
1. 你的回答必须完全来源于上述提供的【政策问答库内容】，不得包含任何外部知识、杜撰或猜测。
2. 如果用户的问题在上述内容中没有直接或间接提及，请务必直接回复：“抱歉，该政策文档中未包含相关内容。”
3. 如果内容中有相关信息，请提取并分析这些信息，给出准确、清晰、连贯的答复。

用户问题：{input}
"""

    prompt = PromptTemplate.from_template(system_prompt_template)

    # Create the document chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain

def ask_question(question: str) -> str:
    """Convenience function to ask a question to the RAG system."""
    chain = setup_rag_chain()
    response = chain.invoke({"input": question})
    return response["answer"]
