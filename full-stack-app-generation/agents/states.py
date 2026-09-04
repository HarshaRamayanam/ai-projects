from pydantic import BaseModel, Field

class RequirementsOutput(BaseModel):
    app_name: str = Field(description="Suggested name for the application")
    tech_stack: list[str] = Field(description="Key technologies needed")
    core_features: list[str] = Field(description="Key functional requirements")

# ===============================================================================================================

class CoderOutput(BaseModel):
    component_file_name: str = Field(description="Component file name (e.g., auth.js)")
    component_file_location: str = Field(description="Directory path relative to root (e.g., src/routes)")
    code: str = Field(description="Fully functional runnable code snippet")

class CodebaseOutput(BaseModel):
    files: list[CoderOutput] = Field(description="List of generated code files for the full-stack application")
    
# ===============================================================================================================
    
# This the common state used by langgraph
class AgentState(BaseModel):
    user_task: str = Field(description="A brief description of the user task")
    requirements: RequirementsOutput | None = Field(default=None, description="Structured requirements output")
    code_files: list[CoderOutput] = Field(default_factory=list, description="List of generated code files")