from langchain.agents import tool
# from dotenv import load_dotenv
import json
import re
import requests
from pprint import pprint
import traceback

from main.core import model,State
# load_dotenv()

def validate_candidates(state: State):
        """
        Validates the candidates proposed under PyPi API.
        """
        print("currently at validation state")
        can_list = state["current_candidates"]
        accepted_cans = []
        rejected_cans = [] 
        for package_name in can_list:
            print(f"trying to fetch data for {package_name}")
            endpoint_template = f"https://pypi.org/pypi/{package_name}/json"
            try:
                response = requests.get(endpoint_template)
                # pprint(response.text[:20])
                if response.status_code == 404 or response.status_code==500:
                    print(f"module name {package_name} is not found in pypi")
                    rejected_cans.append(package_name)
                else:
                    try:
                        json_response = json.loads(response.text)
                        accepted_cans.append(json_response["info"]["name"])
                        pprint(json_response["info"]["name"])
                    except Exception as e:
                        print(f"exception in loading json response from PYPi(validation): {str(e)}")
                        print(f"Exception type: {type(e).__name__}")
                        # print("validation traceback",traceback.print_stack())
                        return {"accepted_candidates":[],"rejected_candidates":[],"next_node":"end"}
                pass
            except Exception as e:
                print("exception during validation",str(e))
                print("Exception type: ",type(e).__name__)
                return {"accepted_candidates":[],"rejected_candidates":[],"next_node":"end"}
        print("accepted cans at validation node ",accepted_cans)

        state["accepted_candidates"] = accepted_cans
        state["rejected_candidates"] = rejected_cans
        if rejected_cans==[]:
            state["next_node"] = "display"
        else:
            state["next_node"] = "alternatives"
        return state
    

def parse_model_response(res,can_list):
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern,res,re.DOTALL)
    for m in matches:
        data = json.loads(m.strip())
        for cans in data['packages']:
            can_name = cans['name']
            can_list.append(can_name)



def suggest_candidates(state: State):
    """
        Adds the suggested candidates to a list and a description dictionary.
    """
    can_list = []
    # user_input = state["messages"][-1] if state["messages"] else ""
    print("currently at suggest candidates")
    history = state["messages"] if state["messages"] else "how to make data science virtual env"
    suggest_prompt_template = f"""
        You are an expert in Python Packages.
        You have to suggest 5 starter packages based on the  project topic suggested by the user OR provide 5 alternatives for a package stated by the user:
        HISTORY: {history}
        ONLY RESPOND IN JSON. FOLLOW THE BELOW FORMAT ONLY :-
        ```json
        {{
            "packages" : [
            {{
                "name": "",
            }}]
        }}
        ```
        DO NOT inlcude any extra text, salutations or explanations or reasoning.
    """
    try:
        res = model.invoke(suggest_prompt_template)
        print(res.content)
    except Exception as e:
        print("exception at suggest candidates: ",str(e))
        state["candidate_list"] = []
        state["current_candidates"] = []
        state["next_node"] = "end"
        return state

    if res:
        parse_model_response(res.content,can_list)
    else:
        print("model response not recieved during suggestions")
    state["candidate_list"] = can_list
    state["current_candidates"] = can_list
    state["next_node"] = "validation"
    return state




