from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PdfReader(io.BytesIO(file_bytes))
    
    full_text = ""
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n[Page {page_num + 1}]\n{text}"
    
    return full_text

def split_text_into_chunks(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    return chunks