from enum import Enum
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List, Optional
import os
import re
import streamlit as st

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

class NursingAdmissionBot:
    def __init__(self):
        # Use Streamlit secrets management
        try:
            self.api_key = st.secrets["AZURE_API"]
            self.endpoint = st.secrets["AZURE_ENDPOINT"]
        except KeyError as e:
            st.error(f"Missing required secret: {e}")
            st.stop()
        except Exception:
            # Fallback to environment variables for local development
            self.api_key = os.getenv("AZURE_API")
            self.endpoint = os.getenv("AZURE_ENDPOINT")

            if not self.api_key or not self.endpoint:
                st.error("Azure credentials not found. Please configure Streamlit secrets or environment variables.")
                st.stop()

        self.model_name = "Llama-4-Maverick-17B-128E-Instruct-FP8"

        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            api_version="2024-05-01-preview"
        )

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
                'en': """
📋 ELIGIBILITY CRITERIA FOR B.Sc NURSING ADMISSION

✅ MANDATORY REQUIREMENTS:
• Biology in 12th grade (COMPULSORY - बायोलॉजी अनिवार्य है)
• Age: 17 to 35 years
• Must pass PNT Exam
• Valid 12th grade marksheet required
• Medical fitness certificate

⚠️ IMPORTANT NOTE:
"B.Sc Nursing mein admission ke liye Biology avashyak hai"
- If you studied any other subject instead of Biology, admission is not possible

🎯 Selection Process:
• Merit-based selection
• First come, first served (after meeting eligibility)
• Limited seats available (60 total)

Press Enter to return to main menu...""",

                'hi': """
📋 B.Sc नर्सिंग प्रवेश के लिए योग्यता मापदंड

✅ अनिवार्य आवश्यकताएं:
• 12वीं कक्षा में बायोलॉजी (अनिवार्य)
• आयु: 17 से 35 वर्ष
• PNT परीक्षा पास करना आवश्यक
• वैध 12वीं कक्षा की मार्कशीट आवश्यक
• मेडिकल फिटनेस सर्टिफिकेट

⚠️ महत्वपूर्ण नोट:
"B.Sc Nursing में admission के लिए Biology अवश्यक है"
- यदि आपने Biology के बजाय कोई अन्य विषय पढ़ा है तो प्रवेश संभव नहीं है

🎯 चयन प्रक्रिया:
• मेरिट आधारित चयन
• पहले आओ, पहले पाओ (योग्यता पूरी करने के बाद)
• सीमित सीटें उपलब्ध (कुल 60)

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
📋 B.Sc NURSING ADMISSION KE LIYE ELIGIBILITY CRITERIA

✅ MANDATORY REQUIREMENTS:
• 12th grade mein Biology (COMPULSORY - बायोलॉजी अनिवार्य है)
• Age: 17 to 35 years
• PNT Exam pass karna zaroori hai
• Valid 12th grade marksheet required
• Medical fitness certificate

⚠️ IMPORTANT NOTE:
"B.Sc Nursing mein admission ke liye Biology avashyak hai"
- Agar aapne Biology ke bajay koi aur subject padha hai to admission possible nahi hai

🎯 Selection Process:
• Merit-based selection
• First come, first served (eligibility meet karne ke baad)
• Limited seats available (total 60)

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'program_details': {
                'en': """
📚 B.Sc NURSING PROGRAM DETAILS

🎓 Program Overview:
• Full name: Bachelor of Science in Nursing
• Duration: 4 years (full-time)
• Type: Professional degree course
• Medium: English

📖 Curriculum Structure:
• Theoretical classes: Nursing fundamentals, anatomy, physiology
• Practical training: Hands-on experience with real patients
• Hospital training: Included throughout the program
• Clinical rotations: Various medical specialties

🏥 Training Experience:
• Work with real patients under supervision
• Learn from experienced nursing professionals
• Exposure to different medical departments
• Develop practical nursing skills

🎯 Career Opportunities:
• Hospital nursing positions
• Community health centers
• Government nursing jobs
• Private healthcare facilities
• Further studies: M.Sc Nursing, specialized courses

Press Enter to return to main menu...""",

                'hi': """
📚 B.Sc नर्सिंग प्रोग्राम विवरण

🎓 प्रोग्राम अवलोकन:
• पूरा नाम: Bachelor of Science in Nursing
• अवधि: 4 साल (पूर्णकालिक)
• प्रकार: व्यावसायिक डिग्री कोर्स
• माध्यम: अंग्रेजी

