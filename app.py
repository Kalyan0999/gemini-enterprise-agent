import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖")
st.title("📂 Enterprise Knowledge Agent")

# Sidebar for API Key and Context
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("---")
    context = st.text_area("Enterprise Knowledge Base:", 
                           placeholder="Paste company policies or data here...",
                           height=300)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask the agent about the context..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Grounding the AI with the context provided
        full_query = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer using only the context provided."
        
        with st.chat_message("assistant"):
            response = model.generate_content(full_query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("Please enter your Gemini API Key in the sidebar to begin.")
  
