import streamlit as st
from groq import Groq
import os
from datetime import datetime
import io

# ── PDF support (optional) ────────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TN Scholarship Finder",
    page_icon="🎓",
    layout="wide"
)

# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not set. Add it to your environment variables or Streamlit secrets.")
        st.stop()
    return Groq(api_key=api_key)

client = get_client()
MODEL = "llama-3.3-70b-versatile"

# ── SCHOLARSHIP DATABASE ──────────────────────────────────────────────────────
SCHOLARSHIPS = [
    {
        "id": 1,
        "name": "AICTE Pragati Scholarship (Girl Students)",
        "category": "central",
        "gender": ["female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 8.0,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹5,000–₹50,000/year",
        "deadline": "2026-10-31",
        "portal": "scholarships.gov.in",
        "notes": "Max 2 girls per family. AICTE-approved college required.",
        "documents": ["Aadhaar Card","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 2,
        "name": "AICTE Saksham Scholarship (Specially Abled)",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 8.0,
        "min_marks": 50,
        "disability_required": True,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹50,000/year",
        "deadline": "2026-10-31",
        "portal": "scholarships.gov.in",
        "notes": "Requires 40%+ disability certificate.",
        "documents": ["Aadhaar Card","Disability Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 3,
        "name": "AICTE Swanath Scholarship (Orphan/COVID-affected)",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 8.0,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": True,
        "amount": "₹50,000/year",
        "deadline": "2026-10-31",
        "portal": "scholarships.gov.in",
        "notes": "For orphans, COVID-bereaved students, or wards of Shaheed.",
        "documents": ["Aadhaar Card","Death Certificate","Orphan/Shaheed Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 4,
        "name": "NSP Post-Matric Scholarship — SC",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["SC"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹25,000–₹45,000/year",
        "deadline": "2026-11-30",
        "portal": "scholarships.gov.in",
        "notes": "National Scholarship Portal — SC category.",
        "documents": ["Aadhaar Card","SC Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 5,
        "name": "NSP Post-Matric Scholarship — ST",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["ST"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹25,000–₹45,000/year",
        "deadline": "2026-11-30",
        "portal": "scholarships.gov.in",
        "notes": "National Scholarship Portal — ST category.",
        "documents": ["Aadhaar Card","ST Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 6,
        "name": "NSP Post-Matric Scholarship — Minority",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["Minority"],
        "max_income": 2.0,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹25,000–₹45,000/year",
        "deadline": "2026-11-30",
        "portal": "scholarships.gov.in",
        "notes": "Muslim, Christian, Sikh, Buddhist, Jain, Parsi students.",
        "documents": ["Aadhaar Card","Minority Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 7,
        "name": "NSP Post-Matric Scholarship — OBC",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["OBC"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹25,000–₹45,000/year",
        "deadline": "2026-11-30",
        "portal": "scholarships.gov.in",
        "notes": "National Scholarship Portal — OBC category.",
        "documents": ["Aadhaar Card","OBC Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 8,
        "name": "TN Free Education Scheme (BC/MBC/DNC)",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["BC","MBC","DNC"],
        "max_income": 2.5,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Full tuition + fees up to ₹2 lakh/year",
        "deadline": "2027-01-31",
        "portal": "bcmbcmw.tn.gov.in",
        "notes": "Tamil Nadu domicile required.",
        "documents": ["Aadhaar Card","Community Certificate","Income Certificate","Fee Receipt","Marksheets","Bank Passbook"]
    },
    {
        "id": 9,
        "name": "TN Post-Matric Scholarship — BC/MBC/DNC",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["BC","MBC","DNC"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Tuition reimbursement + ₹1,500/month stipend",
        "deadline": "2027-01-31",
        "portal": "bcmbcmw.tn.gov.in",
        "notes": "TN native required.",
        "documents": ["Aadhaar Card","Community Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook","Fee Receipt"]
    },
    {
        "id": 10,
        "name": "TN Post-Matric Scholarship — SC",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["SC"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Tuition reimbursement + maintenance allowance",
        "deadline": "2027-01-31",
        "portal": "ssp24-25.tnega.org",
        "notes": "TN native required.",
        "documents": ["Aadhaar Card","SC Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 11,
        "name": "TN Post-Matric Scholarship — ST",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["ST"],
        "max_income": 2.5,
        "min_marks": 50,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Tuition reimbursement + maintenance allowance",
        "deadline": "2027-01-31",
        "portal": "ssp24-25.tnega.org",
        "notes": "TN native required.",
        "documents": ["Aadhaar Card","ST Certificate","Income Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 12,
        "name": "TN HESS Scholarship — ST (Hostel)",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["ST"],
        "max_income": 2.0,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": True,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹8,000/year",
        "deadline": "2027-03-31",
        "portal": "tntribalwelfare.tn.gov.in",
        "notes": "Must be staying in hostel.",
        "documents": ["Aadhaar Card","ST Certificate","Income Certificate","Hostel Certificate","Bonafide Certificate","Marksheets","Bank Passbook"]
    },
    {
        "id": 13,
        "name": "TN First Generation Graduate Scholarship",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 2.5,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": True,
        "orphan_required": False,
        "amount": "Full tuition + book allowance",
        "deadline": "2027-03-31",
        "portal": "dte.tn.gov.in",
        "notes": "First in family to pursue engineering degree.",
        "documents": ["Aadhaar Card","Income Certificate","Class 12 Marksheet","First-Graduate Declaration","Bonafide Certificate","Bank Passbook"]
    },
    {
        "id": 14,
        "name": "TN Scholarship for Differently Abled",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 50.0,
        "min_marks": 40,
        "disability_required": True,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹7,000/year",
        "deadline": "2027-03-31",
        "portal": "scd.tn.gov.in",
        "notes": "Apply offline via District Welfare Officer.",
        "documents": ["Aadhaar Card","National ID for Differently Abled","Disability Certificate","Institution Certificate","Marksheet","Bank Passbook"]
    },
    {
        "id": 15,
        "name": "TN Adi Dravidar Welfare Scholarship",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["SC"],
        "max_income": 2.5,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Fee reimbursement + maintenance allowance",
        "deadline": "2027-03-31",
        "portal": "tnadw.tn.gov.in",
        "notes": "TN domicile required.",
        "documents": ["Aadhaar Card","SC Certificate","Income Certificate","Bonafide Certificate","Fee Receipt","Marksheets","Bank Passbook"]
    },
    {
        "id": 16,
        "name": "TN Tribal Welfare Scholarship",
        "category": "state",
        "gender": ["male","female"],
        "categories": ["ST"],
        "max_income": 2.0,
        "min_marks": 0,
        "disability_required": False,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "₹7,500–₹8,000/year",
        "deadline": "2027-03-31",
        "portal": "tntribalwelfare.tn.gov.in",
        "notes": "TN domicile required.",
        "documents": ["Aadhaar Card","ST Certificate","Income Certificate","Bonafide Certificate","Fee Receipt","Marksheets","Bank Passbook"]
    },
    {
        "id": 17,
        "name": "IDFC FIRST Bank Scholarship (Disabilities)",
        "category": "private",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 50.0,
        "min_marks": 0,
        "disability_required": True,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Up to ₹1 lakh/year for 4 years",
        "deadline": "2027-03-31",
        "portal": "idfcfirst.com",
        "notes": "40%+ disability required. Check website for exact deadline.",
        "documents": ["Aadhaar Card","Disability Certificate","Income Certificate","Bonafide Certificate","Admission Letter","Marksheets","Bank Passbook"]
    },
    {
        "id": 18,
        "name": "NHFDC Scholarship (Disabled Students)",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 3.0,
        "min_marks": 0,
        "disability_required": True,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Fee assistance + maintenance allowance",
        "deadline": "2027-03-31",
        "portal": "nhfdc.nic.in",
        "notes": "40%+ disability required.",
        "documents": ["Aadhaar Card","Disability Certificate","Income Certificate","Admission Letter","Marksheets","Fee Receipt","Bank Passbook"]
    },
    {
        "id": 19,
        "name": "NSP Top Class Education — Students with Disabilities",
        "category": "central",
        "gender": ["male","female"],
        "categories": ["SC","ST","OBC","BC","MBC","DNC","General","Minority"],
        "max_income": 8.0,
        "min_marks": 0,
        "disability_required": True,
        "hostel_required": False,
        "first_gen_required": False,
        "orphan_required": False,
        "amount": "Full tuition + ₹3,000/month + ₹2,000 special + ₹5,000 books + ₹30,000 computer",
        "deadline": "2027-03-31",
        "portal": "socialwelfare.gov.in",
        "notes": "Only for IIT/NIT/IIIT students. 40%+ disability required.",
        "documents": ["Aadhaar Card","Disability Certificate","Income Certificate","Admission Letter","Marksheets","Bank Passbook"]
    },
]

ALL_CATEGORIES = ["SC","ST","OBC","BC","MBC","DNC","General","Minority"]

# ── HELPERS ───────────────────────────────────────────────────────────────────

def days_until(deadline_str):
    try:
        return (datetime.strptime(deadline_str, "%Y-%m-%d") - datetime.now()).days
    except Exception:
        return 999

def urgency_info(days):
    if days < 0:
        return "❌ CLOSED", "error"
    elif days < 60:
        return f"🔴 URGENT — {days} days left", "error"
    elif days < 120:
        return f"🟡 {days} days left", "warning"
    else:
        return f"🟢 {days} days left", "success"

def match_score(s, profile):
    score = 70
    if profile["income"] < 1.0:
        score += 15
    elif profile["income"] < 1.5:
        score += 10
    if profile["marks"] >= 80:
        score += 10
    elif profile["marks"] >= 65:
        score += 5
    if s["category"] == "state":
        score += 5
    d = days_until(s["deadline"])
    if 30 < d < 90:
        score += 5
    return min(score, 99)

def filter_scholarships(profile):
    matches = []
    for s in SCHOLARSHIPS:
        # gender
        if profile["gender"] not in s["gender"]:
            continue
        # category
        if s["categories"] != ALL_CATEGORIES and profile["category"] not in s["categories"]:
            continue
        # income
        if profile["income"] > s["max_income"]:
            continue
        # marks
        if s["min_marks"] > 0 and profile["marks"] < s["min_marks"]:
            continue
        # special flags
        if s["disability_required"] and not profile["disability"]:
            continue
        if s["hostel_required"] and not profile["hostel"]:
            continue
        if s["first_gen_required"] and not profile["first_gen"]:
            continue
        if s["orphan_required"] and not profile["orphan"]:
            continue
        # skip closed
        if days_until(s["deadline"]) < 0:
            continue
        matches.append(s)
    matches.sort(key=lambda x: match_score(x, profile), reverse=True)
    return matches

def unique_documents(matches):
    docs = set()
    for s in matches:
        docs.update(s["documents"])
    return sorted(docs)

def build_system_prompt(matches, profile, language):
    lang_map = {
        "English": "Respond in English only.",
        "தமிழ் (Tamil)": "Respond entirely in Tamil language only.",
        "हिंदी (Hindi)": "Respond entirely in Hindi language only.",
    }
    scholarship_text = ""
    for i, s in enumerate(matches, 1):
        d = days_until(s["deadline"])
        tag = "⚠️ URGENT" if d < 60 else "Normal"
        scholarship_text += (
            f"\n{i}. {s['name']} [{tag}] [Match: {match_score(s,profile)}%]"
            f"\n   Amount: {s['amount']}"
            f"\n   Deadline: {s['deadline']} ({d} days remaining)"
            f"\n   Apply at: {s['portal']}"
            f"\n   Notes: {s['notes']}"
            f"\n   Documents: {', '.join(s['documents'])}\n"
        )
    return f"""You are an expert scholarship advisor for Tamil Nadu engineering students.

STUDENT PROFILE:
- Category: {profile['category']}
- Gender: {profile['gender'].title()}
- Family Income: ₹{profile['income']} lakh/year
- Last Exam Marks: {profile['marks']}%
- First Generation Engineer: {'Yes' if profile['first_gen'] else 'No'}
- Disability (40%+): {'Yes' if profile['disability'] else 'No'}
- Hostel Resident: {'Yes' if profile['hostel'] else 'No'}
- Orphan/COVID-affected: {'Yes' if profile['orphan'] else 'No'}

MATCHED SCHOLARSHIPS ({len(matches)} found — already pre-filtered for eligibility):
{scholarship_text}

RULES:
1. Present scholarships sorted by urgency first (URGENT ones first)
2. Explain why each scholarship matches this specific student
3. Give clear next steps for each scholarship
4. Never invent scholarships not listed above
5. Always end with: "Verify deadlines at official websites before applying."

{lang_map.get(language, 'Respond in English only.')}"""

# ── PDF GENERATOR ─────────────────────────────────────────────────────────────

def generate_pdf(matches, profile, student_name=""):
    if not PDF_AVAILABLE:
        return None
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("T", parent=styles["Title"], fontSize=18,
                                  spaceAfter=4, textColor=colors.HexColor("#1a1a2e"))
    story.append(Paragraph("🎓 TN Engineering Scholarship Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]))
    if student_name:
        story.append(Paragraph(f"Student: {student_name}", styles["Normal"]))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Student Profile", styles["Heading2"]))
    pdata = [
        ["Category", profile["category"]],
        ["Gender", profile["gender"].title()],
        ["Family Income", f"₹{profile['income']} lakh/year"],
        ["Marks", f"{profile['marks']}%"],
        ["First Generation", "Yes" if profile["first_gen"] else "No"],
        ["Disability (40%+)", "Yes" if profile["disability"] else "No"],
        ["Hostel", "Yes" if profile["hostel"] else "No"],
    ]
    t = Table(pdata, colWidths=[2*inch, 3.5*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#e8f4fd")),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("FONTSIZE",(0,0),(-1,-1),10),
        ("PADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(f"✅ {len(matches)} Scholarships You Qualify For", styles["Heading2"]))
    for i, s in enumerate(matches, 1):
        d = days_until(s["deadline"])
        urgent = " ⚠️ URGENT" if d < 60 else ""
        story.append(Paragraph(f"{i}. {s['name']}{urgent}", styles["Heading3"]))
        rows = [
            ["Amount", s["amount"]],
            ["Deadline", f"{s['deadline']} ({d} days remaining)"],
            ["Apply at", s["portal"]],
            ["Notes", s["notes"]],
        ]
        t2 = Table(rows, colWidths=[1.5*inch, 4*inch])
        bg = colors.HexColor("#fff3cd") if d < 60 else colors.HexColor("#f8f9fa")
        t2.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),bg),
            ("GRID",(0,0),(-1,-1),0.3,colors.grey),
            ("FONTSIZE",(0,0),(-1,-1),9),
            ("PADDING",(0,0),(-1,-1),4),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("📋 Master Document Checklist", styles["Heading2"]))
    story.append(Paragraph("Prepare these for all your scholarship applications:", styles["Normal"]))
    for doc in unique_documents(matches):
        story.append(Paragraph(f"☐  {doc}", styles["Normal"]))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "⚠️ Always verify deadlines at official websites before applying.",
        ParagraphStyle("W", parent=styles["Normal"], textColor=colors.red, fontSize=9)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── UI LABELS (3 languages) ───────────────────────────────────────────────────
UI = {
    "English": {
        "title": "🎓 TN Engineering Scholarship Finder",
        "subtitle": "Find every scholarship you qualify for — verified June 2026",
        "name_label": "Your Name (optional — used in PDF report)",
        "cat_label": "Caste Category",
        "gender_label": "Gender",
        "income_label": "Family Annual Income (₹ lakhs, e.g. 1.5)",
        "marks_label": "Last Exam Marks (%)",
        "firstgen_label": "First in family to study engineering?",
        "disability_label": "Do you have a disability (40%+)?",
        "hostel_label": "Do you stay in hostel?",
        "orphan_label": "Are you an orphan or COVID-bereaved?",
        "btn": "🔍 Find My Scholarships",
        "letter_btn": "📝 Generate Application Letter",
        "pdf_btn": "📥 Download PDF Report",
        "yes": "Yes", "no": "No",
        "male": "Male", "female": "Female",
        "no_match": "No scholarships matched your profile. Double-check your inputs.",
        "found": "scholarships found",
        "urgent_note": "⚠️ Scholarships marked URGENT close within 60 days — apply first!",
        "chat_placeholder": "Ask anything about your scholarships...",
        "select_label": "Select scholarship to generate letter for:",
        "doc_title": "📋 Master Document Checklist",
        "chat_title": "💬 Ask About Your Scholarships",
        "letter_title": "📝 Application Letter Generator",
    },
    "தமிழ் (Tamil)": {
        "title": "🎓 TN பொறியியல் உதவித்தொகை கண்டுபிடிப்பான்",
        "subtitle": "உங்களுக்கு தகுதியான அனைத்து உதவித்தொகைகளையும் கண்டுபிடியுங்கள் — ஜூன் 2026 சரிபார்க்கப்பட்டது",
        "name_label": "உங்கள் பெயர் (விரும்பினால் — PDF அறிக்கைக்கு)",
        "cat_label": "சாதி வகை",
        "gender_label": "பாலினம்",
        "income_label": "குடும்ப ஆண்டு வருமானம் (₹ லட்சத்தில், எ.கா. 1.5)",
        "marks_label": "கடைசி தேர்வு மதிப்பெண் (%)",
        "firstgen_label": "குடும்பத்தில் முதல் பொறியியல் மாணவரா?",
        "disability_label": "மாற்றுத்திறன் உள்ளதா (40%+)?",
        "hostel_label": "விடுதியில் தங்குகிறீர்களா?",
        "orphan_label": "அனாதையா அல்லது COVID பாதித்தவரா?",
        "btn": "🔍 என் உதவித்தொகை கண்டுபிடி",
        "letter_btn": "📝 விண்ணப்பக் கடிதம் உருவாக்கு",
        "pdf_btn": "📥 PDF அறிக்கை பதிவிறக்கு",
        "yes": "ஆம்", "no": "இல்லை",
        "male": "ஆண்", "female": "பெண்",
        "no_match": "உங்கள் சுயவிவரத்திற்கு பொருந்தும் உதவித்தொகை இல்லை. உள்ளீடுகளை சரிபார்க்கவும்.",
        "found": "உதவித்தொகைகள் கண்டுபிடிக்கப்பட்டன",
        "urgent_note": "⚠️ சிவப்பு நிறத்தில் உள்ளவை 60 நாட்களில் முடிவடையும் — முதலில் விண்ணப்பியுங்கள்!",
        "chat_placeholder": "உதவித்தொகை பற்றி கேளுங்கள்...",
        "select_label": "கடிதத்திற்கு உதவித்தொகை தேர்வு செய்யுங்கள்:",
        "doc_title": "📋 ஆவண பட்டியல்",
        "chat_title": "💬 உதவித்தொகை பற்றி கேளுங்கள்",
        "letter_title": "📝 விண்ணப்பக் கடிதம் உருவாக்கி",
    },
    "हिंदी (Hindi)": {
        "title": "🎓 TN इंजीनियरिंग छात्रवृत्ति खोजक",
        "subtitle": "अपनी पात्र सभी छात्रवृत्तियां खोजें — जून 2026 सत्यापित",
        "name_label": "आपका नाम (वैकल्पिक — PDF रिपोर्ट के लिए)",
        "cat_label": "जाति श्रेणी",
        "gender_label": "लिंग",
        "income_label": "पारिवारिक वार्षिक आय (₹ लाख में, जैसे 1.5)",
        "marks_label": "पिछली परीक्षा में अंक (%)",
        "firstgen_label": "क्या परिवार में इंजीनियरिंग पढ़ने वाले पहले हैं?",
        "disability_label": "क्या विकलांगता है (40%+)?",
        "hostel_label": "क्या हॉस्टल में रहते हैं?",
        "orphan_label": "क्या अनाथ या COVID प्रभावित हैं?",
        "btn": "🔍 मेरी छात्रवृत्ति खोजें",
        "letter_btn": "📝 आवेदन पत्र बनाएं",
        "pdf_btn": "📥 PDF रिपोर्ट डाउनलोड करें",
        "yes": "हाँ", "no": "नहीं",
        "male": "पुरुष", "female": "महिला",
        "no_match": "आपकी प्रोफाइल से कोई छात्रवृत्ति मेल नहीं खाई। इनपुट जांचें।",
        "found": "छात्रवृत्तियां मिलीं",
        "urgent_note": "⚠️ लाल चिह्नित छात्रवृत्तियां 60 दिनों में बंद होंगी — पहले आवेदन करें!",
        "chat_placeholder": "छात्रवृत्ति के बारे में पूछें...",
        "select_label": "आवेदन पत्र के लिए छात्रवृत्ति चुनें:",
        "doc_title": "📋 दस्तावेज़ चेकलिस्ट",
        "chat_title": "💬 छात्रवृत्ति के बारे में पूछें",
        "letter_title": "📝 आवेदन पत्र जनरेटर",
    },
}

# ── APP LAYOUT ────────────────────────────────────────────────────────────────
language = st.sidebar.selectbox(
    "🌐 Language / மொழி / भाषा",
    ["English", "தமிழ் (Tamil)", "हिंदी (Hindi)"]
)
lb = UI[language]

st.title(lb["title"])
st.caption(lb["subtitle"])
st.caption("Data verified June 15, 2026 | Free AI powered by Groq (LLaMA 3.3 70B)")

# ── PROFILE FORM ──────────────────────────────────────────────────────────────
with st.form("profile_form"):
    student_name = st.text_input(lb["name_label"], placeholder="e.g. Priya Murugan")
    col1, col2 = st.columns(2)
    with col1:
        category    = st.selectbox(lb["cat_label"], ALL_CATEGORIES)
        gender_raw  = st.radio(lb["gender_label"], [lb["male"], lb["female"]], horizontal=True)
        income      = st.number_input(lb["income_label"], min_value=0.0, max_value=50.0, value=1.5, step=0.1)
        marks       = st.number_input(lb["marks_label"], min_value=0, max_value=100, value=60)
    with col2:
        firstgen    = st.radio(lb["firstgen_label"],   [lb["yes"], lb["no"]], horizontal=True)
        disability  = st.radio(lb["disability_label"], [lb["yes"], lb["no"]], horizontal=True)
        hostel      = st.radio(lb["hostel_label"],     [lb["yes"], lb["no"]], horizontal=True)
        orphan      = st.radio(lb["orphan_label"],     [lb["yes"], lb["no"]], horizontal=True)

    submitted = st.form_submit_button(lb["btn"], type="primary", use_container_width=True)

if submitted:
    gender_en = "female" if gender_raw == lb["female"] else "male"
    profile = {
        "name":       student_name,
        "category":   category,
        "gender":     gender_en,
        "income":     income,
        "marks":      marks,
        "first_gen":  firstgen   == lb["yes"],
        "disability": disability == lb["yes"],
        "hostel":     hostel     == lb["yes"],
        "orphan":     orphan     == lb["yes"],
    }
    st.session_state["profile"]  = profile
    st.session_state["matches"]  = filter_scholarships(profile)
    st.session_state["messages"] = []
    st.session_state["language"] = language
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────────────────────
if "matches" in st.session_state and "profile" in st.session_state:
    matches  = st.session_state["matches"]
    profile  = st.session_state["profile"]
    lang     = st.session_state.get("language", "English")
    lb       = UI[lang]

    if not matches:
        st.warning(lb["no_match"])
    else:
        # ── Summary bar ──
        st.success(f"✅ **{len(matches)} {lb['found']}** for your profile")
        st.info(lb["urgent_note"])

        # ── Scholarship cards ──
        for s in matches:
            d = days_until(s["deadline"])
            u_label, u_type = urgency_info(d)
            score = match_score(s, profile)
            cat_badge = {"central":"🏛️ Central Gov","state":"🏠 Tamil Nadu State","private":"🏢 Private/CSR"}.get(s["category"],"")

            with st.expander(f"**{s['name']}** · {s['amount']} · {u_label} · Match {score}%"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**Amount:** {s['amount']}")
                    st.markdown(f"**Apply at:** [{s['portal']}](https://{s['portal']})")
                    st.markdown(f"**Notes:** {s['notes']}")
                    st.markdown("**Documents needed:**")
                    dc1, dc2 = st.columns(2)
                    for i, doc in enumerate(s["documents"]):
                        (dc1 if i % 2 == 0 else dc2).markdown(f"☐ {doc}")
                with c2:
                    st.markdown(f"**Type:** {cat_badge}")
                    if u_type == "error":
                        st.error(u_label)
                    elif u_type == "warning":
                        st.warning(u_label)
                    else:
                        st.success(u_label)

        st.divider()

        # ── PDF + Document checklist row ──
        col_pdf, col_docs = st.columns(2)

        with col_pdf:
            if PDF_AVAILABLE:
                pdf_buf = generate_pdf(matches, profile, profile.get("name",""))
                if pdf_buf:
                    st.download_button(
                        lb["pdf_btn"],
                        data=pdf_buf,
                        file_name=f"TN_Scholarships_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("For PDF export run: `pip install reportlab`")

        with col_docs:
            with st.expander(lb["doc_title"]):
                udocs = unique_documents(matches)
                st.markdown(f"**Prepare these {len(udocs)} documents:**")
                for doc in udocs:
                    st.markdown(f"☐ {doc}")
                st.caption("Get originals + 2 photocopies of each.")

        st.divider()

        # ── Application Letter Generator ──
        st.subheader(lb["letter_title"])
        sch_names     = [s["name"] for s in matches]
        selected_name = st.selectbox(lb["select_label"], sch_names)
        selected_sch  = next((s for s in matches if s["name"] == selected_name), None)

        if st.button(lb["letter_btn"], type="secondary"):
            if selected_sch:
                letter_prompt = f"""Write a formal scholarship application letter.

Student Details:
- Name: {profile.get('name') or 'the student'}
- Category: {profile['category']}
- Gender: {profile['gender'].title()}
- Family Income: ₹{profile['income']} lakh/year
- Last Exam Marks: {profile['marks']}%
- First Generation Engineer: {'Yes' if profile['first_gen'] else 'No'}
- Disability: {'Yes (40%+)' if profile['disability'] else 'No'}

Scholarship Details:
- Name: {selected_sch['name']}
- Amount: {selected_sch['amount']}
- Portal: {selected_sch['portal']}
- Notes: {selected_sch['notes']}

Write a 300-350 word formal application letter including:
1. To: The Scholarship Committee, [Scholarship Name]
2. Subject line
3. Introduction with student details and course
4. Eligibility points clearly tied to criteria
5. Financial need with specifics
6. Academic achievements
7. How this scholarship helps future plans
8. Formal closing with date placeholder

Keep it professional, genuine, and specific to this student's profile."""

                with st.spinner("Generating letter..."):
                    try:
                        response = client.chat.completions.create(
                            model=MODEL,
                            messages=[{"role":"user","content":letter_prompt}],
                            max_tokens=1000,
                            stream=True
                        )
                        letter_box = st.empty()
                        full_letter = ""
                        for chunk in response:
                            delta = chunk.choices[0].delta.content or ""
                            full_letter += delta
                            letter_box.markdown(full_letter + "▌")
                        letter_box.markdown(full_letter)

                        st.download_button(
                            "📥 Download Letter (.txt)",
                            data=full_letter,
                            file_name=f"Application_Letter_{selected_name[:25].replace(' ','_')}.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Letter generation failed: {e}")

        st.divider()

        # ── Chat Interface ──
        st.subheader(lb["chat_title"])

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Auto first message
        if not st.session_state.messages:
            auto_q = "Analyze my matched scholarships. Tell me which to apply for first based on urgency and my profile. Give clear next steps."
            st.session_state.messages.append({"role":"user","content":auto_q})
            system_prompt = build_system_prompt(matches, profile, lang)
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role":"system","content":system_prompt},
                        {"role":"user","content":auto_q}
                    ],
                    max_tokens=1500,
                    stream=True
                )
                with st.chat_message("assistant"):
                    box = st.empty()
                    full = ""
                    for chunk in response:
                        delta = chunk.choices[0].delta.content or ""
                        full += delta
                        box.markdown(full + "▌")
                    box.markdown(full)
                st.session_state.messages.append({"role":"assistant","content":full})
            except Exception as e:
                st.error(f"AI error: {e}")
        else:
            for msg in st.session_state.messages:
                # hide auto query from UI
                if msg["role"] == "user" and "Analyze my matched" in msg["content"]:
                    continue
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # User chat input
        user_input = st.chat_input(lb["chat_placeholder"])
        if user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            system_prompt = build_system_prompt(matches, profile, lang)
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role":"system","content":system_prompt},
                        *st.session_state.messages
                    ],
                    max_tokens=1500,
                    stream=True
                )
                with st.chat_message("assistant"):
                    box = st.empty()
                    full = ""
                    for chunk in response:
                        delta = chunk.choices[0].delta.content or ""
                        full += delta
                        box.markdown(full + "▌")
                    box.markdown(full)
                st.session_state.messages.append({"role":"assistant","content":full})
            except Exception as e:
                st.error(f"Error: {e}")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
c1, c2, c3 = st.columns(3)
c1.caption("📅 Data verified: June 15, 2026")
c2.caption("🤖 Powered by Groq (LLaMA 3.3 70B) — Free")
c3.caption("⚠️ Verify all deadlines at official websites")
