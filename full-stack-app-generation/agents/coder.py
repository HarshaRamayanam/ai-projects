from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from config import CODER_MODEL
from .states import AgentState, CoderOutput

def run_coder(state: AgentState) -> dict:
    print("Generating code...")
    
    llm = ChatOllama(model=CODER_MODEL, temperature=0).with_structured_output(CoderOutput, method="json_schema")
    
    sys_message = (
        "You are an expert full-stack developer. Given an application's requirements, "
        "generate full code content for every file."
        
    )
    
    prompt = f"""
    User Task: {state.user_task}
    
    Application Requirements:
    - App Name: {state.requirements.app_name if state.requirements else 'N/A'}
    - Tech Stack: {', '.join(state.requirements.tech_stack) if state.requirements else 'N/A'}
    - Core Features: {', '.join(state.requirements.core_features) if state.requirements else 'N/A'}
    - Core Dependencies: {', '.join(state.requirements.core_dependencies) if state.requirements else 'N/A'}
    - Dev Dependencies: {', '.join(state.requirements.dev_dependencies) if state.requirements else 'N/A'}
    """
    
    response: CoderOutput = llm.invoke([
        SystemMessage(content=sys_message),
        HumanMessage(content=prompt)
    ])
    
    return {"coder_output": response}