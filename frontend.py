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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stApp {
        background-color: #121212;
    }

    .main .block-container {
        padding: 2rem 4rem;
        max-width: 1200px;
        margin: 0 auto;
        background-color: #121212;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    .main > div {
        padding-top: 0;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    .chat-message {
        padding: 1.25rem 1.75rem;
        margin: 1rem 0;
        border-radius: 24px;
        max-width: 75%;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        margin-right: 0;
        text-align: right;
        border-bottom-right-radius: 8px;
    }

    .assistant-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 0;
        margin-right: auto;
        text-align: left;
        border-bottom-left-radius: 8px;
    }

    .stButton > button {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #2d3748;
        font-weight: 500;
        font-size: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        height: auto;
        min-height: 60px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }

    .stButton > button:hover {
        background: linear-gradient(145deg, #f7fafc 0%, #edf2f7 100%);
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        color: #4a5568;
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
    }

    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #fed7d7 0%, #feb2b2 100%);
        border: 1px solid #fc8181;
        color: #c53030;
        font-weight: 500;
    }

    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(145deg, #fc8181 0%, #f56565 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 101, 101, 0.25);
    }

    .language-selection .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        border: none;
        font-weight: 600;
        min-height: 70px;
        font-size: 16px;
    }

    .language-selection .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce 0%, #2c5aa0 100%);
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(66, 153, 225, 0.3);
    }

    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 2px solid #e2e8f0;
        padding: 1rem 1.5rem;
        font-size: 15px;
        background: #ffffff !important;
        color: #2d3748 !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        background: #ffffff !important;
        color: #2d3748 !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important;
    }

    .ai-input-container {
        display: flex;
        align-items: flex-end;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    .ai-input-container .stTextInput {
        flex: 1;
        margin-bottom: 0 !important;
    }

    .ai-input-container .stButton {
        margin-bottom: 0 !important;
    }

    .ai-input-container .stButton > button {
        min-height: 50px !important;
        height: 50px !important;
        border-radius: 24px !important;
        padding: 0 2rem !important;
    }

    .status-text {
        color: #e2e8f0;
        font-size: 16px;
        text-align: center;
        margin: 2rem 0 1.5rem 0;
        font-weight: 400;
        letter-spacing: 0.025em;
    }

    .page-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 3rem 0;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .chat-container {
        min-height: 60vh;
        background: #ffffff;
        border-radius: 24px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .menu-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .main-content {
        padding-bottom: 2rem;
    }

    .stSpinner > div {
        border-color: #667eea !important;
    }

    .conversation-container {
        background: #ffffff;
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 2rem;
        }
        
        .chat-message {
            max-width: 90%;
            padding: 1rem 1.25rem;
            font-size: 14px;
        }
        
        .page-title {
            font-size: 24px;
            margin: 1rem 0 2rem 0;
        }
        
        .conversation-container {
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
    }

    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'bot' not in st.session_state:
        st.session_state.bot = NursingAdmissionBot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'ai_mode' not in st.session_state:
        st.session_state.ai_mode = False

def display_message(message, is_user=False):
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            {message.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

def handle_language_selection():
    st.markdown('<div class="status-text">Please select your preferred language</div>', unsafe_allow_html=True)

    st.markdown('<div class="language-selection">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        if st.button("English", key="lang_en"):
            process_bot_response("1")

    with col2:
        if st.button("हिंदी", key="lang_hi"):
            process_bot_response("2")

    with col3:
        if st.button("Hinglish", key="lang_hinglish"):
            process_bot_response("3")

    st.markdown('</div>', unsafe_allow_html=True)

def create_menu_button(label, value, help_text=""):
    button_html = f"""
    <div class="menu-button" onclick="selectOption('{value}')" title="{help_text}">
        {label}
    </div>
    """
    return button_html

def handle_main_menu():
    st.markdown('<div class="status-text">What would you like to know about our B.Sc Nursing Program?</div>', unsafe_allow_html=True)

    menu_options = [
        ("Eligibility Criteria", "1"),
        ("Program Details", "2"),
        ("Fee Structure", "3"),
        ("Hostel & Training", "4"),
        ("College Location", "5"),
        ("Recognition & Accreditation", "6"),
        ("Clinical Training", "7"),
        ("Scholarship Options", "8"),
        ("Seat Availability", "9"),
        ("Complete Summary", "11"),
        ("Ask AI Assistant", "10"),
        ("Exit Conversation", "0")
    ]

    col1, col2 = st.columns(2, gap="medium")

    for i, (label, value) in enumerate(menu_options):
        with col1 if i % 2 == 0 else col2:
            if st.button(label, key=f"menu_{value}"):
                process_bot_response(value)

def process_bot_response(user_input):
    if user_input not in ["1", "2", "3"] or st.session_state.bot.current_state != ConversationState.LANGUAGE_SELECTION:
        action_map = {
            "1": "Eligibility Criteria" if st.session_state.bot.current_state == ConversationState.MAIN_MENU else "English",
            "2": "Program Details" if st.session_state.bot.current_state == ConversationState.MAIN_MENU else "Hindi",
            "3": "Fee Structure" if st.session_state.bot.current_state == ConversationState.MAIN_MENU else "Hinglish",
            "4": "Hostel & Training",
            "5": "College Location",
            "6": "Recognition & Accreditation",
            "7": "Clinical Training",
            "8": "Scholarship Options",
            "9": "Seat Availability",
            "10": "AI Assistant",
            "11": "Complete Summary",
            "0": "Exit"
        }

        display_text = action_map.get(user_input, user_input)
        st.session_state.messages.append({
            'content': display_text,
            'is_user': True
        })

    bot_response = st.session_state.bot.process_message(user_input)

    st.session_state.messages.append({
        'content': bot_response,
        'is_user': False
    })

    if st.session_state.bot.current_state == ConversationState.AI_QUERY:
        st.session_state.ai_mode = True
    else:
        st.session_state.ai_mode = False

    st.rerun()

def handle_ai_input():
    st.markdown('<div class="status-text">AI Assistant Mode - Ask me anything about the nursing program</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Return to Menu", key="return_menu", type="primary"):
            process_bot_response("menu")

def render_bottom_input():
    if st.session_state.bot.current_state == ConversationState.AI_QUERY:
        st.markdown("---")

        st.markdown('<div class="ai-input-container">', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1], gap="small")

        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Type your question here...",
                key="ai_message",
                label_visibility="collapsed"
            )

        with col2:
            send_button = st.button("Send", type="primary", key="send_ai")

        st.markdown('</div>', unsafe_allow_html=True)

        if send_button and user_input.strip():
            st.session_state.messages.append({
                'content': user_input,
                'is_user': True
            })

            with st.spinner("Thinking..."):
                bot_response = st.session_state.bot.process_message(user_input)

            st.session_state.messages.append({
                'content': bot_response,
                'is_user': False
            })

            st.rerun()

def main():
    initialize_session_state()

    st.markdown('<div class="page-title">Nursing College Admission Assistant</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="conversation-container">', unsafe_allow_html=True)

        if st.session_state.messages:
            for message in st.session_state.messages:
                display_message(message['content'], message['is_user'])
        else:
            if not st.session_state.conversation_started:
                welcome_message = st.session_state.bot.start_conversation()
                st.session_state.messages.append({
                    'content': welcome_message,
                    'is_user': False
                })
                st.session_state.conversation_started = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.bot.current_state == ConversationState.COMPLETED:
            st.markdown('<div class="status-text">Conversation completed. Thank you for using our service!</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Start New Conversation", type="primary"):
                    st.session_state.bot = NursingAdmissionBot()
                    st.session_state.messages = []
                    st.session_state.conversation_started = False
                    st.session_state.ai_mode = False
                    st.rerun()

        elif st.session_state.bot.current_state == ConversationState.LANGUAGE_SELECTION:
            handle_language_selection()

        elif st.session_state.bot.current_state == ConversationState.MAIN_MENU:
            handle_main_menu()

        elif st.session_state.bot.current_state == ConversationState.AI_QUERY:
            handle_ai_input()

    if st.session_state.bot.current_state == ConversationState.AI_QUERY:
        render_bottom_input()

    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Reset Conversation", type="secondary"):
            st.session_state.bot = NursingAdmissionBot()
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.session_state.ai_mode = False
            st.rerun()

if __name__ == "__main__":
    main()