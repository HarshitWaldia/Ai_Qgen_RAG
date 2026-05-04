import pdfplumber
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def extract_and_chunk(self, file_path: str) -> list[Document]:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
            
        if not text.strip():
            raise ValueError("The PDF appears to be empty or contains no extractable text.")

        chunks = self.text_splitter.split_text(text)
        return[Document(page_content=chunk) for chunk in chunks]