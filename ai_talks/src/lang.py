from dataclasses import dataclass
from typing import List  # NOQA: UP035


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    ai_role_postfix: str
    title: str
    language: str
    lang_code: str
    chat_placeholder: str
    chat_run_btn: str
    chat_clear_btn: str
    chat_save_btn: str
    speak_btn: str
    input_kind: str
    input_kind_1: str
    input_kind_2: str
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str
    empty_api_handler: str


AI_ROLE_OPTIONS_EN = [
    "helpful assistant",
    "english grammar expert",
    "friendly and helpful teaching assistant",
    "translate corporate jargon into plain English",
    "text improver",
]

AI_ROLE_OPTIONS_CN = [
    "助理",
    "英语语法专家",
    "教学助理",
    "英语翻译",
    "文字优化",
]

readme_url = ""
ai_talks_url = ""

en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are an assistant",
    ai_role_postfix="Answer as concisely as possible.",
    title="AI Talks",
    language="English",
    lang_code="en",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    speak_btn="Push to Speak",
    input_kind="Input Kind",
    input_kind_1="Text",
    input_kind_2="Voice[test]",
    select_placeholder1="Select Model",
    select_placeholder2="Select Role",
    select_placeholder3="Create Role",
    radio_placeholder="Role Interaction",
    radio_text1="Select",
    radio_text2="Create",
    stt_placeholder="To Hear The Voice Of AI Press Play",
    empty_api_handler=f"""
        API key not found. Create `.streamlit/secrets.toml` with your API key.
        See [README.md]({readme_url}) for instructions or use the original [AI Talks]({ai_talks_url}).
    """,
)

cn = Locale(
    ai_role_options=AI_ROLE_OPTIONS_CN,
    ai_role_prefix="你是一名女性助理",
    ai_role_postfix="回答的尽可能的耐心",
    title="AI Talks",
    language="中文",
    lang_code="zh",
    chat_placeholder="开始对话吧",
    chat_run_btn="发送",
    chat_clear_btn="清理",
    chat_save_btn="保存",
    speak_btn="按下说话",
    input_kind="输入类型",
    input_kind_1="文本",
    input_kind_2="语音[测试中]",
    select_placeholder1="选择模型",
    select_placeholder2="选择角色",
    select_placeholder3="创建角色",
    radio_placeholder="角色反应",
    radio_text1="选择",
    radio_text2="创建",
    stt_placeholder="按下Play听语音",
    empty_api_handler=f"""
        API key not found. Create `.streamlit/secrets.toml` with your API key.
    """,
)
