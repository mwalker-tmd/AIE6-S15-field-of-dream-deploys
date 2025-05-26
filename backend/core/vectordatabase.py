"""
Vector database handler for storing and retrieving text chunks using embeddings.

TODO:
- Replace in-memory store with a persistent backend (e.g., FAISS, Pinecone).
- Customize embedding provider as needed.
"""

from langchain_community.vectorstores import FAISS
from backend.core.embeddings import EmbeddingProvider

class VectorDatabase:
    """
    Handles the creation and querying of a vector database using text embeddings.
    """

    def __init__(self):
        self.db = None
        self.embedding_provider = EmbeddingProvider()

    async def abuild_from_list(self, chunks):
        """
        Build the vector database from a list of text chunks.

        Parameters
        ----------
        chunks : list of str
            The list of preprocessed text segments.
        """
        self.db = FAISS.from_texts(texts=chunks, embedding=self.embedding_provider.model)

    def search_by_text(self, query, k=4):
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
            List of matched chunks with relevance metadata.
        """
        if self.db is None:
            raise ValueError("Vector database is not initialized.")
        return self.db.similarity_search_with_score(query, k=k)
