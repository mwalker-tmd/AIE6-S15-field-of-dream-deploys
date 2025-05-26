from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ..core.vector_store import VectorStore
from ..prompts.prompt_manager import PromptManager

# Load environment variables at module level
load_dotenv()

router = APIRouter()
llm = ChatOpenAI(model_name="gpt-4o-mini")  # Using LangChain's ChatOpenAI
vector_store = VectorStore()
prompt_manager = PromptManager()

@router.post("/ask")
async def query(question: str = Form(...)):
    if not vector_store.is_initialized:
        return JSONResponse(
            status_code=400, 
            content={"error": "No file uploaded yet. Please upload a file before asking questions."}
        )

    context_list = vector_store.search(question)
    context_prompt = "\n".join([ctx[0] for ctx in context_list])
    messages = prompt_manager.create_messages(question, context_prompt)

    async def response_stream():
        async for chunk in llm.astream(messages):
            # Extract the text content from the AIMessageChunk
            if hasattr(chunk, 'content'):
                yield chunk.content
            else:
                # Fallback if the chunk doesn't have a content attribute
                yield str(chunk)

    return StreamingResponse(response_stream(), media_type="text/plain") 