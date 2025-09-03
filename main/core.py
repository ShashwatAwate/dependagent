from typing import Annotated
from typing_extensions import TypedDict

from langchain_mistralai import ChatMistralAI
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage

import json
import os
from dotenv import load_dotenv

load_dotenv()

def add_to_list(prev: list, new: list) -> list:
    return prev + [x for x in new if x not in prev]


model = ChatMistralAI(model='mistral-large-latest',api_key=os.getenv("MISTRAL_API_KEY"))

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

class State(TypedDict):
    messages: Annotated[list,add_messages]
    candidate_list: list
    accepted_candidates: Annotated[list,add_to_list]
    rejected_candidates: list
    next_node : str
