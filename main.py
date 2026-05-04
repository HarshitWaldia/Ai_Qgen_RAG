from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
import os

from core.config import settings
from core.models import GenerateRequest
from services.document_processor import DocumentProcessor
from services.vector_store import VectorStoreManager
from services.generator import PaperGenerator
from services.exporter import Exporter

app = FastAPI(title="EdTech Question Paper Generator API")
app.mount("/static", StaticFiles(directory="static"), name="static")

processor = DocumentProcessor()
vstore = VectorStoreManager()
generator = PaperGenerator()

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is healthy and running."}

@app.get("/")
async def root():
    return {"message": "Welcome to the EdTech Question Paper Generator API. Use /api/upload to upload documents and /api/generate to create question papers."}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}.pdf")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    try:
        docs = processor.extract_and_chunk(file_path)
        vstore.store_documents(doc_id, docs)
        return {"document_id": doc_id, "chunks_processed": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_paper(req: GenerateRequest):
    try:
        blueprint = generator.generate_paper(req)
        Exporter.to_docx(blueprint, req.document_id)
        Exporter.to_pdf(blueprint, req.document_id)
        
        return {
            "status": "success",
            "paper": blueprint.dict(),
            "download_urls": {
                "qp_docx": f"/api/download/{req.document_id}/qpaper.docx",
                "ak_docx": f"/api/download/{req.document_id}/answerkey.docx",
                "qp_pdf": f"/api/download/{req.document_id}/qpaper.pdf"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{doc_id}/{file_type}")
async def download_file(doc_id: str, file_type: str):
    file_path = os.path.join(settings.EXPORT_DIR, f"{doc_id}_{file_type}")
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"Generated_{file_type}")
    raise HTTPException(status_code=404, detail="File not found")