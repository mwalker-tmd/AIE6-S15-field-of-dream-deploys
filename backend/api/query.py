from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
from ..core.vector_store import VectorStore
from ..core.chatmodel import ChatModel
import os
import json
import re

# Load environment variables at module level
load_dotenv()

router = APIRouter()
vector_store = VectorStore()
chat_model = ChatModel()

# Define the RAG prompt template
RAG_PROMPT_TEMPLATE = """\
<|start_header_id|>system<|end_header_id|>
You are a helpful assistant. You answer user questions based on provided context. 
If no context is provided or if the context is empty, respond with: "I don't have any documents loaded to answer your question. Please upload some documents first."
If you can't answer the question with the provided context, say you don't know.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
User Query:
{query}

Context:
{context}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

# Utility to clean up hallucinated or special tokens from model output
def clean_response(text):
    # Remove only the specific hallucinated tokens
    start_pos = text.find('<|eot_id|>')
    if start_pos != -1:
        text = text[:start_pos]
    return text

def get_rag_chain():
    """Create a RAG chain using the vector store and LLM."""
    vector_store.try_initialize_from_qdrant()  # Ensure vector_db is initialized if Qdrant has data
    if not vector_store.is_initialized:
        return None
        
    # Get the retriever from the vector store
    retriever = vector_store.as_retriever()
    
    # Initialize the HuggingFace LLM
    hf_llm = HuggingFaceEndpoint(
        endpoint_url=os.getenv("HF_LLM_ENDPOINT_URL"),
        huggingfacehub_api_token=os.getenv("HF_API_KEY"),
        task="text-generation",
        max_new_tokens=256,
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

@router.get("/status")
async def get_status():
    """Check if the vectorstore has any content."""
    return {
        "has_content": vector_store.is_initialized and vector_store.has_content()
    }

@router.post("/ask")
async def query(question: str = Form(...)):
    print(f"[DEBUG] Received question: {question}")
    try:
        # Get the RAG chain
        vector_store.try_initialize_from_qdrant()  # Ensure vector_db is initialized if Qdrant has data
        if not vector_store.is_initialized:
            # If no vector store, return empty context message
            response = chat_model.run(question, "")
            return JSONResponse(content={"response": clean_response(response)})

        # Get relevant context from vector store
        results = vector_store.search(question)
        context = "\n".join([text for text, _ in results])

        async def response_stream():
            try:
                async for chunk in chat_model.astream(question, context):
                    cleaned = clean_response(chunk)
                    if cleaned:
                        yield cleaned
            except Exception as e:
                # Send error as a JSON chunk
                error_msg = json.dumps({"error": str(e)})
                yield error_msg

        return StreamingResponse(
            response_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        ) 