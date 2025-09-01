from typing import Annotated
from typing_extensions import TypedDict

from langchain_mistralai import ChatMistralAI


from langgraph.graph import StateGraph,START,END


from dotenv import load_dotenv
import os
import re

from agent.prepare_candidates import *
from agent.router_node import router_node

from .core import model,State



graph_builder = StateGraph(State)

def chatbot(state: State):
    """Gives the message history to the llm and we get response appended to the 'messages' """
    return {"messages": [model.invoke(state['messages'])]}

def router_conditional(state: State):
    """Returns the next node to go to"""

    return state["next_node"]

def stream_graph_updates(user_input: str):
    """Just for printing the LLM's messages"""

    for event in graph.stream({'messages':[{"role": "user", "content": user_input}]}):
        for value in event.values():
            if "messages" in value and value["messages"]:
                print("Assistant: ",value["messages"][-1].content)
            elif "next_node" in value:
                print(f"Routing to next node {value["next_node"]}")



#                           -----NODES-----
graph_builder.add_node(router_node)
graph_builder.add_node(chatbot)

#                           -----EDGES-----
graph_builder.add_edge(START,"router_node")
graph_builder.add_conditional_edges(
    "router_node",router_conditional,
    {
        "chatbot":"chatbot",
        # "suggesstions": "suggestions",
        # "validation":"validation"
    }
)
graph_builder.add_edge("chatbot",END)
graph = graph_builder.compile()



if __name__ == "__main__":
    while True:
        try:
            
            user_input = input("enter a message ")
            if user_input.lower() in ["quit",'q']:
                print("exiting")
                break
            stream_graph_updates(user_input)
            pass
        except :
            fallback_input = "What is the meaning of AI?"
            stream_graph_updates(fallback_input)
    pass