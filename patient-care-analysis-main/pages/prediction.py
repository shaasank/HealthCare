import streamlit as st

st.set_page_config(page_title="Predicton" ,page_icon="🧏")

from model import predict_disease
from send_email import send_email
from db_operations import add_data
from symptoms_options import unique_symptoms
import gen_ai
from gen_ai import model
import time
#scheduler.main()
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("You should Sign in")
    st.switch_page("pages/login.py")


# Init session_state 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

if "user_name" not in st.session_state:
    st.session_state.user_name=''

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'answers' not in st.session_state:
    st.session_state.answers = []

if 'questions' not in st.session_state:
    st.session_state.questions = []

if 'user_record' not in st.session_state:
    st.session_state.user_record='' 


def details_page():
    st.title("Patient Care Analysis")

    if st.session_state.logged_in:
        user_record = {}

        if not st.session_state.form_submitted:
            with st.form("details_form"):
                name = st.text_input('Name')
                age = st.number_input('Age', min_value=1, max_value=100)
                symptoms = st.selectbox('Select your primary symptom', options=unique_symptoms)
                sleep_cycle = st.selectbox('What is your sleep cycle?', ['4 hours', '6 hours', '8 hours'])
                activity_level = st.selectbox('How is your life activity level?', ['active', 'very active', 'less active', 'lazy'])
                medical_history = st.selectbox('Do you have a medical history of any of the following diseases?',
                                               ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Cancer", "Arthritis", "Thyroid Disorder", "None of the above"])
                submitted = st.form_submit_button("Submit")
                
                if submitted and name and age and symptoms:
                    st.session_state.form_submitted = True
                    st.session_state.user_name = name
                    st.session_state.user_age = age
                    st.session_state.symptoms = symptoms
                    st.session_state.sleep_cycle = sleep_cycle
                    st.session_state.activity_level = activity_level
                    st.session_state.medical_history = medical_history
                    top_diseases, description, precautions, medications, diet, workout = predict_disease(symptoms)
                    st.session_state.disease = top_diseases
                    st.session_state.description = description
                    st.session_state.precautions = precautions
                    st.session_state.medications = medications
                    st.session_state.diet = diet
                    st.session_state.workout = workout
                    st.session_state.questions = gen_ai.generate_questions(st.session_state.disease[0], st.session_state.symptoms,st.session_state.user_age)
                    st.rerun()

        if st.session_state.form_submitted:
            if st.session_state.question_index < len(st.session_state.questions):
                question = st.session_state.questions[st.session_state.question_index]
                answer = st.text_input(question)
                if st.button("Submit Answer"):
                    st.session_state.answers.append(answer)
                    st.session_state.question_index += 1
                    st.rerun()
            else:
                severity_prompt = f"""
                Based on the following answers, assess the severity of the symptoms for the disease '{st.session_state.disease[0]}':
                Symptoms: {st.session_state.symptoms}
                Answers: {st.session_state.answers}
                Provide a severity assessment (e.g., mild, moderate, severe) and a brief explanation.
                """
                severity_response = model.generate_content(severity_prompt)
                severity = severity_response.text.strip()
                advice = gen_ai.generate_personalized_advice(
                    st.session_state.sleep_cycle, 
                    st.session_state.symptoms, 
                    st.session_state.activity_level, 
                    st.session_state.medical_history, 
                    severity, 
                    st.session_state.disease[0]
                )

                user_record = {
                    "name": st.session_state.user_name,
                    "age": st.session_state.user_age,
                    "email": st.session_state.user_email,
                    "disease": st.session_state.disease[0],
                    "description": st.session_state.description,
                    "precautions": st.session_state.precautions,
                    "medications": st.session_state.medications,
                    "diet": st.session_state.diet,
                    "workout": st.session_state.workout,
                    'Personalized Advice': advice,
                    "extra_diseases":','.join(st.session_state.disease[1:])
                }

                # Add to database
                add_data(user_record)
                # Send email
                send_email(user_record)
                
                st.write("Health report is sent to your email. Do check it out!")
                st.session_state.user_record=user_record
               
                st.session_state.answers = []
                st.session_state.form_submitted = False
                st.session_state.question_index = 0
                st.switch_page("pages/report.py")




def main():
    if st.session_state.logged_in:
        
        st.sidebar.markdown(f"<span style='font-weight:bold;'>Patient Care Analysis <img src={'https://cdn-icons-png.freepik.com/32/12058/12058949.png'}></img></span>",unsafe_allow_html=True)
        st.sidebar.page_link("pages/prediction.py",label="Prediction",icon="🧏")
        st.sidebar.page_link("pages/report.py",label="Report",icon="📑")
        st.sidebar.page_link("pages/history.py",label="History",icon='📖')
        st.sidebar.page_link("pages/chatbot.py",label="MedBot",icon="🤖")
        st.sidebar.page_link("pages/logout.py",label="Logout",icon="⬅️")
        
        details_page()
    else:
        st.switch_page('pages/login.py')

if __name__ == "__main__":
    main()