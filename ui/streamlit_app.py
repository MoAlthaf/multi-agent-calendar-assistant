import os
import uuid

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("SCHEDULEME_API_URL", "http://localhost:8000/api/v1")
REQUEST_TIMEOUT = 60

st.set_page_config(page_title="ScheduleMe", page_icon="📅", layout="centered")
st.title("📅 ScheduleMe")
st.markdown("Natural language calendar assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button("New chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    st.caption(f"Thread: `{st.session_state.thread_id[:8]}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your request...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                resp = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": user_input,
                        "thread_id": st.session_state.thread_id,
                    },
                    timeout=REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                reply = resp.json()["reply"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except requests.exceptions.ConnectionError:
                error_msg = f"❌ Cannot reach backend at {API_URL}. Is the FastAPI server running?"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.Timeout:
                error_msg = f"❌ Backend timed out after {REQUEST_TIMEOUT}s."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.HTTPError as e:
                error_msg = f"❌ Backend returned {e.response.status_code}: {e.response.text}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
