import streamlit as st
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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" 

def get_groq_response(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": messages,
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response found.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Groq API: {e}"
    except KeyError:
        return "Unexpected response format from the API."

st.title("AI Chatbot")
st.subheader("Ask anything, and I will try my best to help!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", key="user_input", placeholder="Type your question here...")
    submit_button = st.form_submit_button("Send")

if submit_button:
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        messages = st.session_state.chat_history
        bot_response = get_groq_response(messages)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    else:
        st.warning("Please enter a message!")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"_Bot:_ {message['content']}")
