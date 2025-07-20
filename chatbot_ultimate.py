import streamlit as st
from transformers import pipeline
from datetime import datetime
import pyttsx3
import speech_recognition as sr

st.set_page_config(page_title="🧠 AI ChatBot Ultimate")

st.title("💬 Ultimate ChatBot (Local + Free + Voice + Save)")

# Text-to-Speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load smarter model
@st.cache_resource
def load_bot():
    return pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)

bot = load_bot()

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Voice input function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Couldn't understand you.")
    except sr.RequestError:
        st.error("Speech service not available.")
    return ""

# Input UI
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("You:", key="input")
with col2:
    if st.button("🎤 Voice"):
        user_input = listen()

# Chat handling
if user_input:
    with st.spinner("Thinking..."):
        # Just send user_input for FLAN
        result = bot(user_input)[0]["generated_text"]
        reply = result.strip()

        st.session_state.chat_history.append({"user": user_input, "bot": reply})
        st.success("🤖: " + reply)
        speak(reply)

# Show full chat history
st.markdown("### 📝 Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")

# Save button
if st.button("💾 Save Chat"):
    filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    text = "\n".join([f"You: {c['user']}\nBot: {c['bot']}\n" for c in st.session_state.chat_history])
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    st.success(f"Saved as {filename}")
