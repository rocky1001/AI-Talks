import deepl
import streamlit as st


@st.cache_data()
def translate(src_text: str, dst_lang: str) -> str:
    try:
        auth_key = st.secrets.api_credentials.deepl_key  # Replace with your key
        translator = deepl.Translator(auth_key)

        result = translator.translate_text(src_text, target_lang=dst_lang)
        return result.text
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    except Exception as e:
        return e
