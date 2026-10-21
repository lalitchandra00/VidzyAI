from langchain_community.vectorstores import FAISS
from yt_transcript import chunks
from embeddings import embeddings

# Data storage has done here and Retrival variable made
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})