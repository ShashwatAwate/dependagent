
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

@tool
def get_correct_name_tool(package_name):
    """Returns a chunk of text which can have the correct package name for a pip install"""

    search_template = f"Correct package name for installing {package_name} through pip"
    try:
        search = TavilySearch(max_results = 1,tavily_api_key = os.getenv("TAVILY_API_KEY"))
        results = search.invoke(search_template)
        result_content = results["results"][0]["content"]
        result_score = results["results"][0]["score"]
        if(result_score < 0.7):
            return ""
        # print(results)
        return result_content
    except Exception as e:
        print("correct name tool exception ",str(e))
        print("exception type: ",type(e).__name__)
    return ""

@tool
def get_pypi_requirements(package_name):
    """Get requirements of a package from PyPI"""

    pypi_endpoint = f"https://pypi.org/pypi/{package_name}/json"
    try:
        res = requests.get(pypi_endpoint)
        if res.status_code==404 or res.status_code==500:
            print(f"{package_name} not found in pypi")
            return ""
        json_res = json.loads(res.text)
        requirements = json_res["info"]["requires_dist"]
        print(requirements)
        print(type(requirements))        
    except Exception as e:
        print(f"Exception at getting pypi requirements {str(e)}")
        print(f"exception type: {type(e).__name__}")

if __name__ == "__main__":
    package = "opencv-python"
    get_pypi_requirements.invoke(package)