📖 पाठ्यक्रम संरचना:
• सैद्धांतिक कक्षाएं: नर्सिंग मूल बातें, शरीर रचना, शरीर विज्ञान
• व्यावहारिक प्रशिक्षण: वास्तविक रोगियों के साथ अनुभव
• अस्पताल प्रशिक्षण: पूरे कार्यक्रम में शामिल
• क्लिनिकल रोटेशन: विभिन्न चिकित्सा विशेषताएं

🏥 प्रशिक्षण अनुभव:
• निरीक्षण में वास्तविक रोगियों के साथ काम
• अनुभवी नर्सिंग पेशेवरों से सीखना
• विभिन्न चिकित्सा विभागों का एक्सपोजर
• व्यावहारिक नर्सिंग कौशल विकसित करना

🎯 करियर अवसर:
• अस्पताल नर्सिंग पद
• सामुदायिक स्वास्थ्य केंद्र
• सरकारी नर्सिंग नौकरियां
• निजी स्वास्थ्य सुविधाएं
• आगे की पढ़ाई: M.Sc नर्सिंग, विशेष कोर्स

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
📚 B.Sc NURSING PROGRAM DETAILS

🎓 Program Overview:
• Full name: Bachelor of Science in Nursing
• Duration: 4 saal (full-time)
• Type: Professional degree course
• Medium: English

📖 Curriculum Structure:
• Theoretical classes: Nursing fundamentals, anatomy, physiology
• Practical training: Real patients ke saath hands-on experience
• Hospital training: Poore program mein included
• Clinical rotations: Various medical specialties

🏥 Training Experience:
• Supervision mein real patients ke saath kaam
• Experienced nursing professionals se seekhna
• Different medical departments ka exposure
• Practical nursing skills develop karna

