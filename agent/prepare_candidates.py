from langchain.agents import tool
# from dotenv import load_dotenv
import json
import re
import requests
from pprint import pprint


# load_dotenv()
candidate_list = []
candidate_purpose = {}
rejected_packages = []
python_version = None

def validate_candidates(package_name):
        print(f"trying to fetch data for {package_name}")
        endpoint_template = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(endpoint_template)
            # pprint(response.text[:20])
            if response.status_code == 404 or response.status_code==500:
                print(f"module name {package_name} is not found in pypi")
                candidate_list.remove(package_name)
                candidate_purpose.remove(package_name)
                rejected_packages.append(package_name)
            else:
                try:
                    json_response = json.loads(response.text)
                    pprint(json_response)
                except Exception as e:
                    print(f"error: {str(e)}")
                    return None
            pass
        except Exception as e:
            print("error ",str(e))
            return None
    

def suggest_candidates(cans: dict):
    """
        Adds the suggested candidates to a list and a description dictionary.
    """
    for candidate,purpose in cans.items():
        candidate_list.append(candidate)
        candidate_purpose[candidate] = purpose

def parse_model_response(res,candidate_list,candidate_purpose):
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern,res,re.DOTALL)
    for m in matches:
        data = json.loads(m.strip())
        python_version = data['python_version']
        for cans in data['packages']:
            can_name = cans['name']
            can_purpose = cans['purpose']
            candidate_list.append(can_name)
            candidate_purpose[can_name] = can_purpose


def add_user_candidates(candidate):
    candidate_list.append(candidate)
    candidate_purpose[candidate] = "user added package"



