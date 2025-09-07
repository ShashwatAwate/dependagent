
from langgraph.graph import StateGraph,START,END

import traceback

from agent.prepare_candidates import suggest_candidates,validate_candidates
from agent.router_node import router_node
from agent.alternatives import suggest_alternatives
from agent.display_cans import display_cans
from .core import tool_node

from .core import State,chatbot



graph_builder = StateGraph(State)


def router_conditional(state: State):
    """Returns the next node to go to"""

    return state["next_node"]

def route_tools(state: State):
    """This function will return 'tools' if tool_node is to be routed to, else it will route to router"""
    if isinstance(state,list):
        ai_message = state["messages"][-1]
    elif messages := state.get("messages",[]):
        ai_message = state["messages"][-1]
    else:
        raise ValueError(f"No messages found in input for tool_edge {state}")
    
    if hasattr(ai_message,"tool_calls") and len(ai_message.tool_calls)>0:
        return "tools"
    return "router"


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
graph_builder.add_node(suggest_candidates)
graph_builder.add_node(validate_candidates)
graph_builder.add_node(suggest_alternatives)
graph_builder.add_node(display_cans)
graph_builder.add_node("tool_node",tool_node)

#                           -----EDGES-----
graph_builder.add_edge(START,"router_node")
graph_builder.add_conditional_edges(
    "router_node",router_conditional,
    {
        "chatbot":"chatbot",
        "suggestions": "suggest_candidates",
    }
)
graph_builder.add_conditional_edges(
    "suggest_alternatives",router_conditional,
    {
        "end":END,
        "validation":"validate_candidates",
        "display": "display_cans"
    }
)
graph_builder.add_conditional_edges(
    "validate_candidates",router_conditional,
    {
        "end":END,
        "display":"display_cans",
        "alternatives":"suggest_alternatives"
    }
)
graph_builder.add_edge("chatbot",END)
graph_builder.add_edge("suggest_candidates","validate_candidates")
graph_builder.add_edge("display_cans",END)

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
        except Exception as e:
            print("exception occured during execution of graph: ",str(e))
            traceback.print_exc()
            fallback_input = "What is the meaning of AI?"
            stream_graph_updates(fallback_input)
    pass