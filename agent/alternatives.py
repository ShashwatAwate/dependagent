from main.core import State,model
from main.tools import get_correct_name_tool
from utils.utils import res_to_json

import time
import json


base_interval = 3
def suggest_alternatives(state: State) -> list:
    """used to suggest alternatives to a package or search up its correct name using a web search"""
    rejected_cans = state["rejected_candidates"]
    if(rejected_cans==[]):
        return{"candidate_list":[],"next_node":"display"}
    current_cans = []
    for package in rejected_cans:
    
        web_content = get_correct_name_tool.invoke(package)
        if(web_content==""):
            alts_prompt = f"""
            Suggest single best alternative for the python package {package}.
            ONLY RETURN VALID JSON.
            Follow the below format: 
             ```json
                {{
                    "name":""
                }}
                ```
            """
            llm_res = model.invoke(alts_prompt)
            res_content = llm_res.content
            print("response content ",res_content)
            try:
                json_content = res_to_json(res_content)
                package_name = json_content["name"]
                # print(f"suggested alternative: {package_name}")
                current_cans.append(package_name)
            except Exception as e:
                print(f"Exception during suggesting alternatives: {str(e)}")
                print(f"Exception type: {type(e).__name__}")
                state["current_candidates"] = []
                state["next_node"] = "end"
                return state
        else:
            pckg_extraction_prompt = f"""
Given the below text, find the correct python package name from it:
TEXT: {web_content}
ONLY RETURN VALID JSON.
Follow the below format: 
 ```json
    {{
        "name":""
    }}
    ```
""" 
            
            llm_res = model.invoke(pckg_extraction_prompt)
    
            res_content = llm_res.content
            try:
                json_content = res_to_json(res_content)
                package_name = json_content["name"]
                # print(f"suggested alternative: {package_name}")
                current_cans.append(package_name)
            except Exception as e:
                print(f"Exception during suggesting alternatives: {str(e)}")
                print(f"Exception type: {type(e).__name__}")
                state["current_candidates"] = []
                state["next_node"] = "end"
                return state
    state["current_candidates"] = current_cans 
    state["next_node"] = "validation"  
    return state
    time.sleep(3**2)




if __name__ == "__main__":
    rejected_cans = ["cv2","torch","redis"]
    # suggest_alternatives(rejected_cans=rejected_cans)
