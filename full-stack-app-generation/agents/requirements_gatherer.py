from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from .states import AgentState, RequirementsOutput
from config import REQUIREMENTS_MODEL

def gather_requirements(state: AgentState) -> dict:
    print("Gathering requirements...")
    llm = ChatOllama(model=REQUIREMENTS_MODEL, temperature=0).with_structured_output(RequirementsOutput)
    
    sys_message = (
        "You are given a vague task for creating a full-stack application. "
        "Analyze the user task and extract minimal structured requirements."
    )
    
    response = llm.invoke([
        SystemMessage(content=sys_message),
        HumanMessage(content=state.user_task)
    ])
    
    return {"requirements": response}