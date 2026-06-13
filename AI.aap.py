import os
import threading
from flask import Flask, render_template, request, jsonify
from google import genai
from google.colab import userdata
from google.colab.output import eval_js

# 1. ऑटोमैटिक templates फ़ोल्डर और HTML फ़ाइल बनाना
os.makedirs('templates', exist_ok=True)

html_code = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat Box</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white font-sans h-screen flex flex-col justify-between">
    <header class="bg-gray-800 p-4 text-center text-xl font-bold border-b border-gray-700 text-blue-400">
        AI Pathshala - Gemini Chat Assistant
    </header>
    <div id="chat-box" class="flex-1 p-6 overflow-y-auto space-y-4 max-w-3xl w-full mx-auto">
        <div class="text-left">
            <span class="bg-gray-800 text-gray-300 px-4 py-2 rounded-lg inline-block border border-gray-700">
                नमस्ते! मैं मेमोरी वाला जेमिनी एआई हूँ। बताइए, आज हम क्या सीखने वाले हैं?
            </span>
        </div>
    </div>
    <div class="p-4 bg-gray-800 border-t border-gray-700">
        <div class="max-w-3xl mx-auto flex gap-3">
            <input id="user-input" type="text" placeholder="अपना सवाल यहाँ टाइप करें..." 
                   class="flex-1 p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-600">
            <button onclick="sendMessage()" class="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-bold">
                भेजें
            </button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const inputEl = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const message = inputEl.value.trim();
            if (!message) return;

            chatBox.innerHTML += `<div class="text-right"><span class="bg-blue-600 text-white px-4 py-2 rounded-lg inline-block text-left max-w-md">${message}</span></div>`;
            inputEl.value = '';
            
            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div id="${loadingId}" class="text-left"><span class="bg-gray-800 text-gray-400 px-4 py-2 rounded-lg inline-block italic">सोच रहा हूँ...</span></div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await axios.post('/chat', { message: message });
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="text-left"><span class="bg-gray-800 text-gray-200 px-4 py-2 rounded-lg inline-block border border-gray-700 max-w-md whitespace-pre-line">${response.data.reply}</span></div>`;
            } catch (error) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="text-left"><span class="bg-red-900 text-red-200 px-4 py-2 rounded-lg inline-block">त्रुटि: सर्वर से जवाब नहीं मिला।</span></div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

# 2. फ्लैस्क सर्वर और जेमिनी मेमोरी सेटअप (नए मॉडल नाम के साथ)
app = Flask(__name__)

API_KEY = userdata.get('GEMINI_API_KEY')
client = genai.Client(api_key=API_KEY)
chat_session = None

@app.route('/')
def index():
    global chat_session
    # यहाँ हमने मॉडल का नाम बदल दिया है
    chat_session = client.chats.create(model="gemini-3.5-flash")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_session
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'reply': 'कृपया संदेश लिखें।'})
        
    if chat_session is None:
        chat_session = client.chats.create(model="gemini-3.5-flash")

    try:
        response = chat_session.send_message(user_message)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

threading.Thread(target=run_flask).start()

# लाइव लिंक जनरेट करना
print("\n✓ एरर फिक्स हो गई है! नीचे दिए गए नए लिंक पर क्लिक करें:")
print(eval_js("google.colab.kernel.proxyPort(5000)"))