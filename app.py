import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖")
st.title("📂 Enterprise Knowledge Agent")

# Sidebar
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("---")
    
    # NEW: PDF Uploader
    uploaded_file = st.file_uploader("Upload Company Policy (PDF)", type="pdf")
    
    # Manual context fallback
    manual_context = st.text_area("Or Paste Text Here:", height=200)

# Helper function to read PDF
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Auto-detect best model
        if "model_name" not in st.session_state:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.session_state.model_name = next((m for m in models if "flash" in m), models[0])
        
        model = genai.GenerativeModel(st.session_state.model_name)

        # Determine which context to use
        context = ""
        if uploaded_file:
            context = get_pdf_text(uploaded_file)
            st.sidebar.success("PDF Loaded Successfully!")
        else:
            context = manual_context

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # UI: Clear Chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about the documents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            full_prompt = f"Using ONLY this context: {context}\n\nQuestion: {prompt}"
            
            with st.chat_message("assistant"):
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter your API Key in the sidebar to start.")
    
