"""
Chat model support.

Includes:
- ChatModel class for basic RAG-style completion/streaming
- get_chat_model() for LangChain-compatible usage with agents
"""

import os
from typing import AsyncGenerator, List, Dict, Any
from langchain_community.llms import HuggingFaceEndpoint
from langchain.callbacks.streaming import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, SystemMessage

class ChatModel:
    """
    Simple wrapper around HuggingFace Inference Endpoints for RAG.

    Supports synchronous and asynchronous responses with streaming output.
    """

    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.endpoint_url = os.getenv("HF_LLM_ENDPOINT_URL")
        
        if not self.endpoint_url:
            raise ValueError("HF_LLM_ENDPOINT_URL environment variable is required")
        if not self.api_key:
            raise ValueError("HF_API_KEY environment variable is required")

    def run(self, prompt: str) -> str:
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
        
        messages = [
            SystemMessage(content="You are a helpful AI assistant. Use the provided context to answer questions accurately and concisely."),
            HumanMessage(content=prompt)
        ]
        
        response = llm.invoke(messages)
        return response

    async def astream(self, prompt: str) -> AsyncGenerator[str, None]:
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
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        messages = [
            SystemMessage(content="You are a helpful AI assistant. Use the provided context to answer questions accurately and concisely."),
            HumanMessage(content=prompt)
        ]
        
        async for chunk in llm.astream(messages):
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
