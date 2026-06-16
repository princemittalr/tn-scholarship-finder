import streamlit as st
from groq import Groq
import os

api_key = os.environ.get("GROQ_API_KEY", "ENTER YOUR GROQ_API_KEY")
client = Groq(api_key=api_key)

SCHOLARSHIP_DATA = """
You are a scholarship assistant for Tamil Nadu engineering students.
Help students find scholarships they are eligible for.
Only answer based on this verified scholarship data (verified June 15, 2026).

SCHOLARSHIPS:

1. AICTE Pragati Scholarship (Girl Students)
   - Who: Female, AICTE-approved engineering, income < ₹8 lakh, min 50% marks, max 2 girls per family
   - Amount: ₹5,000–₹50,000/year
   - Deadline: October 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, Income Certificate, Bonafide Certificate, Marksheets, Bank Passbook

2. AICTE Saksham Scholarship (Specially Abled)
   - Who: 40%+ disability, AICTE engineering, income < ₹8 lakh, min 50% marks
   - Amount: ₹50,000/year
   - Deadline: October 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, Disability Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

3. AICTE Swanath Scholarship (Orphan/COVID-affected)
   - Who: Orphan OR COVID-bereaved OR ward of Shaheed, engineering, income < ₹8 lakh
   - Amount: ₹50,000/year
   - Deadline: October 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, Death Certificate, Orphan/Shaheed Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

4. NSP Post-Matric Scholarship - SC
   - Who: SC, engineering, income < ₹2.5 lakh, min 50% marks
   - Amount: ₹25,000–₹45,000/year
   - Deadline: November 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, SC Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

5. NSP Post-Matric Scholarship - ST
   - Who: ST, engineering, income < ₹2.5 lakh, min 50% marks
   - Amount: ₹25,000–₹45,000/year
   - Deadline: November 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, ST Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

6. NSP Post-Matric Scholarship - Minority
   - Who: Muslim/Christian/Sikh/Buddhist/Jain/Parsi, engineering, income < ₹2 lakh, min 50% marks
   - Amount: ₹25,000–₹45,000/year
   - Deadline: November 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, Minority Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

6. NSP Post-Matric Scholarship - OBC
   - Who: OBC, engineering, income < ₹2.5 lakh, min 50% marks
   - Amount: ₹25,000–₹45,000/year
   - Deadline: November 2026
   - Apply: scholarships.gov.in
   - Documents: Aadhaar, OBC Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

7. TN Free Education Scholarship (BC/MBC/DNC)
   - Who: BC/MBC/DNC, engineering, income < ₹2.5 lakh, TN domicile
   - Amount: Full tuition + fees up to ₹2 lakh/year
   - Deadline: January 2027
   - Apply: bcmbcmw.tn.gov.in
   - Documents: Aadhaar, Community Certificate, Income Certificate, Fee receipt, Marksheets, Bank Passbook

8. TN Post-Matric Scholarship BC/MBC/DNC
   - Who: BC/MBC/DNC, engineering, income < ₹2.5 lakh, TN native, min 50% marks
   - Amount: Tuition reimbursement + ₹1,500/month stipend
   - Deadline: January 2027
   - Apply: bcmbcmw.tn.gov.in
   - Documents: Aadhaar, Community Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook, Fee receipt

9. TN Post-Matric Scholarship SC
   - Who: SC, engineering, income < ₹2.5 lakh, TN native, min 50% marks
   - Amount: Tuition reimbursement + maintenance allowance
   - Deadline: January 2027
   - Apply: ssp24-25.tnega.org
   - Documents: Aadhaar, SC Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

10. TN Post-Matric Scholarship ST
    - Who: ST, engineering, income < ₹2.5 lakh, TN native, min 50% marks
    - Amount: Tuition reimbursement + maintenance allowance
    - Deadline: January 2027
    - Apply: ssp24-25.tnega.org
    - Documents: Aadhaar, ST Certificate, Income Certificate, Bonafide, Marksheets, Bank Passbook

11. TN HESS Scholarship - ST
    - Who: ST, engineering, hostel resident, parental income < ₹2 lakh
    - Amount: ₹8,000/year
    - Deadline: Rolling
    - Apply: tntribalwelfare.tn.gov.in
    - Documents: Aadhaar, ST Certificate, Income Certificate, Hostel Certificate, Bonafide, Marksheets, Bank Passbook

12. TN First Generation Graduate Scholarship
    - Who: First in family to do engineering, income < ₹2.5 lakh, TN domicile
    - Amount: Full tuition + book allowance
    - Deadline: Rolling
    - Apply: dte.tn.gov.in
    - Documents: Aadhaar, Income Certificate, 12th Marksheet, First-graduate declaration, Bonafide, Bank Passbook

13. TN Scholarship for Differently Abled
    - Who: 40%+ disability, engineering, min 40% marks, TN domicile
    - Amount: ₹7,000/year
    - Deadline: Offline via District Welfare Officer
    - Apply: scd.tn.gov.in
    - Documents: Aadhaar, National ID for Differently Abled, Disability Certificate, Institution Certificate, Marksheet, Bank Passbook

14. TN Adi Dravidar Welfare Scholarship
    - Who: SC/Adi Dravidar, engineering, income < ₹2.5 lakh, TN domicile
    - Amount: Fee reimbursement + maintenance allowance
    - Deadline: Rolling
    - Apply: tnadw.tn.gov.in
    - Documents: Aadhaar, SC Certificate, Income Certificate, Bonafide, Fee receipt, Marksheets, Bank Passbook

15. TN Tribal Welfare Scholarship
    - Who: ST/Tribal, engineering, income < ₹2 lakh, TN domicile
    - Amount: ₹7,500–₹8,000/year
    - Deadline: Rolling
    - Apply: tntribalwelfare.tn.gov.in
    - Documents: Aadhaar, ST Certificate, Income Certificate, Bonafide, Fee receipt, Marksheets, Bank Passbook

16. IDFC FIRST Bank Scholarship (Disabilities)
    - Who: 40%+ disability, 4-year engineering, any institution
    - Amount: Up to ₹1 lakh/year for 4 years
    - Deadline: Check website
    - Apply: idfcfirst.com
    - Documents: Aadhaar, Disability Certificate, Income Certificate, Bonafide, Admission letter, Marksheets, Bank Passbook

17. NHFDC Scholarship (Disabled Students)
    - Who: 40%+ disability, graduation/technical, income < ₹3 lakh
    - Amount: Fee assistance + maintenance
    - Deadline: Rolling
    - Apply: nhfdc.nic.in
    - Documents: Aadhaar, Disability Certificate, Income Certificate, Admission letter, Marksheets, Fee receipt, Bank Passbook

18. NSP Top Class Education - Students with Disabilities
    - Who: 40%+ disability, engineering at IIT/NIT/IIIT, income < ₹8 lakh
    - Amount: Full tuition + ₹3,000/month + ₹2,000 special allowance + ₹5,000 books + ₹30,000 computer
    - Deadline: Rolling
    - Apply: socialwelfare.gov.in
    - Documents: Aadhaar, Disability Certificate, Income Certificate, Admission letter, Marksheets, Bank Passbook

LANGUAGE RULE:
- If user writes in Tamil → respond fully in Tamil
- If user writes in Hindi → respond fully in Hindi
- Default: English

RULES:
- Always ask: category, gender, family income, marks — if not provided
- List ALL scholarships student qualifies for
- Always show deadline + application website
- Always show combined document checklist at end
- Highlight scholarships closing within 3 months as URGENT
- Never guess. If unsure, say so.
- End every response with: "Verify deadlines at official websites before applying."
"""

