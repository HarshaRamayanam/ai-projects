import os

from pydantic import BaseModel, Field
from typing import List, Literal, Union

class RequirementsOutput(BaseModel):
    app_name: str = Field(description="Suggested name for the application")
    tech_stack: list[str] = Field(description="Key technologies needed")
    core_features: list[str] = Field(description="Key functional requirements")
    api_endpoints: list[str] = Field(description="Key API endpoints")
    core_dependencies: list[str] = Field(default_factory=list, description="Key core dependencies")
    dev_dependencies: list[str] = Field(default_factory=list, description="Key dev dependencies")

# ===============================================================================================================

class FileNode(BaseModel):
    type: Literal["file"] = "file"
    name: str = Field(description="Filename with extension, e.g., 'App.tsx' or 'package.json'")
    content: str = Field(description="Complete source code or contents of the file")

class DirectoryNode(BaseModel):
    type: Literal["directory"] = "directory"
    name: str = Field(description="Directory name, e.g., 'src' or 'components'")
    # Discrimination / Union allowing recursive nesting
    children: List[Union["DirectoryNode", FileNode]] = Field(
        default_factory=list,
        description="Contents of this directory (files or subdirectories)"
    )

# Enable recursive references in Pydantic v2
DirectoryNode.model_rebuild()


class CoderOutput(BaseModel):
    root_directory_name: str = Field(description="Root project name, e.g., 'my-fullstack-app'")
    children: List[Union[DirectoryNode, FileNode]] = Field(
        description="Root level files and directories"
    )

# ===============================================================================================================
    
# This the common state used by langgraph
class AgentState(BaseModel):
    user_task: str = Field(description="A brief description of the user task")
    requirements: RequirementsOutput | None = Field(default=None, description="Structured requirements output")
    coder_output: CoderOutput | None = Field(default=None, description="Structured code output")


def write_project_to_disk(base_path: str, nodes: List[Union[DirectoryNode, FileNode]]):
    for node in nodes:
        node_path = os.path.join(base_path, node.name)
        if isinstance(node, DirectoryNode) or node.type == "directory":
            os.makedirs(node_path, exist_ok=True)
            # Recurse through subdirectories
            write_project_to_disk(node_path, node.children)
        else:
            os.makedirs(os.path.dirname(node_path), exist_ok=True)
            with open(node_path, "w", encoding="utf-8") as f:
                f.write(node.content)