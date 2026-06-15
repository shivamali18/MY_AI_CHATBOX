import streamlit as st
from google import genai

# 1. पेज सेटअप
st.set_page_config(page_title="AI Pathshala", layout="centered")

# 2. API Key का सुरक्षित उपयोग
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key नहीं मिली! कृपया Streamlit Settings -> Secrets में GEMINI_API_KEY डालें।")
    st.stop()

# 3. Client को Session State में सुरक्षित करना
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

# 4. चैट सेशन शुरू करना
if "chat_session" not in st.session_state:
    # यहाँ हमने मॉडल का नाम बदल दिया है जैसा आपने कहा था
    st.session_state.chat_session = st.session_state.client.chats.create(model="gemini-2.0-flash")
    st.session_state.messages = []

# 5. UI बनाना
st.title("AI Pathshala - Gemini Chat Assistant")

# पुरानी चैट हिस्ट्री दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. चैट इनपुट और रिस्पॉन्स हैंडलिंग
if prompt := st.chat_input("अपना सवाल यहाँ टाइप करें..."):
    # यूजर का मैसेज स्क्रीन पर दिखाना
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # एआई का जवाब (Error Handling के साथ)
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"क्षमा करें, एरर आ गया: {e}")
