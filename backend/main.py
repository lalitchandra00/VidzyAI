from chain import main_chain

question = input("Enter your question: ")
answer = main_chain.invoke(question)
print(answer)