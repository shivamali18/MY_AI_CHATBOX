import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Pathshala", layout="centered")

# API Key Check
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key नहीं मिली! कृपया Streamlit Settings -> Secrets में GEMINI_API_KEY सेट करें।")
    st.stop()

# --- बदलाव यहाँ है: Client को session_state में डालें ---
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

# Session State में चैट हिस्ट्री और सेशन रखें
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.client.chats.create(model="gemini-1.5-flash")
    st.session_state.messages = []

st.title("AI Pathshala - Gemini Chat Assistant")

# पुरानी चैट दिखाएं
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# यूजर का इनपुट
if prompt := st.chat_input("अपना सवाल यहाँ टाइप करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini का रिस्पॉन्स
    with st.chat_message("assistant"):
        # यहाँ अब session_state वाले client का उपयोग होगा
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})