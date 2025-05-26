"""
Tool registry for the agent. Add tools here to make them available to your agent's toolbox.
"""

from langchain.tools import Tool
from backend.tools.dummy_tool import echo_tool

tools = [
    Tool(
        name="echo",
        func=echo_tool,
        description="Repeats back what the user says. Used as a template tool."
    )
]

# TODO: Add additional tools here as needed
