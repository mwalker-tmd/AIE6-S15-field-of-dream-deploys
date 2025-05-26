from fastapi import APIRouter, Form
from backend.agents.agent_loader import load_agent

router = APIRouter()

agent = load_agent()

@router.post("/agent", tags=["Agent"])
async def run_agent(query: str = Form(...)):
    """
    Executes the agent with the given query input.

    Parameters
    ----------
    query : str
        The input prompt or question from the user.

    Returns
    -------
    dict
        The final string response from the agent.
        Example:
        {
            "response": "You said: Hello world"
        }
    """
    result = await agent.ainvoke({"input": query})
    
    # Extract the useful part
    output = result.get("output") if isinstance(result, dict) else result

    return {"response": output}
