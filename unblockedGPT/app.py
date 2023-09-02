import streamlit as st
import requests
import openai

# Initialize session_state if not already initialized
if 'history' not in st.session_state:
    st.session_state.history = []
if 'position' not in st.session_state:
    st.session_state.position = -1  # Position of the current display in history

# API Keys (Replace with your actual API keys)
openai_api_key = "key"
stealthgpt_api_key = "key"
gptzero_api_key = 'key'

# Title
st.title('ChatGPT')

# Model selection
model_selection = st.selectbox('Select the model:', ['gpt-3.5-turbo', 'gpt-4'])

# Metric display
st.write('<div style="text-align: right; color: blue;">AI Detection Score: N/A</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input('You: ')

# Load conversation and rephrase_list based on the current position
if st.session_state.position == -1:
    conversation = []
    rephrase_list = []
else:
    conversation, rephrase_list = st.session_state.history[st.session_state.position]

# Add user input to conversation
if user_input:
    conversation.append({"role": "user", "content": user_input})

    # Make API call to OpenAI GPT model
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model=model_selection,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]
    )
    chatbot_response = response['choices'][0]['message']['content'].strip()
    conversation.append({"role": "assistant", "content": chatbot_response})

    # Call GPTZero for AI Detection Score
    gptzero_response = requests.post(
        "https://api.gptzero.me/v2/predict/text",
        headers={"x-api-key": gptzero_api_key},
        json={"document": chatbot_response}
    ).json()

    if 'documents' in gptzero_response:
        ai_detection_score = f"{round(gptzero_response['documents'][0]['completely_generated_prob'] * 100, 2)}%"
    else:
        ai_detection_score = "N/A"

    st.session_state.history.append((conversation[:], rephrase_list[:]))
    st.session_state.position += 1

# Display AI Detection Score
st.write(f'<div style="text-align: right; color: blue;">AI Detection Score: {ai_detection_score}</div>', unsafe_allow_html=True)

# Rephrase button
if st.button('Rephrase Text'):
    headers = {'api-token': stealthgpt_api_key, 'Content-Type': 'application/json'}
    data = {'prompt': conversation[-1]['content'], 'rephrase': True}
    response = requests.post('https://stealthgpt.ai/api/stealthify', headers=headers, json=data)
    
    if response.status_code == 200:
        rephrased_text = response.json().get('response', 'Could not rephrase')
        rephrase_list.append(rephrased_text)
     
    st.session_state.history.append((conversation[:], rephrase_list[:]))   
    st.session_state.position += 1

# Display conversation and rephrases
st.write("### Conversation:")
for turn in conversation:
    if turn['role'] == 'user':
        st.write(f'<div style="color: blue; background-color: #E6EFFF; padding: 10px; border-radius: 12px; margin: 5px;"><b>You:</b> {turn["content"]}</div>', unsafe_allow_html=True)
    elif turn['role'] == 'assistant':
        st.write(f'<div style="color: black; background-color: #F0F0F0; padding: 10px; border-radius: 12px; margin: 5px;"><b>ChatGPT:</b> {turn["content"]}</div>', unsafe_allow_html=True)
    
for rephrase in rephrase_list:
    st.write(f'<div style="color: black; background-color: #D3D3D3; padding: 10px; border-radius: 12px; margin: 5px;"><b>Rephrased Text:</b> {rephrase}</div>', unsafe_allow_html=True)
