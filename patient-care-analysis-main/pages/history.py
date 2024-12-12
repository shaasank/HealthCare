import streamlit as st
st.set_page_config(page_title="History",page_icon="📖")
import time
from db_operations import collection

if 'logged_in' not in st.session_state:
    st.error("You should Sign in!")
    time.sleep(2)
    st.switch_page("pages/login.py")




st.sidebar.markdown(f"<span style='font-weight:bold;'>Patient Care Analysis <img src={'https://cdn-icons-png.freepik.com/32/12058/12058949.png'}></img></span>",unsafe_allow_html=True)
st.sidebar.page_link("pages/prediction.py",label="Prediction",icon="🧏")
st.sidebar.page_link("pages/report.py",label="Report",icon="📑")
st.sidebar.page_link("pages/history.py",label="History",icon='📖')
st.sidebar.page_link("pages/chatbot.py",label="MedBot",icon="🤖")
st.sidebar.page_link("pages/logout.py",label="Logout",icon="⬅️")

cols=st.columns(2)
user=collection.find_one({"email":st.session_state.user_email})
disease_arr=user['diseases'] if 'diseases' in user else []

if not disease_arr:
    st.write("There is no history report to be shown")

else:
    @st.dialog("Personalized Health Report")
    def display_report(user_record):
        dis=user_record['extra_diseases'].split(",")
        with st.container():
            st.markdown(f"""
            **Hello {user_record['name']},**
        """)
            st.markdown('''
    <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:10px;
                line-height:1;
            }
            .st-b0 {
                line-height: 1.6;
                overflow: scroll;
                height: 545px;
            }
            .st-bc {
                color: rgb(49, 51, 63);
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                background-color: #f0f3fff2;
            }
                                
    </style>
    ''', unsafe_allow_html=True)
        # Predicted disease and description
            st.subheader(f"Predicted Disease: {user_record['disease']}")
            st.subheader(f'You might also have these diseases: {dis[0]},  {dis[1]}')
            st.write(f"{user_record['description']}")

            # Precautions
            st.subheader("Precautions")
            st.markdown(f"""\
            {user_record['precautions']}
            """)

            # Medications
            st.subheader("Medications")
            st.markdown(f"""\
            {user_record['medications']}
            """)
            # Diet
            st.subheader("Diet")
            diet=user_record['diet'].split()
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
           
    c=st.container(height=300   )
    with c:
        cols=c.columns(1)
        for i in range(len(disease_arr)):
            try:
                    with cols[0]:
                            col1, col2 = st.columns([2, 2])  # Adjust the ratios as needed
                            with col1:
                                but1=st.button(disease_arr[i]['disease'],key=str(i))
                            with col2:
                                a=st.button("🗑️ Delete",key=disease_arr[i]['id'])
                            if but1:    
                                display_report(disease_arr[i])
                            if a:
                                st.success("Successfully deleted!!!")
                                del st.session_state[disease_arr[i]['id']]
                                collection.find_one_and_update({"email":st.session_state.user_email},{"$pull":{"diseases":{"id":disease_arr[i]['id']}}})
                            
                   
            except:
                pass
