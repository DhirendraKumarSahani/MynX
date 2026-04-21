from app.rag.rag_service import build_rag_context

def rag_search(query: str):
    """
    Retrieve relevant knowledge from local documents using vector search.
    Returns summarized context.
    """
    context = build_rag_context(query)
    return f"""
Use the following context to answer:

{context}
"""