from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
from ..core.vector_store import VectorStore
import os

# Load environment variables at module level
load_dotenv()

router = APIRouter()
vector_store = VectorStore()

# Define the RAG prompt template
RAG_PROMPT_TEMPLATE = """\
<|start_header_id|>system<|end_header_id|>
You are a helpful assistant. You answer user questions based on provided context. If you can't answer the question with the provided context, say you don't know.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
User Query:
{query}

Context:
{context}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

def get_rag_chain():
    """Create a RAG chain using the vector store and LLM."""
    if not vector_store.is_initialized:
        return None
        
    # Get the retriever from the vector store
    retriever = vector_store.as_retriever()
    
    # Initialize the HuggingFace LLM
    hf_llm = HuggingFaceEndpoint(
        endpoint_url=os.getenv("HF_LLM_ENDPOINT_URL"),
        huggingfacehub_api_token=os.getenv("HF_API_KEY"),
        task="text-generation",
        max_new_tokens=512,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        repetition_penalty=1.03,
        streaming=True
    )
    
    # Create the prompt template
    rag_prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    
    # Create the RAG chain using LCEL composition
    chain = (
        RunnablePassthrough.assign(
            context=lambda x: retriever.get_relevant_documents(x["query"])
        )
        | rag_prompt
        | hf_llm
    )
    
    return chain

@router.post("/ask")
async def query(question: str = Form(...)):
    if not vector_store.is_initialized:
        return JSONResponse(
            status_code=400, 
            content={"error": "No file uploaded yet. Please upload a file before asking questions."}
        )

    # Get the RAG chain
    rag_chain = get_rag_chain()
    if not rag_chain:
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to initialize RAG chain"}
        )

    async def response_stream():
        async for chunk in rag_chain.astream({"query": question}):
            if isinstance(chunk, str):
                yield chunk
            elif hasattr(chunk, 'content'):
                yield chunk.content
            else:
                yield str(chunk)

    return StreamingResponse(response_stream(), media_type="text/plain") 