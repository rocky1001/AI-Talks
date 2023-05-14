import logging
import random
from typing import List  # NOQA: UP035

import openai
import streamlit as st


@st.cache_data()
def gpt_thinking(ai_model: str, messages: List[dict]) -> dict:
    try:
        openai.api_key = random.choice(st.secrets.api_credentials.api_key)
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    logging.info(f"{messages=}")
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
        temperature=0.7,
        # stream=True,
    )
    logging.info(f"{completion=}")
    return completion
