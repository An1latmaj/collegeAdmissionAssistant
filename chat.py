from enum import Enum
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import streamlit as st
import re
from typing import List, Dict


class ConversationState(Enum):
    LANGUAGE_SELECTION = "language_selection"
    MAIN_MENU = "main_menu"
    ELIGIBILITY_INFO = "eligibility_info"
    PROGRAM_DETAILS = "program_details"
    FEE_STRUCTURE = "fee_structure"
    HOSTEL_TRAINING = "hostel_training"
    LOCATION_INFO = "location_info"
    RECOGNITION_INFO = "recognition_info"
    CLINICAL_TRAINING = "clinical_training"
    SCHOLARSHIP_INFO = "scholarship_info"
    SEAT_AVAILABILITY = "seat_availability"
    AI_QUERY = "ai_query"
    COMPLETED = "completed"


class CollegeInfoRAG:
    def __init__(self, info_file_path: str = "college_info.txt"):
        self.info_file_path = info_file_path
        self.college_info = self._load_college_info()
        self.sections = self._parse_sections()

    def _load_college_info(self) -> str:
        """Load college information from text file"""
        try:
            with open(self.info_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "College information file not found."

    def _parse_sections(self) -> Dict[str, str]:
        """Parse the college info into sections for better retrieval"""
        sections = {}
        current_section = ""
        current_content = []

        for line in self.college_info.split('\n'):
            line = line.strip()
            if line and line.isupper() and line.endswith(':'):
                if current_section:
                    sections[current_section.lower()] = '\n'.join(current_content)
                current_section = line[:-1]  # Remove the colon
                current_content = []
            elif line:
                current_content.append(line)

        if current_section:
            sections[current_section.lower()] = '\n'.join(current_content)

        return sections

    def retrieve_relevant_info(self, query: str) -> str:
        """Retrieve relevant information based on query keywords"""
        query_lower = query.lower()
        relevant_sections = []

        # Define keyword mappings to sections
        keyword_mappings = {
            'eligibility': ['eligibility criteria'],
            'biology': ['eligibility criteria'],
            'age': ['eligibility criteria'],
            'qualify': ['eligibility criteria'],
            'योग्यता': ['eligibility criteria'],

            'fee': ['fee structure'],
            'cost': ['fee structure'],
            'price': ['fee structure'],
            'money': ['fee structure'],
            'payment': ['fee structure'],
            'फीस': ['fee structure'],
            'पैसा': ['fee structure'],

            'program': ['program details'],
            'course': ['program details'],
            'curriculum': ['program details'],
            'study': ['program details'],
            'duration': ['program details'],
            'years': ['program details'],

            'hostel': ['hostel and training facilities'],
            'accommodation': ['hostel and training facilities'],
            'facility': ['hostel and training facilities'],
            'training': ['hostel and training facilities', 'clinical training locations'],

            'location': ['location'],
            'where': ['location'],
            'delhi': ['location'],
            'address': ['location'],
            'स्थान': ['location'],

            'recognition': ['recognition and accreditation'],
            'accreditation': ['recognition and accreditation'],
            'inc': ['recognition and accreditation'],
            'valid': ['recognition and accreditation'],

            'clinical': ['clinical training locations'],
            'hospital': ['clinical training locations'],
            'practical': ['clinical training locations'],

            'scholarship': ['scholarships'],
            'financial': ['scholarships'],
            'help': ['scholarships'],
            'छात्रवृत्ति': ['scholarships'],

            'seat': ['seat availability'],
            'admission': ['seat availability'],
            'available': ['seat availability'],
            'vacancy': ['seat availability'],

            'advantage': ['college advantages'],
            'benefit': ['college advantages'],
            'why': ['college advantages'],
            'choose': ['college advantages'],
            'best': ['college advantages'],
            'special': ['college advantages'],
            'unique': ['college advantages']
        }

        # Find relevant sections based on keywords
        matched_sections = set()
        for keyword, sections in keyword_mappings.items():
            if keyword in query_lower:
                matched_sections.update(sections)

        # If no specific keywords found, return a general overview
        if not matched_sections:
            return self._get_general_overview()

        # Retrieve content for matched sections
        for section_name in matched_sections:
            if section_name in self.sections:
                relevant_sections.append(f"{section_name.upper()}:\n{self.sections[section_name]}")

        return '\n\n'.join(relevant_sections) if relevant_sections else self._get_general_overview()

    def _get_general_overview(self) -> str:
        """Return a general overview of the college"""
        overview_sections = ['program details', 'eligibility criteria', 'fee structure']
        overview = []
        for section in overview_sections:
            if section in self.sections:
                overview.append(f"{section.upper()}:\n{self.sections[section]}")
        return '\n\n'.join(overview)

    def get_section(self, section_name: str) -> str:
        """Get specific section by name"""
        return self.sections.get(section_name.lower(), "Section not found.")


class NursingAdmissionBot:
    def __init__(self):
        # Get API credentials from Streamlit secrets
        try:
            self.api_key = st.secrets["AZURE_API"]
            self.endpoint = st.secrets["AZURE_ENDPOINT"]
        except KeyError as e:
            st.error(f"Missing secret key: {e}. Please add AZURE_API and AZURE_ENDPOINT to your Streamlit secrets.")
            st.stop()
        
        self.model_name = "Llama-4-Maverick-17B-128E-Instruct-FP8"

        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            api_version="2024-05-01-preview"
        )

        # Initialize RAG system
        self.rag_system = CollegeInfoRAG()

        self.responses = self.create_responses()
        self.conversation_history = []
        self.current_state = ConversationState.LANGUAGE_SELECTION
        self.selected_language = 'en'

    def create_responses(self):
        return {
            'language_selection': {
                'prompt': """
🏥 Welcome to Nursing College Admission Assistant! 🏥

Please select your preferred language / कृपया अपनी पसंदीदा भाषा चुनें:

1. English
2. हिंदी (Hindi)
3. Hinglish (Hindi + English)

 """
            },

            'main_menu': {
                'en': """
🏥 NURSING COLLEGE ADMISSION INFORMATION 🏥

What would you like to know about our B.Sc Nursing Program?

1. 📋 Eligibility Criteria
2. 📚 Program Details
3. 💰 Fee Structure
4. 🏠 Hostel & Training Facilities
5. 📍 College Location
6. ✅ Recognition & Accreditation
7. 🏥 Clinical Training Locations
8. 🎓 Scholarship Options
9. 🪑 Seat Availability
10. ❓ Ask Any Question (AI Assistant)
11. 📊 View Summary of All Information
0. 🚪 Exit

 """,

                'hi': """
🏥 नर्सिंग कॉलेज प्रवेश की जानकारी 🏥

आप हमारे B.Sc Nursing Program के बारे में क्या जानना चाहते हैं?

1. 📋 योग्यता मापदंड (Eligibility Criteria)
2. 📚 प्रोग्राम विवरण (Program Details)
3. 💰 फीस संरचना (Fee Structure)
4. 🏠 हॉस्टल और प्रशिक्षण सुविधाएं
5. 📍 कॉलेज स्थान (College Location)
6. ✅ मान्यता और प्रत्यायन
7. 🏥 क्लिनिकल प्रशिक्षण स्थान
8. 🎓 छात्रवृत्ति विकल्प
9. 🪑 सीट उपलब्धता
10. ❓ कोई भी प्रश्न पूछें (AI सहायक)
11. 📊 सभी जानकारी का सारांश देखें
0. 🚪 बाहर निकलें
 """,

                'hinglish': """
🏥 NURSING COLLEGE ADMISSION INFORMATION 🏥

Aap hamare B.Sc Nursing Program ke baare mein kya jaanna chahte hain?

1. 📋 Eligibility Criteria (योग्यता मापदंड)
2. 📚 Program Details (प्रोग्राम विवरण)
3. 💰 Fee Structure (फीस संरचना)
4. 🏠 Hostel aur Training Facilities
5. 📍 College Location (कॉलेज स्थान)
6. ✅ Recognition aur Accreditation
7. 🏥 Clinical Training Locations
8. 🎓 Scholarship Options (छात्रवृत्ति)
9. 🪑 Seat Availability (सीट उपलब्धता)
10. ❓ Koi bhi question puchiye (AI Assistant)
11. 📊 Sab information ka summary dekhiye
0. 🚪 Exit karne ke liye
 """
            },

            'eligibility_criteria': {
                'en': self.rag_system.get_section('eligibility criteria'),
                'hi': self.rag_system.get_section('eligibility criteria'),
                'hinglish': self.rag_system.get_section('eligibility criteria')
            },

            'program_details': {
                'en': self.rag_system.get_section('program details'),
                'hi': self.rag_system.get_section('program details'),
                'hinglish': self.rag_system.get_section('program details')
            },

            'fee_structure': {
                'en': self.rag_system.get_section('fee structure'),
                'hi': self.rag_system.get_section('fee structure'),
                'hinglish': self.rag_system.get_section('fee structure')
            },

            'hostel_training': {
                'en': self.rag_system.get_section('hostel and training facilities'),
                'hi': self.rag_system.get_section('hostel and training facilities'),
                'hinglish': self.rag_system.get_section('hostel and training facilities')
            },

            'location_info': {
                'en': self.rag_system.get_section('location'),
                'hi': self.rag_system.get_section('location'),
                'hinglish': self.rag_system.get_section('location')
            },

            'recognition_info': {
                'en': self.rag_system.get_section('recognition and accreditation'),
                'hi': self.rag_system.get_section('recognition and accreditation'),
                'hinglish': self.rag_system.get_section('recognition and accreditation')
            },

            'clinical_training': {
                'en': self.rag_system.get_section('clinical training locations'),
                'hi': self.rag_system.get_section('clinical training locations'),
                'hinglish': self.rag_system.get_section('clinical training locations')
            },

            'scholarship_info': {
                'en': self.rag_system.get_section('scholarships'),
                'hi': self.rag_system.get_section('scholarships'),
                'hinglish': self.rag_system.get_section('scholarships')
            },

            'seat_availability': {
                'en': self.rag_system.get_section('seat availability'),
                'hi': self.rag_system.get_section('seat availability'),
                'hinglish': self.rag_system.get_section('seat availability')
            },

            'exit_message': {
                'en': "Thank you for using our Nursing College Admission Assistant! For more information, please contact our admission office. Good luck with your nursing career! 🏥",
                'hi': "हमारे नर्सिंग कॉलेज एडमिशन असिस्टेंट का उपयोग करने के लिए धन्यवाद! अधिक जानकारी के लिए, कृपया हमारे एडमिशन ऑफिस से संपर्क करें। आपके नर्सिंग करियर के लिए शुभकामनाएं! 🏥",
                'hinglish': "Hamare Nursing College Admission Assistant ka use karne ke liye thank you! More information ke liye, please hamare admission office se contact kariye. Aapke nursing career ke liye best of luck! 🏥"
            },

            'invalid_option': {
                'en': "❌ Invalid option. Please enter a number from the menu options.",
                'hi': "❌ गलत विकल्प। कृपया मेनू विकल्पों में से कोई संख्या दर्ज करें।",
                'hinglish': "❌ Invalid option. Please menu options mein se koi number enter kariye."
            },

            'ai_prompt': {
                'en': "🤖 AI Assistant Ready!\n\nAsk me anything about the nursing program, admission process, or any related queries.\nI have all the information about eligibility, fees, facilities, etc.\n\nYour question: ",
                'hi': "🤖 AI सहायक तैयार!\n\nनर्सिंग प्रोग्राम, एडमिशन प्रक्रिया, या किसी भी संबंधित प्रश्न के बारे में मुझसे कुछ भी पूछें।\nमेरे पास योग्यता, फीस, सुविधाओं आदि की सभी जानकारी है।\n\nआपका प्रश्न: ",
                'hinglish': "🤖 AI Assistant Ready!\n\nNursing program, admission process, ya koi bhi related queries ke baare mein mujhse kuch bhi puchiye.\nMere paas eligibility, fees, facilities, etc. ki saari information hai.\n\nAapka question: "
            }
        }

    def process_message(self, user_input: str) -> str:
        if self.current_state == ConversationState.LANGUAGE_SELECTION:
            return self.handle_language_selection(user_input)
        elif self.current_state == ConversationState.MAIN_MENU:
            return self.handle_main_menu(user_input)
        elif self.current_state == ConversationState.AI_QUERY:
            return self.handle_ai_query(user_input)
        else:
            self.current_state = ConversationState.MAIN_MENU
            return self.show_main_menu()

    def handle_language_selection(self, user_input: str) -> str:
        if user_input.strip() == '1':
            self.selected_language = 'en'
        elif user_input.strip() == '2':
            self.selected_language = 'hi'
        elif user_input.strip() == '3':
            self.selected_language = 'hinglish'
        else:
            return "❌ Please enter 1, 2, or 3 to select your language / कृपया अपनी भाषा चुनने के लिए 1, 2, या 3 दर्ज करें"

        self.current_state = ConversationState.MAIN_MENU
        return self.show_main_menu()

    def handle_main_menu(self, user_input: str) -> str:
        try:
            choice = int(user_input.strip())
        except ValueError:
            return self.responses['invalid_option'][self.selected_language]

        if choice == 0:
            self.current_state = ConversationState.COMPLETED
            return self.responses['exit_message'][self.selected_language]
        elif choice == 1:
            return self.responses['eligibility_criteria'][self.selected_language]
        elif choice == 2:
            return self.responses['program_details'][self.selected_language]
        elif choice == 3:
            return self.responses['fee_structure'][self.selected_language]
        elif choice == 4:
            return self.responses['hostel_training'][self.selected_language]
        elif choice == 5:
            return self.responses['location_info'][self.selected_language]
        elif choice == 6:
            return self.responses['recognition_info'][self.selected_language]
        elif choice == 7:
            return self.responses['clinical_training'][self.selected_language]
        elif choice == 8:
            return self.responses['scholarship_info'][self.selected_language]
        elif choice == 9:
            return self.responses['seat_availability'][self.selected_language]
        elif choice == 10:
            self.current_state = ConversationState.AI_QUERY
            return self.responses['ai_prompt'][self.selected_language]
        elif choice == 11:
            return self.show_summary()
        else:
            return self.responses['invalid_option'][self.selected_language]

    def handle_ai_query(self, user_input: str) -> str:
        if user_input.lower() in ['menu', 'back', 'return', 'मेनू', 'वापस', 'exit']:
            self.current_state = ConversationState.MAIN_MENU
            return self.show_main_menu()

        try:
            ai_response = self.generate_ai_response(user_input)

            menu_prompt = {
                'en': "\n\nType 'menu' to return to main menu or ask another question: ",
                'hi': "\n\nमुख्य मेनू पर वापस जाने के लिए 'menu' टाइप करें या कोई और सवाल पूछें: ",
                'hinglish': "\n\nMain menu par wapas jaane ke liye 'menu' type kariye ya koi aur question puchiye: "
            }

            return ai_response + menu_prompt[self.selected_language]

        except Exception as e:
            print(f"AI Error: {str(e)}")
            return self.get_fallback_response(user_input)

    def generate_ai_response(self, user_query: str) -> str:
        try:
            # Retrieve relevant information using RAG
            relevant_info = self.rag_system.retrieve_relevant_info(user_query)

            system_prompt = self.get_streamlined_system_prompt(relevant_info)

            messages = [
                {"role": "system", "content": system_prompt}
            ]

            if self.conversation_history:
                messages.extend(self.conversation_history[-4:])

            messages.append({"role": "user", "content": user_query})

            self.conversation_history.append({"role": "user", "content": user_query})

            response = self.client.complete(
                messages=messages,
                model=self.model_name,
                temperature=0.7,
                max_tokens=600,
                top_p=0.9
            )

            ai_response = response.choices[0].message.content

            self.conversation_history.append({"role": "assistant", "content": ai_response})

            return ai_response

        except Exception as e:
            print(f"AI Generation Error: {str(e)}")
            return self.get_fallback_response(user_query)

    def get_streamlined_system_prompt(self, relevant_info: str) -> str:
        """Streamlined system prompt with RAG-retrieved information"""
        language_map = {'hi': 'Hindi', 'en': 'English', 'hinglish': 'Hinglish (Hindi-English mix)'}

        return f"""You are an AI admission counselor for a Nursing College. Always respond in {language_map[self.selected_language]}.

RELEVANT COLLEGE INFORMATION:
{relevant_info}

CONVERSATION PHASES:
1. Greeting & Language Selection
2. Main Menu Navigation
3. Information Delivery
4. AI Assistant Mode
5. Conversation Closure

ROLES & GUIDELINES:
- Be professional, helpful, and concise
- Provide accurate information only from the given context
- If asked about topics not in the context, redirect: "I can only answer questions related to the nursing program and admission process"
- Always maintain the specified language throughout
- Ask follow-up questions to guide the conversation forward

INTENT DETECTION EXAMPLES:

### POSITIVE INTENT:
**User**: "Haan batao college ke baare mein"
**Detection**: Positive (contains "Haan" + "batao")
**Action**: Continue to next conversation step

**User**: "Kitna fees hai?"
**Detection**: Positive (direct question about program)
**Action**: Answer the question and continue flow

**User**: "Yes bro, tell me about hostel facilities"
**Detection**: Positive (yes + specific request)
**Action**: Continue with requested information

### NEGATIVE INTENT:
**User**: "Nahi yaar, not interested"
**Detection**: Negative (contains "Nahi" + "not interested")
**Action**: Polite conversation closure

### UNCLEAR INTENT:
**User**: "Hmm, pata nahi"
**Detection**: Unclear (hesitation words)
**Action**: Ask for clarification: "Would you like to know more about our nursing program, or shall we end our conversation here?"

CONVERSATION CLOSURE EXAMPLES:

### For Negative Intent:
"I understand you're not interested right now. That's completely fine! If you ever want to learn about our nursing program in the future, I'll be here to help. Take care!"

### For Neutral/Polite Decline:
"Thank you for your time. If you have any questions about nursing education later, please don't hesitate to ask. Wishing you all the best!"
"""

    def get_fallback_response(self, user_query: str) -> str:
        """Fallback response using RAG for better information retrieval"""
        # Try to get relevant info using RAG even for fallback
        relevant_info = self.rag_system.retrieve_relevant_info(user_query)

        if relevant_info and relevant_info != self.rag_system._get_general_overview():
            return relevant_info

        fallback_responses = {
            'en': "I can help you with information about our B.Sc Nursing program including eligibility, fees, scholarships, facilities, and more. Please ask a specific question about the nursing program.",
            'hi': "मैं आपको हमारे B.Sc नर्सिंग प्रोग्राम के बारे में जानकारी दे सकता हूं जिसमें योग्यता, फीस, छात्रवृत्ति, सुविधाएं और बहुत कुछ शामिल है। कृपया नर्सिंग प्रोग्राम के बारे में कोई विशिष्ट प्रश्न पूछें।",
            'hinglish': "Main aapko hamare B.Sc Nursing program ke baare mein information de sakta hun including eligibility, fees, scholarships, facilities aur bahut kuch. Please nursing program ke baare mein koi specific question puchiye."
        }
        return fallback_responses[self.selected_language]

    def show_main_menu(self) -> str:
        return self.responses['main_menu'][self.selected_language]

    def show_summary(self) -> str:
        # Use RAG to get comprehensive summary
        summary_info = self.rag_system._get_general_overview()
        return f"📊 COMPLETE INFORMATION SUMMARY - B.Sc NURSING\n\n{summary_info}\n\nPress Enter to return to main menu..."

    def start_conversation(self) -> str:
        return self.responses['language_selection']['prompt']


def main():
    """Console version of the chatbot for testing"""
    print("Testing Nursing Admission Bot...")
    bot = NursingAdmissionBot()

    while bot.current_state != ConversationState.COMPLETED:
        try:
            user_input = input().strip()

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(f"\nAssistant: {bot.responses['exit_message'][bot.selected_language]}")
                break

            if not user_input:
                continue

            response = bot.process_message(user_input)
            print(f"\nAssistant: {response}")

        except KeyboardInterrupt:
            print(f"\n\nAssistant: {bot.responses['exit_message'][bot.selected_language]}")
            break
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_messages = {
                'en': "Sorry, there was an issue. Please try again.",
                'hi': "क्षमा करें, कुछ समस्या हुई है। कृपया दोबारा कोशिश करें।",
                'hinglish': "Sorry, kuch problem hui hai. Please dobara try kariye."
            }
            print(f"Assistant: {error_messages[bot.selected_language]}")


if __name__ == "__main__":
    main()
