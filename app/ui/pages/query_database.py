import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import random

from utils.api_calls import api_request
from urllib.parse import quote
from utils.console import console_log


def verify_sql_injection(query):
    encoded_query = quote(query)
    response = api_request(
        api_url=f"http://0.0.0.0:8200/api/verify-sql-injection/{encoded_query}",
        json=None
    )['status']

    return response


def call_rag(query, message_history_id):
    response = api_request(
        api_url=f"http://0.0.0.0:8200/api/text-to-sql/",
        json={
             "message_history_id": message_history_id,
             "query": query
        }
    )
    return response


def get_historic_message(message_history_id):
    response = api_request(
        api_url=f"http://0.0.0.0:8200/api/historic-message/",
        json={
                "message_history_id": message_history_id,
                "question": ""
            })
    
    return response


def write_user_and_assistant_messages(q_and_a):
    for msg in q_and_a:
        owner = "assistant" if msg["role"] == "assistant" else "user"
        with st.chat_message(name=owner):
            st.write(msg["content"])


def update_historic(q_and_a):
    if "historic" not in st.session_state:
        st.session_state.historic = q_and_a
    else:
        for msg in q_and_a:
            st.session_state.historic.append(msg)


def get_new_message_history_id():
    return random.randint(0, 2**16 - 1)


def return_historic():
    if "historic" not in st.session_state:
        if "message_history_id_site" not in st.session_state:
            st.session_state.message_history_id_site = get_new_message_history_id()
            return []
        else:
            response = get_historic_message(
                st.session_state.message_history_id_site)
            return response
    return st.session_state.historic


def update_last_message(msg):
    if "last_message" not in st.session_state:
        st.session_state.last_message = msg
    else:
        st.session_state.last_message = msg


def return_last_message():
    if "last_message" not in st.session_state:
        return []
    return st.session_state.last_message


with st.chat_message(name="assistant"):
    st.markdown("Hi! How can i help you?")

write_user_and_assistant_messages(return_historic())

if user_input := st.chat_input("Type Here"):
    status = verify_sql_injection(user_input)

    if status:
        if status == 'Secure':
            # st.success("Hi")
            response = call_rag(
                query=user_input,
                message_history_id= st.session_state.message_history_id_site
            )

            update_historic(response)
            update_last_message(response)
            write_user_and_assistant_messages(return_last_message())

        else:
            st.warning("Be careful, your input is trying to make SQl Injection!")

if st.button("Limpar histórico"):
    if "historic" in st.session_state and "last_message" in st.session_state:
        del st.session_state.historic[:]
        del st.session_state.last_message[:]
    st.session_state.message_history_id_site = get_new_message_history_id()
    streamlit_js_eval(js_expressions="parent.window.location.reload()")