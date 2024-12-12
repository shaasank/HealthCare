import google.generativeai as genai
from pathlib import Path
import time
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
current_dir = Path.cwd()
env_vars = current_dir / ".env"
load_dotenv(env_vars)


genai.configure(api_key=st.secrets["PERSONALIZED_REPORT"])
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


model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def generate_questions(disease, symptoms,age):
    prompt =  f"""
    Disease: {disease}
    Symptoms: {symptoms}
    Age: {age}
    
    Generate 3 diagnostic questions that will help determine the severity of the condition (mild, moderate, severe).
    Focus on the symptoms and consider the age of the patient.
    For each question, provide multiple-choice options in brackets (e.g., [option1, option2, option3]).
    Example output format:
    1. How severe is your headache? [Mild, Moderate, Severe]
    2. How long have you been experiencing these symptoms? [Less than 1 week, 1-2 weeks, More than 2 weeks]
    3. How often do you experience these symptoms? [Rarely, Occasionally, Frequently]
    """
    response = model.generate_content(prompt)
    questions = response.text.split('\n')
    return questions
    answers = []
    for question in questions:
        if question.strip():  # Check if the line is not empty
            print(question)
            answer = input("Your answer: ")
            answers.append((question, answer))

    # Create a new prompt to assess severity based on the answers
    severity_prompt = f"""
    Based on the following answers, assess the severity of the symptoms for the disease '{disease}':
    Symptoms: {symptoms}
    Answers: {answers}
    Provide a severity assessment (e.g., mild, moderate, severe) and a brief explanation.
    """
    severity_response = model.generate_content(severity_prompt)
    severity = severity_response.text.strip()

    return answers, severity

def generate_personalized_advice( sleep_cycle,symptoms,activity_level,medical_history, severity, disease):

    prompt = f"""
    Based on the following information:
    - Sleep cycle: {sleep_cycle}
    - Activity level: {activity_level}
    - Medical history: {medical_history}
    - Reported symptoms: {symptoms}

    - Disease severity: {severity}
    - Potential disease: {disease}

    Generate 5 lines of personalized advice focused on practical, actionable steps tailored to this individual's situation. 
    Consider how their sleep cycle, activity level, and medical history interact with their reported symptoms and the severity of their condition. 
    Provide specific recommendations on how to improve sleep, adjust activity levels, and manage symptoms, especially in light of their medical history. 
    Tailor the advice to match the severity, offering more cautious steps if the condition is severe, and more self-care-oriented suggestions if it's less severe. 
    Include guidance on when and whether to seek professional medical help based on the severity and symptoms, and suggest the next best action they should take.
    """
    response = model.generate_content(prompt)
    return response.text
