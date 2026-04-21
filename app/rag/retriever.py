from app.rag.vector_store import load_vector_store

_db = None

def get_db():
    global _db

    if _db is None:
        _db = load_vector_store()

    return _db


def retrieve_docs(query, k=3):
    db = get_db()
    return db.similarity_search(query, k=k)