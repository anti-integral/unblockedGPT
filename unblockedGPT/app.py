import streamlit as st
import openai

# Initialize conversation state
conversation = []

# Title
st.title('UnblockedGPT Chatbot')

# Model selection
model_selection = st.selectbox('Select the model:', ['gpt-3.5-turbo', 'gpt-4'])

# User input
user_input = st.text_input('You: ')

# Add user input to conversation
if user_input:
    conversation.append({"role": "user", "content": user_input})

# Display conversation history
st.write("### Conversation:")
for turn in conversation:
    if turn["role"] == "user":
        st.write(f"You: {turn['content']}")
    elif turn["role"] == "assistant":
        st.write(f"UnblockedGPT ({model_selection}): {turn['content']}")

# Chatbot logic
if user_input:
    # Make API call to OpenAI GPT model (replace 'your_openai_api_key_here' with your actual API key)
    openai.api_key = "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"
    model_engine = model_selection
    response = openai.Completion.create(
        engine=model_engine,
        prompt=conversation,
        max_tokens=100
    )

    # Extract and display chatbot's reply
    chatbot_response = response.choices[0].text.strip()
    conversation.append({"role": "assistant", "content": chatbot_response})
    st.write(f"UnblockedGPT ({model_selection}): {chatbot_response}")
