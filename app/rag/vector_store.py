import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

def create_vector_store(docs):
    return FAISS.from_documents(docs, embedding)

def load_vector_store(path=None):

    # 🔥 dynamic path
    path = path or os.getenv("VECTOR_DB_PATH", "faiss_index")

    return FAISS.load_local(
        path,
        embedding,
        allow_dangerous_deserialization=True
    )