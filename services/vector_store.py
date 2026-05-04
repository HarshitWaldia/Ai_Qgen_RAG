import os
# FIXED: Disables ChromaDB telemetry which was causing the capture() error in your logs
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# FIXED: Using the new updated langchain_chroma package
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import settings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.persist_directory = settings.CHROMA_DIR

    def store_documents(self, document_id: str, docs: list):
        # We use the document_id as the collection name to isolate contexts
        Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            collection_name=document_id,
            persist_directory=self.persist_directory
        )

    def get_retriever(self, document_id: str, k: int = 5):
        db = Chroma(
            collection_name=document_id,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        return db.as_retriever(search_kwargs={"k": k})