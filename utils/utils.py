import json
import re

def res_to_json(content: str) -> json:
    try:
        pattern = r"```json(.*?)```"
        matches = re.findall(pattern,content,re.DOTALL)
        for m in matches:
            json_res = json.loads(m)
            return json_res
    except Exception as e:
        print(f"res_to_json exception:{str(e)}")
        print(f"exception type: {type(e).__name__}")
        return None
    
