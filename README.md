# 📄 RAG Chatbot — Document Intelligence Q&A System

**A Retrieval-Augmented Generation assistant that turns uploaded documents into context-aware, conversational answers** — powered by ChromaDB, LangChain, and Groq's LLaMA 3.1 inference engine.

---

## 🎯 Overview

Traditional document search returns pages of results a user has to sift through. This system takes a different approach: users upload a PDF, and the assistant retrieves the most relevant context automatically and generates a direct, grounded answer using an LLM — with full chat history persisted for continuity.

---

## 🧩 System Design

The pipeline follows a straightforward, reliable RAG flow:

PDF Upload
↓
Text Extraction
↓
Chunking (LangChain RecursiveCharacterTextSplitter)
↓
Embedding Generation
↓
ChromaDB Vector Store (default similarity search)
↓
User Query → Semantic Retrieval of Top-K Chunks
↓
Groq LLaMA 3.1 (context-grounded generation)
↓
Response + Chat History Logged to SQLite


Each stage is deliberately kept simple and modular — the priority is reliability and low-latency response, not unnecessary architectural complexity.

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Backend Framework | FastAPI | Serves document upload, chat, and history endpoints |
| Orchestration | LangChain | Manages chunking and retrieval-augmented prompt construction |
| Chunking | `RecursiveCharacterTextSplitter` | Splits documents into fixed-size, overlapping chunks for reliable embedding |
| Vector Store | ChromaDB (default configuration) | Stores and retrieves document embeddings via built-in similarity search |
| LLM Inference | Groq (LLaMA 3.1) | Generates fast, context-grounded responses |
| Persistence | SQLite | Stores chat history for session continuity |
| Language | Python | Core application logic |

---

## ⚙️ API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/upload` | POST | Upload a PDF document for ingestion and chunking |
| `/chat` | POST | Ask a question and receive a context-grounded answer |
| `/history` | GET | Retrieve past chat history from SQLite |

---

## 🔍 Chunking & Retrieval Logic

- **Chunking:** LangChain's `RecursiveCharacterTextSplitter` splits documents using fixed chunk size and overlap values, preserving local context without cutting sentences awkwardly mid-thought.
- **Retrieval:** ChromaDB's default vector collection handles similarity search out of the box — no custom clustering or sharding is configured, keeping the setup lightweight and easy to reason about.
- **Generation:** Retrieved chunks are passed as context to Groq's LLaMA 3.1 model, chosen specifically for its high-speed inference to keep response times low.
- **Persistence:** Every chat interaction is logged to SQLite, allowing users to revisit prior questions and answers via the `/history` endpoint.

---

## 🚀 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Hetvi-pipaliya/rag-chatbot.git
cd rag-chatbot-v2

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # On macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

```bash
# 5. Run the server
uvicorn main:app --reload
```

---

## 📌 Example Usage

**Upload a PDF:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@document.pdf"
```

**Ask a question:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"message\":\"Your question here\"}"
```

**Retrieve chat history:**
```bash
curl -X GET "http://127.0.0.1:8000/history"
```

---

## 🗺️ Design Considerations & Roadmap

- **Current state:** uses ChromaDB's default similarity search, LangChain's standard recursive splitter, and SQLite for lightweight persistence — a deliberate choice to keep the system fast to build, easy to debug, and reliable for real-world document Q&A.
- **Future scope:** the modular pipeline structure allows for future upgrades such as multi-document collection management or semantic-aware chunking, without needing to redesign the core flow.

---

## 📄 License

Open for educational and portfolio use.
