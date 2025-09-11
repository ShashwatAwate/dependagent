from langgraph.graph import END
from langchain_core.messages import AIMessage

from main.core import State,model

import subprocess
import sys
import os
import re

def build_line_map(req_file="requirements.in"):
    with open(req_file) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    return {i+1: pkg for i, pkg in enumerate(lines)}

def parse_error(error_info: str):
    lines = error_info.splitlines()
    
    cleaned = []
    pattern = re.compile(r"requirements\.in \(line (\d+)\)")
    line_map = build_line_map()
    packages_involved = set()

    for line in lines:
        if line.strip().startswith("Traceback (most recent call last):"):
            break
        cleaned.append(line)

    err_block = []
    for line in cleaned:
        if line.strip().startswith("ERROR:"):
            err_block.append(line)
    err_block = "\n".join(err_block)
    for match in pattern.findall(err_block):
        line_no = int(match)
        pckg = line_map.get(line_no)
        if pckg:
            packages_involved.add(pckg)
    
    pkg_pattern = re.compile(r"[A-Za-z0-9_=\-]+==[^\s]+")
    for pkg in pkg_pattern.findall(err_block):
        packages_involved.add(pkg)
    
    return {
        "error": err_block,
        "packages_involved": packages_involved
    }

def build_env(state: State):
    
    """builds the environment"""

    cans = state['accepted_candidates']
    print("accepted cans at build node",state["accepted_candidates"])
    if(cans== []):
        state['messages'].append(AIMessage(content="I dont have any packages to build with! Try to look up any topic you want to work on"))
        state["next_node"] = END
        return state
    try:
        venv_name = input("what do you want to call this env?")
        if(len(venv_name)>30):
             choice = input("It is recommended you keep you environment names short, want to shorten it or continue with current name? \n(y/n)")
             if choice=='n':
                 venv_name = input("re enter your env name")
        
        
       #creating venv
        subprocess.run([sys.executable,"-m","venv",venv_name],check=True)
        venv_python = os.path.join(venv_name,"bin","python")

        if not os.path.exists(venv_python):
            venv_python = os.path.join(venv_name,"Scripts","python.exe")

        with open("requirements.in",'w') as in_file:
            for package in cans:
                in_file.write(package+"\n")
        
        try:
            result = subprocess.run(["pip-compile","requirements.in"],text=True,check=True,capture_output=True)
            print(result)
            
        except subprocess.CalledProcessError as e:
            print(f"error in pip compile: {str(e)}")
            res = parse_error(e.stderr)
            print(res)

        subprocess.run([venv_python,"-m","pip","install","-r","requirements.txt"],check=True)
        return{"python_ver":sys.version,"venv_path":venv_python}

    except Exception as e:
        print(f"Exception in building venv: {str(e)}")
        print(f"exception type {type(e)}")


if __name__ == "__main__":
    build_env(["requests==2.25.1","urllib3==2.0.0"])