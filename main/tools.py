
from langchain_tavily import TavilySearch
from langchain_core.tools import tool


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


if __name__ == "__main__":
    package = "readis"
    get_correct_name_tool(package)