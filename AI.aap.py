import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Pathshala", layout="centered")

# API Key Check
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key नहीं मिली! कृपया Streamlit Settings -> Secrets में GEMINI_API_KEY सेट करें।")
    st.stop()

client = genai.Client(api_key=api_key)

# Session State
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model="gemini-1.5-flash")
    st.session_state.messages = []

st.title("AI Pathshala - Gemini Chat Assistant")

# Show history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("अपना सवाल यहाँ टाइप करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})