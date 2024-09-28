import streamlit as st

import google.generativeai as genai

from langdetect import detect  # Library for language detection



# Configure the API key

genai.configure(api_key="AIzaSyCVZ3B6HWiqHx6g32oUkFNSbuHCawBAJWo")



# Function to load Gemini Pro model and get responses

model = genai.GenerativeModel("gemini-pro")

chat = model.start_chat(history=[])



# Function to check if a question is medical-related

def is_medical_question(question):

    medical_keywords = [

        "health", "disease", "treatment", "diagnosis", "symptom", "medicine",

        "doctor", "hospital", "surgery", "therapy", "infection", "virus",

        "vaccine", "condition", "emergency", "prescription", "pharmacy"

    ]

    # Convert question to lower case and check for any medical keywords

    return any(keyword in question.lower() for keyword in medical_keywords)



# Function to detect if the text is in English

def is_english(text):

    try:

        language = detect(text)

        return language == 'en'

    except Exception:

        return False  # If language detection fails, assume it's not English



# Function to get response from Gemini Pro model

def get_gemini_response(question):

    try:

        response = chat.send_message(question)

        return response

    except Exception as e:

        return f"Error: {str(e)}"



# Initialize the Streamlit app

st.set_page_config(page_title="Q&A Demo", layout="wide")



# Add custom CSS

st.markdown(

    """
    <style>
    
    .main {

        background-image: url('https://wallpaperaccess.com/full/6890234.jpg');

        background-size: cover;

    }

    .stButton>button {

        background-color: #BF342A;

        color: white;

    }

    .stTextInput>div>input {

        border: 2px solid #4CAF50;

    }
    <style>
     .block-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        height: 200vh;
    }
    .stTextInput > div > div > input {
        width: 100%;
    }
    </style>

    """,

    unsafe_allow_html=True

)



st.markdown(
    "<h1 style='text-align: center;'>Terminous</h1>",
    unsafe_allow_html=True
)

is_on = True



# Initialize session state for chat history if it doesn't exist

if 'chat_history' not in st.session_state:

    st.session_state['chat_history'] = []



# Layout with columns

col1, col2 = st.columns([0.3, 0.7])



with col1:

    st.sidebar.header("Chat with Terminus")

    user_input = st.text_input("Input: ", key="input")

    submit = st.button("Ask the question")



    # Move chat history to the sidebar
    question_number = 1  # Track question numbering

    for i, (role, text) in enumerate(st.session_state['chat_history']):
        print(role,text)
        if role == "You":
            with st.sidebar.expander(f"Q{question_number}: {text}"):
                # Find the corresponding bot response and display it inside the expander

                bot_response = st.session_state['chat_history'][i + 1][1] if i + 1 < len(
                    st.session_state['chat_history']) else "No response available."

                st.write(f"**Response:** {bot_response}")

            question_number += 1  # Increment the question number only for user inputs



with col2:

    if submit and user_input:

        # if is_medical_question(user_input):
        our_prompt = "; Analyze, this prompt well, if this prompt is not a medical related prompt, or health topic related prompt then just reply with this message - This bot only answers health related queries, or else reply with correct answer"
        response = get_gemini_response(user_input + our_prompt)



        # Add user query and response to session state chat history

        st.session_state['chat_history'].append(("You", user_input))



        # Handle response object

        if isinstance(response, str):

            if is_english(response):

                st.session_state['chat_history'].append(("Bot", response))

            else:

                st.session_state['chat_history'].append(("Bot", "The response is not in English."))

        elif hasattr(response, 'candidates') and response.candidates:

            for candidate in response.candidates:

                candidate_text = candidate.content.parts[0].text
                st.write(candidate_text)

                if is_english(candidate_text):

                    st.session_state['chat_history'].append(("Bot", candidate_text))

                else:

                    st.session_state['chat_history'].append(("Bot", "The response is not in English."))

        else:

            st.session_state['chat_history'].append(("Bot", "Unexpected response format."))



        # else:
        #
        #     st.write(f"{user_input} is not  a medical-related question.")
        #
        #     st.session_state['chat_history'].append(("Bot", "Please ask a medical-related question."))



    # Display the chat history in the form of expandable sections




