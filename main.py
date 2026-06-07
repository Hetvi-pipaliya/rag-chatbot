from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import init_db, get_db, ChatHistory
from pdf_processor import extract_text_from_pdf, split_text_into_chunks
from vector_store import add_chunks_to_vectorstore
from rag_chain import get_rag_answer
import json

app = FastAPI(title="RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()

class ChatRequest(BaseModel):
    message: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        chunks = split_text_into_chunks(text)
        count = add_chunks_to_vectorstore(chunks, file.filename)
        return {"message": f"PDF uploaded!", "chunks_stored": count}
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    
@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = get_rag_answer(request.message)
    
    chat_record = ChatHistory(
        question=request.message,
        answer=result["answer"],
        sources=json.dumps(result["sources"])
    )
    db.add(chat_record)
    db.commit()
    
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).limit(10).all()