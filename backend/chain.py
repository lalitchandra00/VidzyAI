from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Import components from your other files
from database import retriever
from prompt import prompt
from chat_model import chat_model  # <-- this connects to chat_model.py

def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

parser = StrOutputParser()

# Connect everything together:
main_chain = parallel_chain | prompt | chat_model | parser