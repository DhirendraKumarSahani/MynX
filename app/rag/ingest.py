from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from app.rag.vector_store import create_vector_store, load_vector_store
import os


def load_document(file_path):

    if file_path.endswith(".txt"):
        return TextLoader(file_path).load()

    elif file_path.endswith(".pdf"):
        return PyPDFLoader(file_path).load()

    elif file_path.endswith(".docx"):
        return UnstructuredWordDocumentLoader(file_path).load()

    else:
        raise ValueError("Unsupported file format")


def ingest_documents(folder_path="data"):

    all_docs = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        docs = load_document(file_path)

        # 🔥 ADD METADATA HERE
        for doc in docs:
            doc.metadata["source"] = file

        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(all_docs)

    # 🔥 MERGE WITH EXISTING DB
    try:
        db = load_vector_store()
        db.add_documents(split_docs)
    except:
        db = create_vector_store(split_docs)

    db.save_local("faiss_index")

    print("✅ Documents indexed successfully")

# ✅ THIS MUST BE OUTSIDE FUNCTION
if __name__ == "__main__":
    ingest_documents("data")