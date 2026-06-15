import streamlit as st
from google import genai

st.set_page_config(page_title="AI Pathshala")

api_key = st.secrets.get("GEMINI_API_KEY")

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

if "chat_session" not in st.session_state:
    # आपने कहा तो मैंने यहाँ 3.5-flash लगा दिया है
    try:
        st.session_state.chat_session = st.session_state.client.chats.create(model="gemini-3.5-flash")
        st.session_state.messages = []
    except Exception as e:
        st.error(f"मॉडल एरर: {e}")
        st.info("प्रो टिप: अगर यह एरर दे, तो 'gemini-1.5-flash' का उपयोग करें, क्योंकि 3.5 अभी सभी के लिए पूरी तरह फ्री उपलब्ध नहीं हो सकता है।")
        st.stop()

st.title("AI Pathshala")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("अपना सवाल लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("लिमिट खत्म हो गई है या मॉडल एक्सेस नहीं है।")
