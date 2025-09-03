from .core import BasicToolNode
from langchain_tavily import TavilySearch
import json
from .core import State

import os
from dotenv import load_dotenv
load_dotenv()
def get_correct_name_tool(package_name):
    search_template = f"Correct 'pip install' name for {package_name}"
    search = TavilySearch(max_results = 1,tavily_api_key = os.getenv("TAVILY_API_KEY"))
    results = search.invoke(search_template)
    print(results)



if __name__ == "__main__":
    package = "cv2"
    get_correct_name_tool(package)