from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader

from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.lang import en, cn

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_CN: str = "中文"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    # "gpt-4",
    # "gpt-4-32k",
    # "bard",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


def chat() -> None:
    # sidebar area
    with st.sidebar:
        st.markdown(f'### Welcome *{name}*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()

        st.selectbox(label=st.session_state.locale.select_placeholder1, key="model",
                     options=AI_MODEL_OPTIONS)
        st.session_state.input_kind = st.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = st.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                st.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case st.session_state.locale.radio_text2:
                st.text_input(label=st.session_state.locale.select_placeholder3, key="role")

    # main area
    selected_lang = option_menu(
        menu_title=None,
        options=[LANG_EN, LANG_CN, ],
        icons=["globe2", "translate"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "中文":
            st.session_state.locale = cn
        case _:
            st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)

    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    get_user_input()
    show_chat_buttons()


if __name__ == "__main__":
    with open('./.streamlit/accounts.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status is None:
        st.warning('Please enter your username and password')
        st.stop()

    if not authentication_status:
        st.error('Username/password is incorrect')
        st.stop()

    if authentication_status:
        # --- LOAD CSS ---
        with open(css_file) as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

        # Storing The Context
        if "locale" not in st.session_state:
            st.session_state.locale = en
        if "generated" not in st.session_state:
            st.session_state.generated = []
        if "past" not in st.session_state:
            st.session_state.past = []
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_text" not in st.session_state:
            st.session_state.user_text = ""
        if "input_kind" not in st.session_state:
            st.session_state.input_kind = st.session_state.locale.input_kind_1

        chat()
