from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know no context in the video.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)