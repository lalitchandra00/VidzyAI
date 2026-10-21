from langchain_community.vectorstores import FAISS
from embeddings import embeddings

def create_retriever(chunks, k: int = 4):
    """Creates a FAISS vector store from document chunks and returns a retriever."""
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
