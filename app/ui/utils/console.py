import streamlit as st
from random import randint
from datetime import datetime


def init_console():
    """Initialize the console in session state."""
    if 'logs' not in st.session_state:
        st.session_state.logs = ""


def console_log(message):
    """Append a message to the console logs."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs += f"{now} | {message}\n"


def display_console():
    """Render the console in the Streamlit app."""
    console_placeholder = st.empty()
    console_placeholder.text_area("Console Output", key=randint(
        0, 10**3), value=st.session_state.logs, height=300, disabled=True)
    return console_placeholder


def update_console(placeholder):
    """Update the console output with current logs."""
    placeholder.text_area("Console Output", key=randint(
        0, 10**3), value=st.session_state.logs, height=300, disabled=True)
