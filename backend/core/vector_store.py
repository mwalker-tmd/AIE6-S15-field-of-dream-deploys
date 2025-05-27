from backend.core.vectordatabase import VectorDatabase
from backend.core.text_utils import PDFLoader, TextFileLoader, CharacterTextSplitter
from langchain.schema.retriever import BaseRetriever
from typing import List, Dict, Any
from pydantic import Field

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance.vector_db = None
            cls._instance.splitter = CharacterTextSplitter()
        return cls._instance
    
    def __init__(self):
        # This will only run once due to the singleton pattern
        if not hasattr(self, 'vector_db'):
            self.vector_db = None
            self.splitter = CharacterTextSplitter()

    async def process_file(self, file_path: str, is_pdf: bool) -> int:
        """Process a file and store its chunks in the vector database"""
        loader = PDFLoader(file_path) if is_pdf else TextFileLoader(file_path)
        documents = loader.load_documents()
        chunks = self.splitter.split_texts(documents)

        self.vector_db = VectorDatabase()
        self.vector_db.abuild_from_list(chunks)
        return len(chunks)

    def search(self, query: str, k: int = 4):
        """Search the vector database for relevant context"""
        print(f"[DEBUG] VectorStore.search called with query: {query}")
        if self.vector_db is None:
            print("[DEBUG] VectorStore.search: vector_db is None")
            return []
        try:
            # Get search results from the vector database
            results = self.vector_db.search_by_text(query, k=k)
            print(f"[DEBUG] Raw search results: {results}")
            # Ensure we're returning a list of tuples with (text, score)
            processed_results = []
            for result in results:
                if isinstance(result, tuple) and len(result) == 2:
                    doc, score = result
                    # Fix: handle both Document and str
                    if hasattr(doc, 'page_content'):
                        processed_results.append((str(doc.page_content), score))
                    else:
                        processed_results.append((str(doc), score))
                else:
                    processed_results.append((str(result), 1.0))
            print(f"[DEBUG] Processed search results: {processed_results}")
            return processed_results
        except Exception as e:
            print(f"Error in vector store search: {e}")
            return []

    def as_retriever(self) -> BaseRetriever:
        """Convert the vector store into a LangChain retriever."""
        return VectorStoreRetriever(vector_store=self)

    @property
    def is_initialized(self) -> bool:
        """Check if the vector database has been initialized"""
        return self.vector_db is not None

    def has_content(self) -> bool:
        """Check if the vectorstore has any content."""
        try:
            # Try to get a single point from the collection
            result = self.client.scroll(
                collection_name=self.collection_name,
                limit=1
            )
            return len(result[0]) > 0
        except Exception:
            return False

    def try_initialize_from_qdrant(self):
        """Initialize vector_db from Qdrant if data exists."""
        if self.vector_db is None:
            db = VectorDatabase()
            # Try to get a single point from the collection
            try:
                result = db.client.scroll(
                    collection_name=db.collection_name,
                    limit=1
                )
                if len(result[0]) > 0:
                    print("[DEBUG] Qdrant has data, initializing vector_db.")
                    self.vector_db = db
                else:
                    print("[DEBUG] Qdrant collection is empty.")
            except Exception as e:
                print(f"[DEBUG] Error checking Qdrant content: {e}")

class VectorStoreRetriever(BaseRetriever):
    """A retriever that uses the vector store for similarity search."""
    
    vector_store: VectorStore = Field(description="The vector store to use for retrieval")
    
    def _get_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """Get documents relevant for a query."""
        print(f"[DEBUG] VectorStoreRetriever._get_relevant_documents called with query: {query}")
        if not self.vector_store.is_initialized:
            print("[DEBUG] VectorStoreRetriever: vector_store is not initialized")
            return []
            
        results = self.vector_store.search(query)
        print(f"[DEBUG] VectorStoreRetriever: search results: {results}")
        return [{"page_content": text, "metadata": {"score": score}} for text, score in results] 