import streamlit as st
import time
from session import clear_session
clear_session()
st.info("Successfully Logged out!!!")
time.sleep(2)
st.switch_page("app.py")