st.set_page_config(page_title="TN Scholarship Finder", page_icon="🎓")
st.title("🎓 TN Engineering Scholarship Finder")
st.write("Find all scholarships you qualify for — free, verified June 2026.")

# Language selector
language = st.selectbox(
    "Choose language / மொழி தேர்வு / भाषा चुनें:",
    ["English", "தமிழ் (Tamil)", "हिंदी (Hindi)"]
)

lang_instruction = {
    "English": "Please respond in English.",
    "தமிழ் (Tamil)": "Please respond in Tamil language only.",
    "हिंदी (Hindi)": "Please respond in Hindi language only."
}

# UI labels per language
ui_labels = {
    "English": {
        "category": "Your Category",
        "gender": "Gender",
        "income": "Family Annual Income (₹ in lakhs, e.g. 1.5)",
        "marks": "Marks in Last Exam (%)",
        "firstgen": "Are you first in family to study engineering?",
        "disability": "Do you have a disability (40%+)?",
        "hostel": "Do you stay in hostel?",
        "btn": "🔍 Find My Scholarships",
        "yes": "Yes", "no": "No",
        "male": "Male", "female": "Female",
        "categories": ["SC", "ST", "OBC", "BC", "MBC", "DNC", "General", "Minority"],
    },
    "தமிழ் (Tamil)": {
        "category": "உங்கள் சாதி வகை",
        "gender": "பாலினம்",
        "income": "குடும்ப ஆண்டு வருமானம் (₹ லட்சத்தில், எ.கா. 1.5)",
        "marks": "கடைசி தேர்வு மதிப்பெண் (%)",
        "firstgen": "குடும்பத்தில் முதல் பொறியியல் மாணவரா?",
        "disability": "உங்களுக்கு மாற்றுத்திறன் உள்ளதா (40%+)?",
        "hostel": "நீங்கள் விடுதியில் தங்குகிறீர்களா?",
        "btn": "🔍 என் உதவித்தொகைகளை கண்டுபிடி",
        "yes": "ஆம்", "no": "இல்லை",
        "male": "ஆண்", "female": "பெண்",
        "categories": ["SC", "ST", "OBC", "BC", "MBC", "DNC", "General", "Minority"],
    },
    "हिंदी (Hindi)": {
        "category": "आपकी जाति श्रेणी",
        "gender": "लिंग",
        "income": "परिवार की वार्षिक आय (₹ लाख में, जैसे 1.5)",
        "marks": "पिछली परीक्षा में अंक (%)",
        "firstgen": "क्या आप परिवार में इंजीनियरिंग पढ़ने वाले पहले हैं?",
        "disability": "क्या आपको विकलांगता है (40%+)?",
        "hostel": "क्या आप हॉस्टल में रहते हैं?",
        "btn": "🔍 मेरी छात्रवृत्ति खोजें",
        "yes": "हाँ", "no": "नहीं",
        "male": "पुरुष", "female": "महिला",
        "categories": ["SC", "ST", "OBC", "BC", "MBC", "DNC", "General", "Minority"],
    }
}

