from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from prompt import prompt
from chat_model import chat_model

def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

def get_rag_chain(retriever):
    """Builds and returns the full RAG chain using the provided retriever."""
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })
    parser = StrOutputParser()
    return parallel_chain | prompt | chat_model | parser
