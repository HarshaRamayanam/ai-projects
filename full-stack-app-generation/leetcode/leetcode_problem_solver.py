import ollama

from rich.console import Console
from rich.markdown import Markdown
from pydantic import BaseModel, Field
from typing import List

CODER_MODEL = "qwen2.5-coder:7b"
REVIEWER_MODEL = "qwen2.5-coder:7b"

console = Console()


class CoderState(BaseModel):
    """Output schema for the initial code-generation step."""

    task: str = Field(..., description="A brief restatement of the user's task")
    code: str = Field(..., description="Generated code for the given user task")
    code_explanation: str = Field(
        ..., description="A brief explanation of how the code works"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description=(
            "Any assumptions made while generating the code "
            "(e.g. libraries, versions, missing requirements)"
        ),
    )


class ReviewState(BaseModel):
    """Output schema for the code-review step."""

    reviewed_code: str = Field(
        ..., description="The final reviewed and corrected version of the code"
    )
    issues_found: List[str] = Field(
        default_factory=list,
        description="List of bugs, edge cases, or PEP8 violations identified in the original code",
    )
    changes_summary: str = Field(
        ..., description="A brief summary of the changes made during review"
    )
    approved: bool = Field(
        ..., description="Whether the original code was acceptable as-is with no changes needed"
    )


def print_markdown(content: str) -> None:
    """Render a markdown string to the console."""
    console.print(Markdown(content))


def run_coder(task: str) -> CoderState:
    """Call the coder model and return its structured output."""
    response = ollama.chat(
        model=CODER_MODEL,
        messages=[
            {"role": "user", "content": task},
        ],
        options={"temperature": 0.0},
        format=CoderState.model_json_schema(),
    )
    return CoderState.model_validate_json(response.message.content)


def run_reviewer(code: str) -> ReviewState:
    """Call the reviewer model and return its structured output."""
    reviewer_prompt = (
        "You are an expert Python developer. You will be given "
        "a python code and your task is to review it thoroughly for any hidden bugs "
        "and mishandled edge cases. Follow PEP8. Provide docstrings wherever necessary "
        "and output the final reviewed code and a brief summary of changes that you "
        "have made."
    )
    response = ollama.chat(
        model=REVIEWER_MODEL,
        messages=[
            {"role": "system", "content": reviewer_prompt},
            {"role": "user", "content": code},
        ],
        options={"temperature": 0.0},
        format=ReviewState.model_json_schema(),
    )
    return ReviewState.model_validate_json(response.message.content)


if __name__ == "__main__":

    USER_QUERY = """
    Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

Example 1:


Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]

Example 2:


Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]
 

Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000
 

Follow-up: Can you solve the problem in O(1) extra memory space?

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Write your code here
    """
    

    console.rule("[bold blue]Coder")
    coder_result = run_coder(USER_QUERY)
    console.print(f"[bold]Task:[/bold] {coder_result.task}\n")
    console.print(coder_result.code)
    if coder_result.assumptions:
        console.print("\n[bold]Assumptions:[/bold]")
        for a in coder_result.assumptions:
            console.print(f"  - {a}")

    console.rule("[bold green]Reviewer")
    review_result = run_reviewer(coder_result.code)
    console.print(review_result.reviewed_code)
    console.print(f"\n[bold]Approved as-is:[/bold] {review_result.approved}")
    if review_result.issues_found:
        console.print("\n[bold]Issues found:[/bold]")
        for issue in review_result.issues_found:
            console.print(f"  - {issue}")
    console.print(f"\n[bold]Summary of changes:[/bold] {review_result.changes_summary}")