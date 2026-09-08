from langgraph.graph import START, END, StateGraph

from agents.states import AgentState, write_project_to_disk
from agents.planner import run_planner
from agents.coder import run_coder

if __name__ == '__main__':
    # user_task = input("Enter your task > ").strip()
    user_task = "A simple user login page without database dependency"
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", run_planner)
    workflow.add_node("coder", run_coder)
    
    workflow.add_edge(START, "planner")
    # workflow.add_edge("planner", END)
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", END)
    
    
    app = workflow.compile()
    
    result = app.invoke({"user_task": user_task})
    
    print("\n--- Processed State ---")
    print(result)
    # print()
    # print(result["coder_output"])
    
    print("Writing projects to disk...")
    write_project_to_disk(
        base_path=result["coder_output"].root_directory_name,
        nodes=result["coder_output"].children
    )
    print("Done writing!")