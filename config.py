from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "documents"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    LLM_MODEL: str = "llama-3.1-8b-instant"
    DATABASE_URL: str = "sqlite:///./chat_history.db"

settings = Settings()