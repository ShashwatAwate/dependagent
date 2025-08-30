from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
load_dotenv()


msg = None
print("welcome!")
try:
    print("starting llm...")
    llm = ChatMistralAI(model="mistral-large-latest")
    print("llm started!...")
    print("invoking...")
    msg = llm.invoke("hii")
except Exception as e:
    print("fuck: ",str(e))
print(msg)
print(type(msg))
print("\n\n mssage content: \n\n",msg.content)