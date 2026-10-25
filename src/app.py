import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag import ask

st.set_page_config(
    page_title="Keyestudio 4WD Robot Assistant", page_icon="🤖", layout="wide"
)

st.title("🤖 Keyestudio 4WD Robot Assistant")
st.caption("Ask anything about the Keyestudio 4WD Robot v2.0 manual")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask a question about the robot..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching manual..."):
            answer, docs = ask(question)

        st.markdown(answer)

        with st.expander("📄 Sources"):
            for d in docs:
                st.markdown(f"**Page {d['page']}** (score {d['score']})")
                st.caption(d["text"][:200] + "...")

        st.session_state.messages.append({"role": "assistant", "content": answer})
