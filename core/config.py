import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_document_size_mb: int = 10
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = "llama-3.3-70b-versatile" # Powerful enough for complex RAG
    #MODEL_NAME: str = "llama-3.1-8b-instant" # More cost-effective for initial testing
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    UPLOAD_DIR: str = "data/uploads"
    CHROMA_DIR: str = "data/chromadb"
    EXPORT_DIR: str = "data/exports"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
for directory in[settings.UPLOAD_DIR, settings.CHROMA_DIR, settings.EXPORT_DIR]:
    os.makedirs(directory, exist_ok=True)