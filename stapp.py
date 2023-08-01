
# Internal usage
from time import  sleep
#### IMPORTS FOR AI PIPELINES 
import requests 
import streamlit as st

#AVATARS
av_us = './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = './lamini.png'

# FUNCTION TO LOG ALL CHAT MESSAGES INTO chathistory.txt
def writehistory(text):
    with open('chathistory.txt', 'a') as f:
        f.write(text)
        f.write('\n')
    f.close()


st.title("🦙 LaMiniGPT ChatBot")
st.subheader("Using model LaMini-Flan-T5-77M")
repo="MBZUAI/LaMini-Flan-T5-77M"

# Set a default model
if "hf_model" not in st.session_state:
    st.session_state["hf_model"] = "MBZUAI/LaMini-Flan-T5-77M"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])

# Accept user input
if myprompt := st.chat_input("What can you do for me?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(usertext)
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=av_ass):
        message_placeholder = st.empty()
        full_response = ""
        apiresponse = requests.get(f'http://127.0.0.1:8000/lamini?question={myprompt}')
        risposta = apiresponse.content.decode("utf-8")
        res  =  risposta[1:-1]
        response = res.split(" ")
        for r in response:
            full_response = full_response + r + " "
            message_placeholder.markdown(full_response + "▌")
            sleep(0.1)
        message_placeholder.markdown(full_response)
        asstext = f"assistant: {full_response}"
        writehistory(asstext)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
