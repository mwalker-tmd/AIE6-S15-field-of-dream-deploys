"""
Embedding model provider used by the vector database.

This template implementation uses OpenAI's embedding model.
To swap providers (e.g., Hugging Face, Cohere), modify or extend this class.

TODO:
- Customize model name or add conditional logic for different providers.
- Add error handling or caching if needed.
"""

import os
from langchain_community.embeddings import OpenAIEmbeddings

class EmbeddingProvider:
    """
    Handles generation of vector embeddings using a pluggable backend.
    
    Attributes
    ----------
    model : BaseEmbedding
        An instance of a LangChain-compatible embedding model.
    """

    def __init__(self):
        model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
        self.model = OpenAIEmbeddings(model=model_name)

    def embed_documents(self, texts):
        """
        Generate vector embeddings for a list of text chunks.

        Parameters
        ----------
        texts : list of str
            The list of text passages to embed.

        Returns
        -------
        list of list of float
            The generated embedding vectors.
        """
        return self.model.embed_documents(texts)

    def embed_query(self, query):
        """
        Generate an embedding for a single query string.

        Parameters
        ----------
        query : str
            The query to embed.

        Returns
        -------
        list of float
            The embedding vector.
        """
        return self.model.embed_query(query)
