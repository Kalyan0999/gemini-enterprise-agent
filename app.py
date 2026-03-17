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
    try:
        genai.configure(api_key=api_key)
        # We use the specific naming convention that Google AI Studio prefers
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask the agent about the context..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # The RAG Prompt
            full_query = f"CONTEXT:\n{context}\n\nUSER QUESTION:\n{prompt}\n\nINSTRUCTION: Answer using only the context above."
            
            with st.chat_message("assistant"):
                response = model.generate_content(full_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Agent Error: {e}")
else:
    st.info("Step 1: Paste your API Key in the sidebar. Step 2: Add context. Step 3: Ask a question!")
    
