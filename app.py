import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖")
st.title("📂 Enterprise Knowledge Agent")

with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("---")
    context = st.text_area("Enterprise Knowledge Base:", height=300)

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # FIX: Instead of hardcoding a name that might be 'Not Found', 
        # we find the first available model on your account that supports chat.
        if "model_name" not in st.session_state:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Prioritize Gemini 2.0 or 1.5 if available
            st.session_state.model_name = next((m for m in available_models if "flash" in m), available_models[0])
        
        model = genai.GenerativeModel(st.session_state.model_name)
        st.caption(f"Connected to: {st.session_state.model_name}")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            full_prompt = f"Using ONLY this context: {context}\n\nQuestion: {prompt}"
            
            with st.chat_message("assistant"):
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Agent Error: {e}")
        st.button("Clear Cache & Retry", on_click=lambda: st.session_state.clear())
else:
    st.info("Paste your API Key in the sidebar to start.")
    
