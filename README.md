# RAG Chatbot 🤖

A simple AI-powered chatbot that answers questions from uploaded documents using Retrieval-Augmented Generation (RAG).

## Tech Stack
- **FastAPI** - REST API
- **LangChain** - RAG Pipeline
- **ChromaDB** - Vector Storage
- **Groq** - LLM (Llama 3.1)
- **SQLite** - Chat History

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd rag-chatbot-v2
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
GROQ_API_KEY=your_groq_api_key
### 5. Run the server
```bash
uvicorn main:app --reload
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload PDF file |
| `/chat` | POST | Ask a question |
| `/history` | GET | Get chat history |

## Example Usage

### Upload PDF
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@document.pdf"
```

### Ask Question
```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"message\":\"Your question here\"}"
```