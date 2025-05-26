# Backend Documentation

This document provides an overview of the backend architecture and components for the AI Maker Space project.

## Project Structure

```
backend/
├── agents/         # Agent definitions and implementations
├── api/            # API endpoints and routes
├── core/           # Core functionality and utilities
├── prompts/        # Prompt templates and management
├── tools/          # Tool implementations for agents
├── tests/          # Test suite
├── main.py         # Application entry point
└── .env            # Environment variables (not in repo)
```

## Core Components

### Vector Store

The `VectorStore` class in `core/vector_store.py` implements a singleton pattern for managing document embeddings and vector search functionality. It provides methods for:

- Processing and embedding documents
- Searching for relevant context based on queries
- Managing the vector database state

### Text Processing

The `text_utils.py` module provides utilities for:

- Loading documents from various formats (PDF, TXT)
- Splitting text into chunks for processing
- Text preprocessing and normalization

### Embeddings

The `embeddings.py` module handles:

- Creating embeddings for text chunks
- Managing embedding models and configurations

### Vector Database

The `vectordatabase.py` module implements:

- Storage and retrieval of vector embeddings
- Similarity search functionality
- Database management operations

## API Endpoints

The backend exposes the following API endpoints:

### Upload Endpoints

- `POST /upload/pdf` - Upload and process PDF documents
- `POST /upload/text` - Upload and process text documents

### Query Endpoints

- `POST /ask` - Query the knowledge base with a question

### Agent Endpoints

- `POST /agent/run` - Execute an agent with specific parameters

## Environment Configuration

The application uses environment variables for configuration. See `.env.template` for required variables:

- `OPENAI_API_KEY` - API key for OpenAI services
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `ENVIRONMENT` - Set to "production" or "development"
- `DEBUG` - Enable debug mode when set to "true"

## Development Setup

1. Clone the repository
2. Create a `.env` file based on `.env.template`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```
   uvicorn backend.main:app --reload
   ```

## Testing

Run the test suite with:

```
pytest
```

Tests are organized by component and include:
- API endpoint tests
- Core functionality tests
- Integration tests

## Architecture Notes

- The application uses FastAPI for the web framework
- VectorStore implements a singleton pattern to ensure a single instance across the application
- Document processing is asynchronous to handle large files efficiently
- The frontend communicates with the backend via REST API endpoints 