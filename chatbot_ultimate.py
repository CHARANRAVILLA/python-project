import streamlit as st
from transformers import pipeline
from datetime import datetime

st.set_page_config(page_title="🧠 AI ChatBot - Web")

st.title("💬 Ultimate ChatBot (Web Only)")

@st.cache_resource
def load_bot():
    return pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)

bot = load_bot()

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="input")

if user_input:
    with st.spinner("Thinking..."):
        result = bot(user_input)[0]["generated_text"]
        reply = result.strip()

        st.session_state.chat_history.append({"user": user_input, "bot": reply})
        st.success("🤖: " + reply)

st.markdown("### 📝 Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")

if st.button("💾 Save Chat"):
    filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    text = "\n".join([f"You: {c['user']}\nBot: {c['bot']}\n" for c in st.session_state.chat_history])
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    st.success(f"Saved as {filename}")

