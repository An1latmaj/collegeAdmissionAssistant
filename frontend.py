import streamlit as st
from chat import chat_with_bot

st.title("Nursing College Admission Chatbot")

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial bot message
    initial_response = chat_with_bot("initiate chat")
    st.session_state.messages.append({"role": "assistant", "content": initial_response})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_bot(prompt)
        st.markdown(response)

    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
