import streamlit as st
from chat import chat_with_bot

st.title("Nursing College Admission Chatbot")

# Initialize session state for chat messages if not exists
if "chat_messages" not in st.session_state:
    # Don't initialize as empty list - let chat_with_bot handle initialization
    initial_response = chat_with_bot("initiate chat")

# Extract display messages (exclude system prompt)
display_messages = [msg for msg in st.session_state.chat_messages if msg["role"] != "system"]

# Display chat messages
for message in display_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_bot(prompt)
        st.markdown(response)
