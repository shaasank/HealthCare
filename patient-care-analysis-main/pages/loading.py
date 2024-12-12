import json
from streamlit_lottie import st_lottie
import streamlit as st
import time

def load_lottie(file):
    with open(file,'r') as f:
        return json.load(f)

lottie_file=load_lottie('Animation - 1723450621256.json')



with st.container():
    st_lottie(
    lottie_file,
    speed=1,
    reverse=False,
    loop=True,
    width=700,
    height=400,
    key="loading"
)
st.write('<h4 style="text-align:center">Loading...</h4>',unsafe_allow_html=True)
    

time.sleep(2)
st.switch_page("pages/prediction.py")