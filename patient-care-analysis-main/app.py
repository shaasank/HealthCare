import streamlit as st
st.set_page_config(page_title="Patient Care Analysis" ,page_icon='https://cdn-icons-png.flaticon.com/64/6401/6401060.png')
import scheduler

st.markdown("""
            <style>
            .stAppViewContainer{
                background-image:url("./app/static/healthcare.png");
                background-size:cover;

            }
            .st-emotion-cache-12fmjuu{
            display:none;
            }
            .stButton>button {
                color: #4F8BF9;
                border-radius: 20%;
                backgroud-color: #00ff00;
                height: 3.5rem;
                width: 8rem;
                position:relative;
                top:410px;
                left:90px;
                }
            <\style>
            """,unsafe_allow_html=True)

res=st.button("Login")
if res:
    st.switch_page("pages/login.py")