🎯 Career Opportunities:
• Hospital nursing positions
• Community health centers
• Government nursing jobs
• Private healthcare facilities
• Further studies: M.Sc Nursing, specialized courses

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'fee_structure': {
                'en': """
💰 FEE STRUCTURE - B.Sc NURSING (Annual)

💳 Fee Breakdown:
• Tuition Fee: ₹60,000 INR
• Bus Fee: ₹10,000 INR
• TOTAL ANNUAL FEES: ₹70,000 INR

📅 Payment Schedule (3 Installments):
• 1st Installment: ₹30,000 (Due at admission time)
• 2nd Installment: ₹20,000 (Due after 1st semester)
• 3rd Installment: ₹20,000 (Due after 2nd semester)

💡 Payment Benefits:
• Installment facility available
• No hidden charges
• Transparent fee structure
• Payment flexibility for families

💸 Additional Costs (Optional):
• Hostel fees (if staying in hostel)
• Personal expenses
• Books and study materials

📋 Fee Payment Methods:
• Online payment accepted
• Bank transfer available
• Demand draft accepted

Press Enter to return to main menu...""",

                'hi': """
💰 फीस संरचना - B.Sc नर्सिंग (वार्षिक)

💳 फीस विवरण:
• ट्यूशन फीस: ₹60,000 INR
• बस फीस: ₹10,000 INR
• कुल वार्षिक फीस: ₹70,000 INR

📅 भुगतान अनुसूची (3 किस्तें):
• पहली किस्त: ₹30,000 (प्रवेश के समय देय)
• दूसरी किस्त: ₹20,000 (पहले सेमेस्टर के बाद देय)
• तीसरी किस्त: ₹20,000 (दूसरे सेमेस्टर के बाद देय)

💡 भुगतान लाभ:
• किस्त की सुविधा उपलब्ध
• कोई छुपे हुए शुल्क नहीं
• पारदर्शी फीस संरचना
• परिवारों के लिए भुगतान लचीलापन

💸 अतिरिक्त लागत (वैकल्पिक):
• हॉस्टल फीस (यदि हॉस्टल में रहते हैं)
• व्यक्तिगत खर्च
• किताबें और अध्ययन सामग्री

📋 फीस भुगतान के तरीके:
• ऑनलाइन भुगतान स्वीकार किया जाता है
• बैंक ट्रांसफर उपलब्ध
• डिमांड ड्राफ्ट स्वीकार किया जाता है

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
💰 FEE STRUCTURE - B.Sc NURSING (Annual)

💳 Fee Breakdown:
• Tuition Fee: ₹60,000 INR
• Bus Fee: ₹10,000 INR
• TOTAL ANNUAL FEES: ₹70,000 INR

📅 Payment Schedule (3 Installments):
• 1st Installment: ₹30,000 (Admission ke time due)
• 2nd Installment: ₹20,000 (1st semester ke baad due)
• 3rd Installment: ₹20,000 (2nd semester ke baad due)

💡 Payment Benefits:
• Installment facility available hai
• Koi hidden charges nahi
• Transparent fee structure
• Families ke liye payment flexibility

💸 Additional Costs (Optional):
• Hostel fees (agar hostel mein rehte hain)
• Personal expenses
• Books aur study materials

📋 Fee Payment Methods:
• Online payment accepted
• Bank transfer available
• Demand draft accepted

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'hostel_training': {
                'en': """
🏠 HOSTEL & TRAINING FACILITIES

🏨 Hostel Facilities:
• 24x7 water and electricity supply
• CCTV surveillance for security
• Warden available on-site for student support
• Safe and comfortable living environment

🏥 Training Facilities:
• Hospital training included with real patients
• Hands-on practical experience
• Professional guidance during training

Press Enter to return to main menu...""",

                'hi': """
🏠 हॉस्टल और प्रशिक्षण सुविधाएं

🏨 हॉस्टल सुविधाएं:
• 24x7 पानी और बिजली की आपूर्ति
• सुरक्षा के लिए सीसीटीवी निगरानी
• छात्र सहायता के लिए वार्डन उपलब्ध
• सुरक्षित और आरामदायक रहने का वातावरण

🏥 प्रशिक्षण सुविधाएं:
• वास्तविक रोगियों के साथ अस्पताल प्रशिक्षण शामिल है
• व्यावहारिक अनुभव
• प्रशिक्षण के दौरान पेशेवर मार्गदर्शन

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
🏠 HOSTEL & TRAINING FACILITIES

🏨 Hostel Facilities:
• 24x7 water aur electricity supply
• CCTV surveillance for security
• Warden available on-site student support ke liye
• Safe aur comfortable living environment

🏥 Training Facilities:
• Hospital training included hai real patients ke saath
• Hands-on practical experience
• Professional guidance during training

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'location_info': {
                'en': """
📍 COLLEGE LOCATION

Our college is located in Delhi, which is an excellent city for nursing education due to its numerous hospitals and healthcare facilities.

Benefits of Delhi location:
• Metro connectivity for easy transportation
• Practical training opportunities with multiple hospitals
• Modern healthcare infrastructure
• Career opportunities after graduation

Press Enter to return to main menu...""",

                'hi': """
📍 कॉलेज स्थान

हमारा कॉलेज दिल्ली में स्थित है, जो नर्सिंग शिक्षा के लिए एक उत्कृष्ट शहर है क्योंकि यहाँ कई अस्पताल और स्वास्थ्य सुविधाएं हैं।

दिल्ली स्थान के फायदे:
• आसान परिवहन के लिए मेट्रो कनेक्टिविटी
• कई अस्पतालों के साथ व्यावहारिक प्रशिक्षण के अवसर
• आधुनिक स्वास्थ्य देखभाल बुनियादी ढांचा
• स्नातक के बाद करियर के अवसर

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
📍 COLLEGE LOCATION

Hamara college Delhi mein located hai, jo nursing education ke liye ek excellent city hai kyunki yahan bahut saare hospitals aur healthcare facilities hain.

Delhi location ke fayde:
• Easy transportation ke liye Metro connectivity
• Multiple hospitals ke saath practical training opportunities
• Modern healthcare infrastructure
• Career opportunities after graduation

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'recognition_info': {
                'en': """
✅ RECOGNITION & ACCREDITATION

Our Nursing College is recognized by the Indian Nursing Council (INC) Delhi.

Benefits of INC Recognition:
• Validates your degree nationally
• Eligibility for government jobs
• Ability to practice anywhere in India

Press Enter to return to main menu...""",

                'hi': """
✅ मान्यता और प्रत्यायन

हमारा नर्सिंग कॉलेज भारतीय नर्सिंग परिषद (INC) दिल्ली द्वारा मान्यता प्राप्त है।

INC मान्यता के फायदे:
• आपकी डिग्री को राष्ट्रीय स्तर पर मान्यता देता है
• सरकारी नौकरियों के लिए पात्रता
• भारत में कहीं भी प्रैक्टिस करने की क्षमता

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
✅ RECOGNITION & ACCREDITATION

Hamara Nursing College Indian Nursing Council (INC) Delhi se recognized hai.

INC Recognition ke fayde:
• Aapki degree ko nationally valid banata hai
• Government jobs ke liye eligibility
• India mein kahin bhi practice karne ki ability

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'clinical_training': {
                'en': """
🏥 CLINICAL TRAINING LOCATIONS

Our students receive clinical training at the following locations:
• District Hospital (Backundpur)
• Community Health Centers
• Regional Hospital (Chartha)
• Ranchi Neurosurgery and Allied Science Hospital (Ranchi, Jharkhand)

These locations provide diverse medical experiences and exposure to various specialties.

Press Enter to return to main menu...""",

                'hi': """
🏥 क्लिनिकल प्रशिक्षण स्थान

हमारे छात्र निम्नलिखित स्थानों पर क्लिनिकल प्रशिक्षण प्राप्त करते हैं:
• जिला अस्पताल (Backundpur)
• सामुदायिक स्वास्थ्य केंद्र
• क्षेत्रीय अस्पताल (Chartha)
• रांची न्यूरोसर्जरी और संबद्ध विज्ञान अस्पताल (रांची, झारखंड)

ये स्थान विभिन्न चिकित्सा अनुभव और विभिन्न विशेषताओं के प्रति एक्सपोजर प्रदान करते हैं।

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
🏥 CLINICAL TRAINING LOCATIONS

Hamare students ko clinical training in locations par milti hai:
• District Hospital (Backundpur)
• Community Health Centers
• Regional Hospital (Chartha)
• Ranchi Neurosurgery and Allied Science Hospital (Ranchi, Jharkhand)

Ye locations aapko diverse medical experiences aur various specialties ka exposure deti hain.

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'scholarship_info': {
                'en': """
🎓 SCHOLARSHIP OPTIONS

We offer the following scholarships:
• Government Post-Matric Scholarship: ₹18,000 - ₹23,000 annually
• Labour Ministry Scholarships: ₹40,000 - ₹48,000 annually (Labour Registration required)

These scholarships can significantly reduce your financial burden.

Press Enter to return to main menu...""",

                'hi': """
🎓 छात्रवृत्ति विकल्प

हम निम्नलिखित छात्रवृत्तियाँ प्रदान करते हैं:
• सरकारी पोस्ट-मैट्रिक छात्रवृत्ति: ₹18,000 - ₹23,000 वार्षिक
• श्रम मंत्रालय छात्रवृत्तियाँ: ₹40,000 - ₹48,000 वार्षिक (श्रम पंजीकरण आवश्यक)

ये छात्रवृत्तियाँ आपकी वित्तीय बोझ को काफी हद तक कम कर सकती हैं।

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

                'hinglish': """
🎓 SCHOLARSHIP OPTIONS

Hum ye scholarships offer karte hain:
• Government Post-Matric Scholarship: ₹18,000 - ₹23,000 annually
• Labour Ministry Scholarships: ₹40,000 - ₹48,000 annually (Labour Registration required)

Ye scholarships aapka financial burden kaafi kam kar sakti hain.

Main menu par wapas jaane ke liye Enter press kariye..."""
            },

            'seat_availability': {
                'en': """
🪑 SEAT AVAILABILITY

• Total Available Seats: 60 seats in B.Sc Nursing program
• Limited seats, so early application is recommended
• Merit-based selection process
• First come, first served basis (after meeting eligibility criteria)

""",

                'hi': """
🪑 सीट उपलब्धता

• कुल उपलब्ध सीटें: B.Sc Nursing प्रोग्राम में 60 सीटें
• सीमित सीटें हैं, इसलिए जल्दी आवेदन करने की सिफारिश की जाती है
• मेरिट आधारित चयन प्रक्रिया
• पहले आओ, पहले पाओ आधार पर (योग्यता मानदंडों को पूरा करने के बाद)

""",

                'hinglish': """
🪑 SEAT AVAILABILITY

• Total Available Seats: B.Sc Nursing program mein 60 seats
• Limited seats hain, isliye early application recommended hai
• Merit-based selection process
• First come, first served basis (eligibility criteria meet karne ke baad)

"""
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
            system_prompt = self.get_comprehensive_system_prompt()

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

    def get_fallback_response(self, user_query: str) -> str:
        query_lower = user_query.lower()

        # Specific general queries
        if any(phrase in query_lower for phrase in [
            'why should i choose', 'why choose this college', 'why this college', 'what makes this college',
            'benefits of this college', 'advantages of this college', 'why should i study here',
            'unique about this college', 'special about this college', 'best about this college',
            'why select this college', 'क्यों चुनें', 'क्यों अच्छा', 'फायदा', 'विशेषता', 'अलग', 'unique', 'best', 'advantage', 'benefit', 'special', 'why us', 'हमारा कॉलेज क्यों', 'हम क्यों', 'हमारे कॉलेज की खासियत'
        ]):
            responses = {
                'en': (
                    "Our college stands out for its experienced faculty, modern facilities, and strong clinical training partnerships. "
                    "We focus on holistic nursing education, hands-on hospital experience, and excellent student support. "
                    "Graduates from our college are highly sought after in both government and private healthcare sectors. "
                    "We also offer scholarships, career guidance, and a vibrant campus life. Choosing our college means investing in a bright future in nursing!"
                ),
                'hi': (
                    "हमारे कॉलेज की खासियत है अनुभवी फैकल्टी, आधुनिक सुविधाएं और मजबूत क्लिनिकल ट्रेनिंग। "
                    "हम समग्र नर्सिंग शिक्षा, अस्पताल में व्यावहारिक अनुभव और बेहतरीन छात्र सहायता पर ध्यान देते हैं। "
                    "हमारे कॉलेज के स्नातक सरकारी और निजी दोनों क्षेत्रों में बहुत मांग में रहते हैं। "
                    "हम छात्रवृत्ति, करियर मार्गदर्शन और जीवंत कैंपस जीवन भी प्रदान करते हैं। हमारे कॉलेज को चुनना आपके उज्ज्वल भविष्य में निवेश है!"
                ),
                'hinglish': (
                    "Hamare college ki khasiyat hai experienced faculty, modern facilities aur strong clinical training. "
                    "Yahan holistic nursing education, hospital mein hands-on experience aur student support milta hai. "
                    "Graduates yahan se government aur private dono sectors mein demand mein hain. "
                    "Scholarships, career guidance aur vibrant campus life bhi milta hai. Hamara college choose karna ek bright future ka investment hai!"
                )
            }
            return responses[self.selected_language]

        if any(word in query_lower for word in ['scholarship', 'छात्रवृत्ति', 'financial', 'help']):
            return self.responses['scholarship_info'][self.selected_language]
        elif any(word in query_lower for word in ['fee', 'cost', 'price', 'फीस', 'पैसा']):
            return self.responses['fee_structure'][self.selected_language]
        elif any(word in query_lower for word in ['eligibility', 'qualify', 'योग्यता', 'biology']):
            return self.responses['eligibility_criteria'][self.selected_language]
        elif any(word in query_lower for word in ['hostel', 'accommodation', 'facility']):
            return self.responses['hostel_training'][self.selected_language]
        elif any(word in query_lower for word in ['location', 'where', 'delhi', 'स्थान']):
            return self.responses['location_info'][self.selected_language]

        fallback_responses = {
            'en': "I can help you with information about our B.Sc Nursing program including eligibility, fees, scholarships, facilities, and more. Please ask a specific question about the nursing program.",
            'hi': "मैं आपको हमारे B.Sc नर्सिंग प्रोग्राम के बारे में जानकारी दे सकता हूं जिसमें योग्यता, फीस, छात्रवृत्ति, सुविधाएं और बहुत कुछ शामिल है। कृपया नर्सिंग प्रोग्राम के बारे में कोई विशिष्ट प्रश्न पूछें।",
            'hinglish': "Main aapko hamare B.Sc Nursing program ke baare mein information de sakta hun including eligibility, fees, scholarships, facilities aur bahut kuch. Please nursing program ke baare mein koi specific question puchiye."
        }
        return fallback_responses[self.selected_language]

    def get_comprehensive_system_prompt(self) -> str:
        language_map = {'hi': 'Hindi', 'en': 'English', 'hinglish': 'Hinglish (Hindi-English mix)'}

        return f"""You are an AI admission counselor for a Nursing College. Always respond in {language_map[self.selected_language]}.

COLLEGE INFORMATION - B.Sc NURSING PROGRAM:

1. ELIGIBILITY CRITERIA:
• Biology in 12th grade (MANDATORY - "B.Sc Nursing mein admission ke liye Biology avashyak hai")
• Age: 17 to 35 years
• Must pass PNT Exam
• Valid 12th grade marksheet
• Medical fitness certificate

2. PROGRAM DETAILS:
• 4-year full-time Bachelor of Science in Nursing
• Professional nursing training with theoretical and practical education
• Hospital training included with real patients
• Career opportunities in hospitals, government jobs, private healthcare

3. FEE STRUCTURE (Annual):
• Tuition Fee: ₹60,000 INR
• Bus Fee: ₹10,000 INR
• Total: ₹70,000 INR
• Payment in 3 installments: ₹30,000 (admission), ₹20,000 (after 1st sem), ₹20,000 (after 2nd sem)

4. HOSTEL & TRAINING:
• 24x7 water and electricity
• CCTV surveillance for security
• Warden available on-site
• Hospital training with real patients included

5. LOCATION:
• College located in Delhi
• Excellent for nursing education with many hospitals
• Metro connectivity for easy transportation
• Modern healthcare infrastructure

6. RECOGNITION:
• Recognized by Indian Nursing Council (INC) Delhi
• Nationally valid degree
• Employment opportunities across India
• Eligibility for nursing license

7. CLINICAL TRAINING LOCATIONS:
• District Hospital (Backundpur)
• Community Health Centers
• Regional Hospital (Chartha)
• Ranchi Neurosurgery and Allied Science Hospital (Ranchi, Jharkhand)

8. SCHOLARSHIPS:
• Government Post-Matric Scholarship: ₹18,000-₹23,000 annually
• Labour Ministry Scholarships: ₹40,000-₹48,000 annually (requires Labour Registration)

9. SEAT AVAILABILITY:
�� Total 60 seats available
• Merit-based selection
• First come, first served basis after meeting eligibility

GUIDELINES:
Answer the user's query based on the above information. If the user's question is irrelevant, tell them you can only answer questions related to the nursing program and admission process.
• Always maintain the specified language throughout the response
• Be professional, helpful, and concise
• Provide accurate information only"""

    def show_main_menu(self) -> str:
        return self.responses['main_menu'][self.selected_language]

    def show_summary(self) -> str:
        summaries = {
            'en': """
📊 COMPLETE INFORMATION SUMMARY - B.Sc NURSING

✅ Eligibility: Biology in 12th + Age 17-35 + PNT Exam
💰 Fees: ₹70,000/year (3 installments)
📍 Location: Delhi
🏠 Hostel: 24x7 facilities with warden
🏥 Training: Real patient experience included
✅ Recognition: INC Delhi approved
🎓 Scholarships: ₹18k-₹48k available
🪑 Seats: 60 total available
⏰ Duration: 4 years full-time

Press Enter to return to main menu...""",

            'hi': """
📊 पूर्ण जानकारी सारांश - B.Sc नर्सिंग

✅ योग्यता: 12वीं में बायोलॉजी + आयु 17-35 + PNT परीक्षा
💰 फीस: ₹70,000/वर्ष (3 किस्तें)
📍 स्थान: दिल्ली
🏠 हॉस्टल: वार्डन के साथ 24x7 सुविधाएं
🏥 प्रशिक्षण: वास्तविक रोगी अनुभव शामिल
✅ मान्यता: INC दिल्ली अनुमोदित
🎓 छात्रवृत्ति: ₹18k-₹48k उपलब्ध
🪑 सीटें: कुल 60 उपलब्ध
⏰ अवधि: 4 साल पूर्णकालिक

मुख्य मेनू पर वापस जाने के लिए Enter दबाएं...""",

            'hinglish': """
📊 COMPLETE INFORMATION SUMMARY - B.Sc NURSING

✅ Eligibility: 12th mein Biology + Age 17-35 + PNT Exam
💰 Fees: ₹70,000/year (3 installments)
📍 Location: Delhi
🏠 Hostel: Warden ke saath 24x7 facilities
🏥 Training: Real patient experience included
✅ Recognition: INC Delhi approved
🎓 Scholarships: ₹18k-₹48k available
🪑 Seats: Total 60 available
⏰ Duration: 4 saal full-time

Main menu par wapas jaane ke liye Enter press kariye..."""
        }

        return summaries[self.selected_language]

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

