from main.core import model,State
import json
import re

def router_node(state: State):
    user_input = state["messages"][-1] if state["messages"] else ""
    print(user_input.content)
    print("currently at router node")

    print(state.get("accepted_candidates"))
    print(state.get("candidate_list"))
    print(state.get("rejected_candidates"))

    router_prompt = f"""
USER INPUT: {user_input.content}
Based on the user input Decide whether this is:
if general QnA route to "chatbot"
if request for suggestion for building a virtual environment route to "suggestions"
if package installation  "validation"
if asked for alternatives of a certain node route to "alternatives"
if asked DIRECTLY to build an ENVIRONMENT route to "build"

Return with JSON Field "next_node".
DO NOT include any other text, salutations or reasoning, only RETURN VALID JSON.
"""

    try:
        raw_resp = model.invoke(router_prompt)
        # print(raw_resp.content)
        pattern = r"```json(.*?)```"
        match = re.findall(pattern,raw_resp.content,re.DOTALL)[0]
        json_res = json.loads(match)
        print("JSON RESPONSE: ",json_res)
        print("JSON RESPONSE OF NEXT NODE AT ROUTER: ",json_res["next_node"])
        state["next_node"] = json_res["next_node"]
        return state
    except Exception as e:
        print("Exception at router node: ", str(e))
        state["next_node"] = "chatbot"
        return state
    
    # return {"next_node": model.invoke(router_prompt)}


if __name__ == "__main__":
    router_node()