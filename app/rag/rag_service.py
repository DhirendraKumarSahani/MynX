from app.rag.retriever import retrieve_docs

def build_rag_context(query):

    docs = retrieve_docs(query, k=3)

    context = ""

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        context += f"[Source: {source}]\n{doc.page_content}\n\n"

    # 🔥 TOKEN CONTROL (VERY IMPORTANT)
    return context[:1500]   # limit context size