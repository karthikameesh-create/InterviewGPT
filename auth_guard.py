import streamlit as st


def initialize_session():

    defaults = {
        "logged_in": False,
        "user": None,
        "user_email": ""
    }

    for key, value in defaults.items():

        st.session_state.setdefault(key, value)


def logout():

    st.session_state.clear()

    st.rerun()