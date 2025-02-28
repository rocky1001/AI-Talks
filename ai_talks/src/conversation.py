import streamlit as st
from openai.error import InvalidRequestError, OpenAIError
from requests.exceptions import TooManyRedirects
from src.agi.bard import BardChat
from src.agi.chat_gpt import gpt_thinking
from src.trans.trans import translate
from src.tts import show_audio_player
from streamlit_chat import message

TRANS_LANG_OPTIONS = {
    "en-US": "ENGLISH_AMERICAN",
    "en-GB": "ENGLISH_BRITISH",
    "zh": "中文",
    "nl": "DUTCH",
    "fr": "FRENCH",
    "de": "GERMAN",
    "it": "ITALIAN",
    "ja": "JAPANESE",
    "ko": "KOREAN",
    "ru": "RUSSIAN",
    "es": "SPANISH",
    "sv": "SWEDISH",
    "tr": "TURKISH",
    "uk": "UKRAINIAN",
}


def format_func(option):
    return TRANS_LANG_OPTIONS[option]


def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.trans_src = ""


def show_text_input() -> None:
    st.text_area(label=st.session_state.locale.chat_placeholder, value=st.session_state.user_text, key="user_text")


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", avatar_style="fun-emoji")
            message(st.session_state.generated[i], key=str(i))
            # st.markdown(st.session_state.generated[i])


def show_gpt_conversation() -> None:
    try:
        completion = gpt_thinking(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content, st.session_state.user_text)
            st.divider()
            show_audio_player(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)


def show_bard_conversation() -> None:
    try:
        bard = BardChat(st.secrets.api_credentials.bard_session)
        ai_content = bard.ask(st.session_state.user_text)
        st.warning(ai_content.get("content"))
    except (TooManyRedirects, AttributeError) as err:
        st.error(err)


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    if st.session_state.model == "bard":
        show_bard_conversation()
    else:
        show_gpt_conversation()


def show_translation() -> None:
    st.text_area(label=st.session_state.locale.trans_placeholder, value=st.session_state.trans_src, key="trans_src")
    c1, c2 = st.columns(2)
    c1.selectbox(label="lang", label_visibility="collapsed", key="trans_dst_lang", options=list(TRANS_LANG_OPTIONS),
                 format_func=format_func)

    if c2.button(label=st.session_state.locale.trans_run_btn):
        trans_dst = translate(st.session_state.trans_src, st.session_state.trans_dst_lang)
        st.text_area(label=st.session_state.locale.trans_placeholder, value=trans_dst)