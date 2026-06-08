import streamlit as st
from pdf_processor import extract_text_from_pdf, split_text_into_chunks
from vector_store import add_chunks_to_vectorstore, search_relevant_chunks
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

prompt_template = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based on the context provided.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:
""")

# PDF Upload
st.sidebar.header("📄 Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.sidebar.button("Upload PDF"):
        with st.spinner("Processing..."):
            file_bytes = uploaded_file.read()
            text = extract_text_from_pdf(file_bytes)
            chunks = split_text_into_chunks(text)
            count = add_chunks_to_vectorstore(chunks, uploaded_file.name)
            st.sidebar.success(f"✅ Done! {count} chunks stored!")

# Chat
st.header("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chunks, sources = search_relevant_chunks(prompt)
            context = "\n\n".join(chunks)
            chain = prompt_template | llm
            response = chain.invoke({"context": context, "question": prompt})
            answer = response.content
            unique_sources = list(set([s["source"] for s in sources]))
            st.markdown(answer)
            st.caption(f"📚 Sources: {', '.join(unique_sources)}")
            st.session_state.messages.append({"role": "assistant", "content": answer})