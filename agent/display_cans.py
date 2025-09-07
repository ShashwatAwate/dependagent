from langchain_core.messages import AIMessage

from main.core import model,State


def display_cans(state: State):
    """Just displays the accepted validated candidates"""

    accepted_cans = state["accepted_candidates"]
    message_content = f"Here are the packages I'll install if you want...\n"
    # print("Here are the packags I'll install if you want...")
    for num,candidate in enumerate(accepted_cans):
        # print(f"{num}. {candidate}")
        message_content += f"{num}. {candidate} \n"
    # print("Do you want to add or remove any packages or need help regarding these packages? Let me know!")
    message_content += "Do you want to add or remove any packages or need help regarding these packages? Let me know! \n"
    state["messages"].append(AIMessage(content=message_content))
    return state