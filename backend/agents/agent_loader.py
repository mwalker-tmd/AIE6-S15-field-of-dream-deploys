"""
Agent loader that initializes a LangChain agent with registered tools.

This template uses the 'openai-tools' agent type. Modify as needed for different strategies
(e.g., ReAct, plan-and-execute).

TODO:
- Add memory or context handling if needed.
- Change agent type to support multi-step workflows.
"""

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from backend.tools.registry import tools

# Load environment variables at module level
load_dotenv()

def load_agent():
    """
    Create a LangChain agent instance with the registered tools.

    Returns
    -------
    Runnable
        A configured LangChain agent ready to be invoked with input.
    """
    llm = ChatOpenAI(model_name="gpt-4o-mini")  # Using same model name consistently
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_MULTI_FUNCTIONS,
        verbose=True,
    )
    return agent
