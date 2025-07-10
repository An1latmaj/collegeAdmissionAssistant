import streamlit as st
from chat import NursingAdmissionBot, ConversationState
import time

st.set_page_config(
    page_title="Nursing College Admission Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary-dark: #4a4a4a;
        --primary-blue: #007AFF;
        --light-blue: #eaf5ff;
        --grey: #f0f0f0;
        --text-color: #333333;
        --white: #ffffff;
        --shadow: rgba(0, 0, 0, 0.05);
        --shadow-hover: rgba(0, 0, 0, 0.1);
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: var(--grey);
    }

    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    header[data-testid="stHeader"], section[data-testid="stSidebar"] {
        display: none;
    }

    .messages-area {
        overflow-y: auto;
        padding-right: 10px;
        flex-grow: 1;
        margin-bottom: 1.5rem;
    }

    .chat-message {
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        border-radius: 18px;
        max-width: 75%;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 15px;
        animation: fadeIn 0.3s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background-color: var(--primary-blue);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .assistant-message {
        background-color: var(--light-blue);
        color: var(--text-color);
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }

    .page-title {
        color: var(--primary-dark);
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
    }

    .menu-container {
        padding-top: 1rem;
    }

    /* Enhanced expander styling with stronger selectors for text color */
    .st-emotion-cache-p5msec, div[data-testid="stExpander"] {
        border-radius: 12px !important;
        border: 1px solid #d0d0d0 !important;
        box-shadow: 0 2px 4px var(--shadow);
    }
    .st-emotion-cache-p5msec:hover, div[data-testid="stExpander"]:hover {
        box-shadow: 0 4px 8px var(--shadow-hover);
    }
    .st-emotion-cache-p5msec summary, div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-size: 15px !important;
        color: #000 !important;
    }
    /* Target every possible element within summary */
    .st-emotion-cache-p5msec summary *, div[data-testid="stExpander"] summary * {
        color: #000 !important;
    }
    /* Specific elements that might contain text */
    .st-emotion-cache-p5msec summary p, div[data-testid="stExpander"] summary p,
    .st-emotion-cache-p5msec summary span, div[data-testid="stExpander"] summary span,
    .st-emotion-cache-p5msec summary div, div[data-testid="stExpander"] summary div,
    .st-emotion-cache-p5msec summary label, div[data-testid="stExpander"] summary label {
        color: #000 !important;
    }
    /* Target by class as well */
    .st-emotion-cache-p5msec .st-emotion-cache-10trblm, div[data-testid="stExpander"] .st-emotion-cache-10trblm {
        color: #000 !important;
    }
    .st-emotion-cache-p5msec summary:hover, div[data-testid="stExpander"] summary:hover {
        color: var(--primary-blue) !important;
    }
    .st-emotion-cache-p5msec summary:hover *, div[data-testid="stExpander"] summary:hover * {
        color: var(--primary-blue) !important;
    }
    .st-emotion-cache-p5msec [data-testid="stExpanderDetails"], div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding-top: 1rem;
    }

    .stButton > button {
        background-color: var(--white);
        border: 1px solid #d0d0d0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: var(--text-color);
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
        box-shadow: 0 2px 4px var(--shadow);
        margin-bottom: 0.5rem;
    }

    .stButton > button:hover {
        background-color: var(--light-blue);
        border-color: var(--primary-blue);
        color: var(--primary-blue);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow-hover);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .ai-input-container {
        display: flex;
        gap: 0.5rem;
        padding: 0.5rem;
        background-color: var(--white);
        border-radius: 16px;
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }

    .stTextInput > div > div > input {
        border: none;
        background-color: transparent !important;
        color: var(--text-color) !important;
        font-size: 15px;
        padding: 0.75rem;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: none;
        outline: none;
    }

    .stButton > button.send-button {
        background-color: var(--primary-blue);
        color: white;
        border-radius: 12px;
        border: none;
        height: 100%;
    }
    .stButton > button.send-button:hover {
        opacity: 0.9;
    }

    .status-text {
        text-align: center;
        color: #666;
        font-size: 14px;
        padding: 1rem 0;
    }

    .reset-button-container {
        text-align: center;
        margin-top: 1rem;
    }
    .reset-button-container .stButton > button {
        background: transparent;
        border: none;
        color: #888;
        font-size: 13px;
        box-shadow: none;
    }
    .reset-button-container .stButton > button:hover {
        color: var(--primary-blue);
        background: transparent;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #aaa; }
</style>
""", unsafe_allow_html=True)
def initialize_session_state():
    if 'bot' not in st.session_state:
        st.session_state.bot = NursingAdmissionBot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False


def display_message(message, is_user=False):
    align_class = "user-message" if is_user else "assistant-message"
    st.markdown(f"""
    <div class="chat-message {align_class}">
        {message.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)


def handle_language_selection():
    st.markdown('<div class="status-text">Please select your language</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    lang_map = {"1": "🇬🇧 English", "2": "🇮🇳 हिंदी", "3": "🌍 Hinglish"}
    for i, (value, label) in enumerate(lang_map.items()):
        with cols[i]:
            if st.button(label, key=f"lang_{value}"):
                process_bot_response(value)


def handle_main_menu():
    menu_categories = {
        "About the Program": [
            ("📚 Program Details", "2"),
            ("📋 Eligibility Criteria", "1"),
            ("✅ Recognition", "6"),
        ],
        "Costs & Financial Aid": [
            ("💰 Fee Structure", "3"),
            ("🎓 Scholarships", "8"),
        ],
        "Campus & Training": [
            ("🏠 Facilities", "4"),
            ("📍 Location", "5"),
            ("🏥 Clinical Training", "7"),
        ],
        "Admission Info": [
            ("🪑 Seat Availability", "9"),
            ("📊 View Summary", "11"),
        ],
        "Other Actions": [
            ("🤖 Ask AI Assistant", "10"),
            ("🚪 Exit", "0"),
        ]
    }

    st.markdown('<div class="menu-container">', unsafe_allow_html=True)

    category_items = list(menu_categories.items())

    # Create two columns for the expanders
    col1, col2 = st.columns(2)

    # Distribute categories into the two columns
    for i, (category, options) in enumerate(category_items):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            with st.expander(category):
                for label, value in options:
                    if st.button(label, key=f"menu_{value}", use_container_width=True):
                        process_bot_response(value)

    st.markdown('</div>', unsafe_allow_html=True)


def process_bot_response(user_input):
    if st.session_state.bot.current_state != ConversationState.AI_QUERY:
        action_map = {
            "1": "Eligibility Criteria", "2": "Program Details", "3": "Fee Structure",
            "4": "Hostel & Training", "5": "College Location", "6": "Recognition",
            "7": "Clinical Training", "8": "Scholarships", "9": "Seat Availability",
            "10": "AI Assistant", "11": "Complete Summary", "0": "Exit"
        }
        if st.session_state.bot.current_state == ConversationState.LANGUAGE_SELECTION:
            lang_map = {"1": "English", "2": "Hindi", "3": "Hinglish"}
            display_text = lang_map.get(user_input)
        else:
            display_text = action_map.get(user_input)

        if display_text:
            st.session_state.messages.append({'content': display_text, 'is_user': True})

    bot_response = st.session_state.bot.process_message(user_input)
    st.session_state.messages.append({'content': bot_response, 'is_user': False})
    st.rerun()


def handle_ai_input():
    if st.button("🔙 Return to Menu", key="return_menu"):
        process_bot_response("menu")

    st.markdown('<div class="ai-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Message", placeholder="Ask a question...", key="ai_message", label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("Send", type="primary", key="send_ai", use_container_width=True)
        st.markdown(
            '<style>.stButton button[key="send_ai"] { background-color: var(--primary-blue); color: white; border-radius: 12px; border: none; height: 100%; } .stButton button[key="send_ai"]:hover { opacity: 0.9; color: white; border: none;}</style>',
            unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if send_button and user_input.strip():
        st.session_state.messages.append({'content': user_input, 'is_user': True})
        with st.spinner("🤔 Thinking..."):
            bot_response = st.session_state.bot.process_message(user_input)
        st.session_state.messages.append({'content': bot_response, 'is_user': False})
        st.rerun()


def main():
    initialize_session_state()
    st.markdown('<div class="page-title">🏥 Nursing Admission Assistant</div>', unsafe_allow_html=True)

    # Messages Area - directly in the main container without the extra chat-container
    st.markdown('<div class="messages-area">', unsafe_allow_html=True)
    if not st.session_state.conversation_started:
        welcome_message = st.session_state.bot.start_conversation()
        st.session_state.messages.append({'content': welcome_message, 'is_user': False})
        st.session_state.conversation_started = True
        st.rerun()
    else:
        for message in st.session_state.messages:
            display_message(message['content'], message['is_user'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Input/Menu Area
    current_state = st.session_state.bot.current_state
    if current_state == ConversationState.COMPLETED:
        st.markdown('<div class="status-text">Conversation ended.</div>', unsafe_allow_html=True)
    elif current_state == ConversationState.LANGUAGE_SELECTION:
        handle_language_selection()
    elif current_state == ConversationState.MAIN_MENU:
        handle_main_menu()
    elif current_state == ConversationState.AI_QUERY:
        handle_ai_input()

    # Reset Button
    st.markdown('<div class="reset-button-container">', unsafe_allow_html=True)
    if st.button("🔄 Start Over"):
        st.session_state.bot = NursingAdmissionBot()
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
