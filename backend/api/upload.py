from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile, shutil, os
from backend.core.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    suffix = f".{file.filename.split('.')[-1]}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        file_path = temp_file.name

    try:
        chunks = await vector_store.process_file(
            file_path, 
            is_pdf=file.filename.endswith(".pdf")
        )
        return JSONResponse({
            "message": f"{file.filename} processed", 
            "chunks": chunks
        })
    finally:
        os.unlink(file_path) 