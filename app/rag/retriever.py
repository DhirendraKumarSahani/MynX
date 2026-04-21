from app.rag.vector_store import load_vector_store

def retrieve_docs(query, k=3):
    db = load_vector_store()
    return db.similarity_search(query, k=k)