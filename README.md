# 🎓 TN Engineering Scholarship Finder

<div align="center">

**AI-powered scholarship discovery for Tamil Nadu engineering students**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://tn-scholarship-finder.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🔥 The Problem

Over **1.2 million engineering students** study in Tamil Nadu — one of India's largest technical education hubs.

Most of them qualify for **multiple government scholarships** worth ₹50,000–₹2 lakh per year.

**Most never apply. Not because they're ineligible — because they don't know these scholarships exist.**

The information is buried across 6+ government portals in bureaucratic language. First-generation students from low-income families — the ones who need this money most — have no one to guide them.

> **This tool changes that.**

---

## ✨ What It Does

A student fills a simple form (2 minutes) — category, gender, income, marks — and instantly gets:

- ✅ Every scholarship they qualify for, ranked by urgency
- ⏰ Live deadline countdown for each scholarship
- 📋 Personalized document checklist (only what they actually need)
- 📝 AI-generated application letter, ready to submit
- 📥 PDF report they can take to their college counselor
- 💬 Chat in English, Tamil, or Hindi for follow-up questions

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| **Smart Eligibility Filter** | Python pre-filters 19 scholarships before AI — faster, more accurate |
| **Match Scoring** | Each scholarship scored 0–99% based on student's need profile |
| **Urgency Detection** | 🔴 Critical (< 60 days) · 🟡 Moderate · 🟢 Plenty of time |
| **Application Letter Generator** | Streaming AI generates personalized formal letter in seconds |
| **PDF Report Export** | Full scholarship report with profile + matches + documents |
| **3-Language Support** | English · தமிழ் · हिंदी — full UI and AI responses |
| **Verified Data** | 19 scholarships across Central Gov, TN State, and Private/CSR sources |
| **Conversational AI** | Chat with AI about any scholarship — streaming responses |

---

## 🏛️ Scholarships Covered

| Source | Examples | Count |
|---|---|---|
| Central Government | AICTE Pragati, Saksham, Swanath · NSP SC/ST/OBC/Minority | 7 |
| Tamil Nadu State | BC/MBC/DNC Free Education · SC/ST Post-Matric · First Generation | 9 |
| Private / CSR | IDFC FIRST Bank · NHFDC · NSP Top Class | 3 |

**Total potential value per student: ₹50,000 – ₹2,00,000/year**

---

## 🛠️ Tech Stack

```
Frontend      →  Streamlit
AI Engine     →  Groq API (LLaMA 3.3 70B) — streaming responses
PDF Export    →  ReportLab
Language      →  Python 3.10+
Deployment    →  Streamlit Community Cloud
```

---

## 🏗️ Architecture

```
Student fills profile form
        │
        ▼
Python eligibility pre-filter
(hard rules: income, marks, category, gender)
        │
        ▼
Match scoring algorithm (0–99%)
        │
        ▼
Ranked scholarship cards with urgency countdown
        │
        ├──► Application Letter Generator (Claude/Groq streaming)
        ├──► Personalized document checklist
        ├──► PDF report export
        └──► Multilingual chat interface
```

**Why pre-filter before AI?**
Sending all 19 scholarships to the LLM on every query is slow and error-prone. Python filters first — AI only explains and generates. This makes the system faster, cheaper, and more accurate.

---

## 🚀 Run Locally

```bash
# Clone
git clone https://github.com/princemittalr/tn-scholarship-finder.git
cd tn-scholarship-finder

# Install
pip install streamlit groq reportlab

# Set API key
export GROQ_API_KEY="your_groq_api_key"   # Get free at console.groq.com

# Run
streamlit run app.py
```

---

## 📁 Project Structure

```
tn-scholarship-finder/
├── app.py              # Main application
├── requirements.txt    # Dependencies
└── README.md
```

---

## 💡 Design Decisions

**Why Groq instead of OpenAI?**
100% free tier. This tool is built for students with zero financial access — the infrastructure should match that mission.

**Why Streamlit?**
Fastest path from idea to deployed web app. Students can access it on any device, no installation needed.

**Why hard-code scholarship data instead of a database?**
For a tool serving students in low-connectivity rural areas, reliability matters more than scalability. A structured Python dict is fast, transparent, and easily auditable by NGOs or government partners.

---

## 🗺️ Roadmap

- [ ] WhatsApp Bot integration (field workers can query via WhatsApp)
- [ ] College-specific filtering (AICTE-approved TN colleges)
- [ ] Application status tracker
- [ ] SMS deadline reminders
- [ ] Expansion to other Indian states

---

## 🌍 Impact

This tool directly serves students from:
- SC / ST / OBC / BC / MBC / DNC communities
- Family income below ₹2.5 lakh/year
- First-generation engineering students
- Students with disabilities
- COVID-bereaved families

These are students for whom ₹50,000 is the difference between continuing education and dropping out.

---

## 👨‍💻 Author

**Prince Mittal**
B.Tech CSE (AI/ML) · Dayananda Sagar University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/princemittalr)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/princemittalr)

---

## 📄 License

MIT License — free to use, modify, and deploy for educational and social impact purposes.

---

<div align="center">

**Data verified June 2026 · Always verify deadlines at official government websites**

*Built with the belief that access to education funding should not depend on who you know.*

</div>