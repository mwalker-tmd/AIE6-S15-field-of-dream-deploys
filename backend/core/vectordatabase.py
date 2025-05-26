"""
Vector database handler for storing and retrieving text chunks using Qdrant.
"""

from typing import List, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from backend.core.embeddings import EmbeddingProvider
import os

class VectorDatabase:
    """
    Handles the creation and querying of a vector database using Qdrant.
    """

    def __init__(self):
        self.embedding_provider = EmbeddingProvider()
        self.collection_name = "s15-field-of-dreams"
        self.vector_size = 1536  # OpenAI embedding dimension
        
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        # Create collection if it doesn't exist
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists in Qdrant."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    async def abuild_from_list(self, chunks: List[str]):
        """
        Build the vector database from a list of text chunks.

        Parameters
        ----------
        chunks : list of str
            The list of preprocessed text segments.
        """
        # Generate embeddings for all chunks
        embeddings = self.embedding_provider.model.embed_documents(chunks)
        
        # Prepare points for upload
        points = []
        for i, (text, embedding) in enumerate(zip(chunks, embeddings)):
            points.append(models.PointStruct(
                id=i,
                vector=embedding,
                payload={"text": text}
            ))
        
        # Upload points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search_by_text(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        """
        Search the vector database for the most relevant chunks based on the query.

        Parameters
        ----------
        query : str
            The user's input question or topic.
        k : int, optional
            The number of top matches to return (default is 4).

        Returns
        -------
        list of tuple
            List of matched chunks with relevance scores.
        """
        # Generate embedding for the query
        query_embedding = self.embedding_provider.model.embed_query(query)
        
        # Search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k
        )
        
        # Format results
        results = []
        for scored_point in search_result:
            text = scored_point.payload["text"]
            score = scored_point.score
            results.append((text, score))
        
        return results
