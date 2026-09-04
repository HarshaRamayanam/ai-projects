from langgraph.graph import START, END, StateGraph

from agents.states import AgentState
from agents.requirements_gatherer import gather_requirements
from agents.coder import run_coder

if __name__ == '__main__':
    # user_task = input("Enter your task > ").strip()
    user_task = "Online Shopping application"
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("requirements", gather_requirements)
    workflow.add_node("coder", run_coder)
    
    workflow.add_edge(START, "requirements")
    workflow.add_edge("requirements", "coder")
    workflow.add_edge("coder", END)
    
    
    app = workflow.compile()
    result = app.invoke({"user_task": user_task})
    
    print("\n--- Processed State ---")
    print("User Task:", result["user_task"])
    print("Extracted Requirements:", result["requirements"])
    print("Generated code:", result["code_files"])
    