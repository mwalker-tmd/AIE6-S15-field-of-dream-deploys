"""
Chat model support.

Includes:
- ChatModel class for basic RAG-style completion/streaming
- get_chat_model() for LangChain-compatible usage with agents
"""

import os
import openai
from langchain_openai import ChatOpenAI

class ChatModel:
    """
    Simple wrapper around OpenAI ChatCompletion for non-agent use (RAG).

    Supports synchronous and asynchronous responses with streaming output.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, prompt: str) -> str:
        """
        Synchronously run a prompt against the chat model.
        """
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message["content"]

    async def astream(self, prompt: str):
        """
        Asynchronously stream response chunks for a given prompt.
        """
        openai.api_key = self.api_key
        response = await openai.ChatCompletion.acreate(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.get("content"):
                yield chunk.choices[0].delta.content

def get_chat_model():
    """
    Returns a LangChain-compatible chat model for use with tools or agents.
    """
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=0,
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )
