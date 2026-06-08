import streamlit as st
from pdf_processor import extract_text_from_pdf, split_text_into_chunks
from vector_store import add_chunks_to_vectorstore, search_relevant_chunks
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# सुधरा हुआ डार्क थीम CSS ताकि चैट का टेक्स्ट साफ़ दिखे
st.markdown("""
<style>
    /* पूरे ऐप का बैकग्राउंड */
    .stApp { background-color: #0f1117; color: #ffffff !important; }
    
    /* हेडर और बटन स्टाइल्स */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        width: 100%;
    }
    [data-testid="stSidebar"] { background-color: #1e2130; }
    
    /* चैट बॉक्स और उसके अंदर के सभी टेक्स्ट को जबरदस्ती वाइट करने के लिए */
    [data-testid="stChatMessage"] {
        background-color: #1e2130 !important;
        color: #ffffff !important;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    [data-testid="stChatMessage"] * {
        color: #ffffff !important;
    }
    
    /* सामान्य टेक्स्ट एलिमेंट्स */
    p, li, h1, h2, h3, label, span, div { color: #ffffff !important; }
    
    /* इनपुट बॉक्स का टेक्स्ट कलर फिक्स करने के लिए */
    .stChatInput textarea {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🤖 RAG Chatbot</h1>
    <p>Upload a PDF and ask questions powered by AI</p>
</div>
""", unsafe_allow_html=True)

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

st.sidebar.markdown("## 📄 Upload Document")
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.sidebar.button("🚀 Upload & Process"):
        with st.spinner("Processing PDF..."):
            file_bytes = uploaded_file.read()
            text = extract_text_from_pdf(file_bytes)
            chunks = split_text_into_chunks(text)
            count = add_chunks_to_vectorstore(chunks, uploaded_file.name)
            st.sidebar.success(f"✅ {count} chunks stored!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 How to use")
st.sidebar.markdown("1. Upload a PDF file")
st.sidebar.markdown("2. Click Upload & Process")
st.sidebar.markdown("3. Ask questions below")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Ask a question about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            chunks, sources = search_relevant_chunks(prompt)
            context = "\n\n".join(chunks)
            chain = prompt_template | llm
            response = chain.invoke({"context": context, "question": prompt})
            answer = response.content
            unique_sources = list(set([s["source"] for s in sources]))
            st.markdown(answer)
            st.caption(f"📚 Sources: {', '.join(unique_sources)}")
            st.session_state.messages.append({"role": "assistant", "content": answer})
