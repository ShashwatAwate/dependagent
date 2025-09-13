from langchain_core.messages import AIMessage

from main.core import model,State

import traceback

def display_cans(state: State):
    """Just displays the accepted validated candidates"""

    print("currently at display node")
    try:
        accepted_cans = state["accepted_candidates"]
        message_content = f"Here are the packages I'll install if you want...\n"
        # print("Here are the packags I'll install if you want...")
        for num,candidate in enumerate(accepted_cans):
            # print(f"{num}. {candidate}")
            message_content += f"{num}. {candidate} \n"
        # print("Do you want to add or remove any packages or need help regarding these packages? Let me know!")
        message_content += "Do you want to add or remove any packages or need help regarding these packages? Let me know! \n"
        state["messages"].append(AIMessage(content=message_content))
        state["accepted_candidates"] =accepted_cans
    except Exception as e:
        print("something happened at display node")
        print(str(e))
        print(type(e).__name__)
        print(traceback.print_stack())
    print("message_content: ",message_content)
    return state