from main.core import model,State
import json
import re

def router_node(state: State):
    user_input = state["messages"][-1] if state["messages"] else input("what do you want to do?")

    router_prompt = f"""
USER INPUT: {user_input}
Based on the user input Decide whether this is:
if general QnA route to "chatbot"
if request for suggestion of packages for building a virtual environment route to "suggestions"
if package installation  "validation"
Return with JSON Field "next_node".
DO NOT include any other text, salutations or reasoning, only RETURN VALID JSON.
"""

    try:
        raw_resp = model.invoke(router_prompt)
        # print(raw_resp.content)
        pattern = r"```json(.*?)```"
        match = re.findall(pattern,raw_resp.content,re.DOTALL)[0]
        json_res = json.loads(match)
        print("JSON RESPONSE OF NEXT NODE AT ROUTER: ",json_res["next_node"])
        return {"next_node": json_res["next_node"]}
    except Exception as e:
        print("Exception at router node: ", str(e))
        return {"next_node": "chatbot"}
    
    # return {"next_node": model.invoke(router_prompt)}


if __name__ == "__main__":
    router_node()