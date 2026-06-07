import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")

# PDF Upload Section
st.sidebar.header("📄 Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.sidebar.button("Upload PDF"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post("http://127.0.0.1:8000/upload", files=files)
            if response.status_code == 200:
                st.sidebar.success(f"✅ PDF Uploaded! Chunks: {response.json()['chunks_stored']}")
            else:
                st.sidebar.error("❌ Upload failed!")

# Chat Section
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
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": prompt}
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                sources = response.json()["sources"]
                st.markdown(answer)
                st.caption(f"📚 Sources: {', '.join(sources)}")
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("❌ Error getting response!")