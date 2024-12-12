import streamlit as st
st.set_page_config(page_title="Chatbot", page_icon=":chat:", layout="wide")
import google.generativeai as genai
from pathlib import Path
import time
from dotenv import load_dotenv
import os

# Load environment variables
current_dir = Path.cwd()
env_vars = current_dir / ".env"
load_dotenv(env_vars)


if 'logged_in' not in st.session_state:
    st.error("You should Sign in")
    st.switch_page("pages/login.py")

import json
from streamlit_lottie import st_lottie
import time


def load_lottie(file):
    with open(file,'r') as f:
        return json.load(f)


lottie_file=load_lottie('Animation - 1723451591208.json')
st_lottie(
    lottie_file,
    speed=1,
    reverse=False,
    loop=True,
    width=800,
    height=100
)

st.sidebar.markdown(f"<span style='font-weight:bold;'>Patient Care Analysis <img src={'https://cdn-icons-png.freepik.com/32/12058/12058949.png'}></img></span>",unsafe_allow_html=True)
st.sidebar.page_link("pages/prediction.py",label="Prediction",icon="🧏")
st.sidebar.page_link("pages/report.py",label="Report",icon="📑")
st.sidebar.page_link("pages/history.py",label="History",icon='📖')
st.sidebar.page_link("pages/chatbot.py",label="MedBot",icon="🤖")
st.sidebar.page_link("pages/logout.py",label="Logout",icon="⬅️")




genai.configure(api_key=st.secrets["CHATBOTAPI"])
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings,system_instruction="""  you are a mental health chatbot and you should provide only the health related responses other than that you should tell that I am here to help you only for the  health related queries.
            So,give a intro about yourself your name is MedBot and say that users can ask any question abut their mentalhealth or their deisese, answer every thing in 3 lines not more than taht talk like a friend who is very conserned about , you will let the user speak out  their heart and answer them with care, use polite words and handle  with care ,if the user says something that is no 
            related to mental health, you will respond with Im sorry to hear  that, Im here here for you, you can talk freely and I will listen to you, I will try to help you and I will be here for 
            you, if the user says something that is related to their predicted diseases you should  act like a professional doctor on that particular topic and answer their querys and give simple 
            tips to avoid the problems they are facing ,if the predicted disease and there mental health symptoms are releated to each other give solution according to that, make it more conversational and more interactive answer only for waht the users asks for dont give summery or report""")


def generate_questions(inp): 
    dis=st.session_state.disease[0] if 'disease' in st.session_state else ''
    name=st.session_state.user_name if 'user_email' in st.session_state else ''
    if not inp:
        if dis and name:
            prompt = f"""
            Disease: {dis}
            name : {name}
            """
        else:
            prompt=f"""Hi, How may I help you?"""
            return prompt
    else:
        prompt=inp
    response = model.generate_content(prompt)
    return response.text
def response_generator(response):    
    for word in response:
        yield word
        time.sleep(0.01)


if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":generate_questions('')}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt=st.chat_input("Enter your query")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response=generate_questions(prompt)
        st.write(response_generator(response))
        st.session_state.messages.append({"role": "assistant", "content": response})