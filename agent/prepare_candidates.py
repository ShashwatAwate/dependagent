from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import json
import re

load_dotenv()
candidate_list = []
candidate_purpose = {}
model = ChatMistralAI(model='mistral-large-latest')

def print_can_datastructures():
    print(candidate_list)
    print(candidate_purpose)

def parse_model_response(res):
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern,res,re.DOTALL)
    for m in matches:
        data = json.loads(m.strip())
        for cans in data['packages']:
            can_name = cans['name']
            can_purpose = cans['purpose']
            candidate_list.append(can_name)
            candidate_purpose[can_name] = can_purpose

def validate_candidates():
    pass
def start():

    user_message = input("What do you wanna build?\n")

    prompt_template = f"""
    You are a highly skilled Python engineer specializing in almost everything related to Python Packages.
    You have to provide a minimal list of correct and viable starter packages a user needs to install in their virtual environment according to the topic they have mentioned in the
    following message.
    USER MESSAGE : {user_message}
    Return the list in valid **JSON FORMAT ONLY**
    **DO NOT INCLUDE ANY ADDITIONAL TEXT, SALUTATIONS OR ANYTHING ELSE. JUST JSON**
    **ONLY FOLLOW THE FOLLOWING FORMAT**
    ```json
    {{
        "packages":[
        {{
            "name": "",
            "purpose": ""
        }}
        ]
    }}
    """
    res = model.invoke(prompt_template)
    parse_model_response(res.content)


if __name__ == "__main__":
    start()
    print_can_datastructures()



