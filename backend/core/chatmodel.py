"""
Chat model support for HuggingFace Inference Endpoints.

Includes:
- ChatModel class for RAG-style completion/streaming
"""

import os
from typing import AsyncGenerator, List, Dict, Any
from langchain_community.llms import HuggingFaceEndpoint
from langchain.schema import HumanMessage, SystemMessage

class ChatModel:
    """
    Wrapper around HuggingFace Inference Endpoints for RAG.
    Supports synchronous and asynchronous responses with streaming output.
    """

    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.endpoint_url = os.getenv("HF_LLM_ENDPOINT_URL")
        
        if not self.endpoint_url:
            raise ValueError("HF_LLM_ENDPOINT_URL environment variable is required")
        if not self.api_key:
            raise ValueError("HF_API_KEY environment variable is required")

    def _format_prompt(self, query: str, context: str = "") -> str:
        """
        Format the prompt using Llama 3 template format.
        """
        system_message = "You are a helpful AI assistant. Use the provided context to answer questions accurately and concisely."
        
        prompt = f"""<|start_header_id|>system<|end_header_id|>
{system_message}<|eot_id|>

<|start_header_id|>user<|end_header_id|>
User Query:
{query}

Context:
{context}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>"""
        
        return prompt

    def run(self, query: str, context: str = "") -> str:
        """
        Synchronously run a prompt against the chat model.
        """
        llm = HuggingFaceEndpoint(
            endpoint_url=self.endpoint_url,
            huggingfacehub_api_token=self.api_key,
            task="text-generation",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03
        )
        
        prompt = self._format_prompt(query, context)
        response = llm.invoke(prompt)
        return response

    async def astream(self, query: str, context: str = "") -> AsyncGenerator[str, None]:
        """
        Asynchronously stream response chunks for a given prompt.
        """
        llm = HuggingFaceEndpoint(
            endpoint_url=self.endpoint_url,
            huggingfacehub_api_token=self.api_key,
            task="text-generation",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            streaming=True
        )
        
        prompt = self._format_prompt(query, context)
        
        async for chunk in llm.astream(prompt):
            if isinstance(chunk, str):
                yield chunk
            elif hasattr(chunk, 'content'):
                yield chunk.content
            else:
                yield str(chunk)

def get_chat_model():
    """
    Returns a LangChain-compatible chat model for use with tools or agents.
    """
    return HuggingFaceEndpoint(
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
