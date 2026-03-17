import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖")
st.title("📂 Enterprise Knowledge Agent")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("---")
    context = st.text_area("Enterprise Knowledge Base:", 
                           placeholder="Paste company policies or data here...",
                           height=300)

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # This is the most stable way to call the model currently
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Providing the context directly in the prompt
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
            
            with st.chat_message("assistant"):
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please enter your Gemini API Key in the sidebar.")
    
