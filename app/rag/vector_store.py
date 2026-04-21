import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings


_embedding = None

def get_embedding():
    global _embedding

    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
        )

    return _embedding

def create_vector_store(docs):

    return FAISS.from_documents(docs, get_embedding())

def load_vector_store(path=None):

    # 🔥 dynamic path
    path = path or os.getenv("VECTOR_DB_PATH", "faiss_index")

    return FAISS.load_local(
        path,
        get_embedding(),
        allow_dangerous_deserialization=True
    )