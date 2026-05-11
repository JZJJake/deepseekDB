import os
import shutil
from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# The embedding model. BAAI/bge-small-zh-v1.5 is a very good open-source Chinese model.
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"
VECTOR_STORE_DIR = "vector_store"

import streamlit as st

@st.cache_resource
def get_embeddings():
    """Returns the HuggingFace embeddings model."""
    # Run on cpu, we can change to cuda if a GPU is available.
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def create_vector_store(documents: List[Document], persist_directory: str = VECTOR_STORE_DIR):
    """
    Creates a new vector store from a list of documents.
    If a vector store already exists, it removes it first to create a fresh one.
    """
    if os.path.exists(persist_directory):
        print(f"Removing existing vector store at {persist_directory}...")
        shutil.rmtree(persist_directory)

    print(f"Creating new vector store from {len(documents)} documents...")
    embeddings = get_embeddings()

    # Create the vector store
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Vector store created at {persist_directory}.")
    return vectorstore

def get_vector_store(persist_directory: str = VECTOR_STORE_DIR):
    """
    Loads an existing vector store.
    """
    if not os.path.exists(persist_directory):
        raise ValueError("Vector store does not exist. Please create it first.")

    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vectorstore
