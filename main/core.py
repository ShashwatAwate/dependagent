from typing import Annotated
from typing_extensions import TypedDict

from langchain_mistralai import ChatMistralAI
from langgraph.graph.message import add_messages



import os
from dotenv import load_dotenv

load_dotenv()

def add_to_list(prev: list, new: list) -> list:
    return prev + [x for x in new if x not in prev]


model = ChatMistralAI(model='mistral-large-latest',api_key=os.getenv("MISTRAL_API_KEY"))



class State(TypedDict):
    messages: Annotated[list,add_messages]
    candidate_list: list
    accepted_candidates: Annotated[list,add_to_list]
    rejected_candidates: list
    next_node : str
