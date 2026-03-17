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
        # Configuration
        genai.configure(api_key=api_key)
        
        # FIX: We use 'gemini-1.5-flash' directly. 
        # The library handles the 'models/' prefix internally.
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about the policy..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Constructing the RAG Prompt
            # We add a clear instruction to ensure it uses the context
            full_query = f"Use the following context to answer the question.\n\nContext: {context}\n\nQuestion: {prompt}"
            
            with st.chat_message("assistant"):
                # Calling the model
                response = model.generate_content(full_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # If gemini-1.5-flash fails, let's try the older gemini-pro automatically
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(full_query)
            st.markdown(response.text)
        except:
            st.error(f"Agent Error: {e}")
else:
    st.info("Please enter your API Key to begin.")
    
