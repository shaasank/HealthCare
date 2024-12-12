import streamlit as st

st.set_page_config(page_title="Login" ,page_icon='https://cdn-icons-png.flaticon.com/64/2250/2250207.png')

from db_operations import add_user
from session import set_session
import time
from streamlit_lottie import st_lottie

import requests

def login_page():
    st.title("Login")
    st.markdown("""\
                <style>
                /*.stAppViewContainer{
                background-image:url("./app/static/healthcare.png");
                background-size:cover   ;
                background-repeat:no-repeat;
                }
                */
                <\style>
                """,unsafe_allow_html=True)
    with st.container( height=400):
        c1=st.columns(2)

        c1[0].image('https://img.freepik.com/free-vector/public-health-concept-illustration_114360-8999.jpg?t=st=1731313750~exp=1731317350~hmac=e74388dcb411369ac42a97240fa0edb659d1ee2ee242f7d91c8aa5d193a5684c&w=740',use_column_width=True)
        user_email = c1[1].text_input("Email")
        password=c1[1].text_input("Password",type='password')
        res=c1[1].button("Login")
    if res:
        if user_email:
            with c1[1].status(expanded=True,label='') as status:
                opt=add_user(user_email,password)
                if opt=='new': 
                    status.update(state='complete',label='Signing up',expanded=False)
                    c1[1].success("Account created successfully")
                  
                    c1[1].session_state.logged_in = True
                    c1[1].session_state.user_email = user_email
                    
                    set_session()
                    c1[1].switch_page('pages/loading.py')
                elif opt:
                    status.update(state='complete',label='Signing in',expanded=False)
                    c1[1].success("Successfully signed in")
                    c1[1].session_state.logged_in = True
                    c1[1].session_state.user_email = user_email
                    set_session()
                    st.switch_page('pages/loading.py')
                    
                else:
                    c1[1].error("Invalid email or password")
                
        else:

            c1[1].error("Invalid email or password")


login_page()
