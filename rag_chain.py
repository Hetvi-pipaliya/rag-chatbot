from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from vector_store import search_relevant_chunks
from config import settings

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model_name=settings.LLM_MODEL
)

prompt_template = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based on the context provided.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}

Answer:
""")

def get_rag_answer(question: str) -> dict:
    chunks, sources = search_relevant_chunks(question)
    
    context = "\n\n".join(chunks)
    
    chain = prompt_template | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    unique_sources = list(set([s["source"] for s in sources]))
    
    return {
        "answer": response.content,
        "sources": unique_sources
    }