"""
Embedding model provider used by the vector database.

This implementation uses HuggingFace Inference Endpoints for embeddings.

TODO:
- Customize model name or add conditional logic for different providers.
- Add error handling or caching if needed.
"""

import os
from langchain_huggingface import HuggingFaceEndpointEmbeddings

class EmbeddingProvider:
    """
    Handles generation of vector embeddings using HuggingFace Inference Endpoints.
    
    Attributes
    ----------
    model : HuggingFaceEndpointEmbeddings
        An instance of the HuggingFace embeddings model.
    """

    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.endpoint_url = os.getenv("HF_EMBEDDING_ENDPOINT_URL")
        
        if not self.endpoint_url:
            raise ValueError("HF_EMBEDDING_ENDPOINT_URL environment variable is required")
        if not self.api_key:
            raise ValueError("HF_API_KEY environment variable is required")
            
        self.model = HuggingFaceEndpointEmbeddings(
            model=self.endpoint_url,
            task="feature-extraction",
            huggingfacehub_api_token=self.api_key
        )

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
