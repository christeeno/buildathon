import streamlit as st
import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyCVZ3B6HWiqHx6g32oUkFNSbuHCawBAJWo")

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    try:
        # Send a message and get the response
        response = chat.send_message(question)
        return response
    except Exception as e:
        # Catch any exceptions and return the error message
        return f"Error: {str(e)}"


# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="wide")

# Add custom CSS
st.markdown(
    """
    <style>
    .main {
        background-image: url('https://www.example.com/background.jpg');
        background-size: cover;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Terminous")
is_on = True

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Layout with columns
col1, col2 = st.columns([1, 3])

with col1:
    st.sidebar.header("Chat with Gemini")
    input = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

    # Move chat history to the sidebar
    with st.sidebar.expander("Chat History"):
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")

with col2:
    if submit and input:
        response = get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")

        # Handle response object
        if isinstance(response, str):
            # In case of an error or direct response
            st.write(response)
            st.session_state['chat_history'].append(("Bot", response))
        elif hasattr(response, 'candidates') and response.candidates:
            # If the response contains candidates
            for candidate in response.candidates:
                st.write(candidate.content.parts[0].text)
                st.session_state['chat_history'].append(("Bot", candidate.content.parts[0].textgit))
        else:
            st.write("Unexpected response format.")
            st.session_state['chat_history'].append(("Bot", "Unexpected response format."))