lb = ui_labels[language]

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox(lb["category"], lb["categories"])
    gender = st.radio(lb["gender"], [lb["male"], lb["female"]], horizontal=True)
    firstgen = st.radio(lb["firstgen"], [lb["yes"], lb["no"]], horizontal=True)
with col2:
    income = st.number_input(lb["income"], min_value=0.0, max_value=50.0, value=1.5, step=0.1)
    marks = st.number_input(lb["marks"], min_value=0, max_value=100, value=60)
    disability = st.radio(lb["disability"], [lb["yes"], lb["no"]], horizontal=True)
    hostel = st.radio(lb["hostel"], [lb["yes"], lb["no"]], horizontal=True)

find_clicked = st.button(lb["btn"], type="primary")

if find_clicked:
    # Build English query from dropdowns
    gender_en = "female" if gender == lb["female"] else "male"
    firstgen_en = "yes, first in family to study engineering" if firstgen == lb["yes"] else "no"
    disability_en = "yes, 40%+ disability" if disability == lb["yes"] else "no"
    hostel_en = "yes" if hostel == lb["yes"] else "no"
    
    auto_query = (
        f"I am {category} {gender_en}, family income ₹{income} lakh per year, "
        f"scored {marks}% in last exam, first generation: {firstgen_en}, "
        f"disability: {disability_en}, hostel: {hostel_en}. "
        f"Find all scholarships I qualify for."
    )
    st.session_state["prefill"] = auto_query
    st.rerun()

# Deadline alert
st.warning("⏰ **Upcoming:** AICTE & NSP scholarships open around October–November 2026. Prepare documents now!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prefill_value = st.session_state.pop("prefill", "")
user_input = prefill_value if prefill_value else st.chat_input("Example: I am BC male, income ₹1.5 lakh, scored 72%...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    system_prompt = SCHOLARSHIP_DATA + "\n\n" + lang_instruction[language]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    ai_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    with st.chat_message("assistant"):
        st.write(ai_reply)

    # Document checklist expander
    with st.expander("📋 Common documents you'll likely need"):
        st.markdown("""
        **Prepare these in advance for most scholarships:**
        - ✅ Aadhaar Card
        - ✅ Community / Caste Certificate
        - ✅ Family Income Certificate
        - ✅ Bonafide Certificate (from your college)
        - ✅ Previous year Marksheets
        - ✅ Bank Passbook (your own account)
        - ✅ Fee Receipt (from college)
        - ✅ Passport size photos
        
        *Get all originals + 2 xerox copies of each.*
        """)

st.markdown("---")
st.caption("Data verified June 15, 2026 | Always verify deadlines at official websites before applying.")