import streamlit as st
st.set_page_config(page_title="Health Report", page_icon=":medical_symbol:", layout="wide")

from pdf_generator import generate_pdf
from db_operations import get_data


if 'logged_in' not in st.session_state:
    st.error("You should Sign in")
    st.switch_page("pages/login.py")

def display_report(user_record):
        # Generate PDF content
    pdf_filename = generate_pdf(user_record)
    cont=st.container(height=700)
    with cont:
        cont.markdown(f"""
        <h1 style="text-align:center";>Personalized Health Report</h1>
        <h5>Hello {user_record['name']},</h5>
    """,unsafe_allow_html=True)
        st.markdown('''
        <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:10px;
                line-height:1;
            }
        </style>
        ''', unsafe_allow_html=True)
    # Predicted disease and description
        dis=user_record['extra_diseases'].split(",")
        st.subheader(f"Predicted Disease: {user_record['disease']}")
        st.write(f'You might also have these diseases: {dis[0]},  {dis[1]}')
        st.subheader("Description")
        st.write(f"{user_record['description']}")

        # Precautions
        st.subheader("Precautions")
        st.markdown(f"""\
        {user_record['precautions']}
        """)

        # Medications
        cont.subheader("Medications")
        st.markdown(f"""\
        {user_record['medications']}
        """)
        # Diet
        st.subheader("Diet")
        diet=user_record['diet'].split(',')
        print(user_record['diet'])
        for i in range(len(diet)): 
            st.markdown(f'- {diet[i].strip(',')}')
        st.subheader("Do's & Dont's:")
        do_dont=user_record['workout'].split(',')
        for i in range(len(do_dont)):
            st.markdown(f"- {do_dont[i]}")

        # Personalized Advice
        st.subheader("Personalized Advice")
        st.markdown(f"""\
        {user_record['Personalized Advice']}
        """)


        # Provide download button
        with open(pdf_filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(
            label="Download your report",
            data=PDFbyte,
            file_name="medical_report.pdf",
            mime='application/pdf'
        )

if 'user_email' in st.session_state:
    user_record = get_data({"email": st.session_state.user_email})
    print(user_record,'user')
    if user_record and 'diseases' in user_record and len(user_record['diseases']):
        display_report(user_record['diseases'][-1])
    else:
        st.write("There is no report to be shown")
else:
    st.write("There is no report to be shown")



st.sidebar.markdown(f"<span style='font-weight:bold;'>Patient Care Analysis <img src={'https://cdn-icons-png.freepik.com/32/12058/12058949.png'}></img></span>",unsafe_allow_html=True)
st.sidebar.page_link("pages/prediction.py",label="Prediction",icon="🧏")
st.sidebar.page_link("pages/report.py",label="Report",icon="📑")
st.sidebar.page_link("pages/history.py",label="History",icon='📖')
st.sidebar.page_link("pages/chatbot.py",label="MedBot",icon="🤖")
st.sidebar.page_link("pages/logout.py",label="Logout",icon="⬅️")
