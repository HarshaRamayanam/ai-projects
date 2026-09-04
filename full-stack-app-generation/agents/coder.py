from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from config import CODER_MODEL
from .states import AgentState, CodebaseOutput

def run_coder(state: AgentState) -> dict:
    print("Generating code...")
    
    llm = ChatOllama(model=CODER_MODEL, temperature=0).with_structured_output(CodebaseOutput)
    
    sys_message = (
        "You are an expert full-stack developer. Given an application's requirements, "
        "generate all essential source code files with accurate paths and complete implementations."
    )
    
    prompt = f"""
    User Task: {state.user_task}
    
    Application Requirements:
    - App Name: {state.requirements.app_name if state.requirements else 'N/A'}
    - Tech Stack: {', '.join(state.requirements.tech_stack) if state.requirements else 'N/A'}
    - Core Features: {', '.join(state.requirements.core_features) if state.requirements else 'N/A'}
    """
    
    response: CodebaseOutput = llm.invoke([
        SystemMessage(content=sys_message),
        HumanMessage(content=prompt)
    ])
    
    return {"code_files": response.files}