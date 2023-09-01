import streamlit as st

st.title('UnblockedGPT Chatbot')

user_input = st.text_input('You: ')

if user_input:
    st.write(f'Chatbot: Hello, you said {user_input}')
