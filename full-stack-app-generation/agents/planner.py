from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from .states import AgentState, RequirementsOutput
from config import REQUIREMENTS_MODEL

def run_planner(state: AgentState) -> dict:
    """Takes raw user input and outputs a structured user requirements"""
    print("Gathering requirements...")
    llm = ChatOllama(model=REQUIREMENTS_MODEL, temperature=0).with_structured_output(RequirementsOutput)
    
    sys_message = (
        "You are given a vague task for creating a full-stack application with Next.js. "
        "Analyze the user task and extract minimal structured requirements. Also generate "
        "core dependencies and dev dependencies along with node package version numbers instead"
        " of `latest`"
    )
    
    response = llm.invoke([
        SystemMessage(content=sys_message),
        HumanMessage(content=state.user_task)
    ])
    
    print(response)
    
    return {"requirements": response}