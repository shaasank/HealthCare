import streamlit as st

def set_session():
    st.session_state.logged_in=True

def clear_session():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']