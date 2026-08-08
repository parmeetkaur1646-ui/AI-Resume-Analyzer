import re
from io import BytesIO

import pdfplumber
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# GEN-Z LIGHT UI
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(221,214,254,.55), transparent 28%),
        radial-gradient(circle at 100% 8%, rgba(191,219,254,.45), transparent 26%),
        radial-gradient(circle at 70% 100%, rgba(252,231,243,.55), transparent 30%),
        #fbfaff;
}
.block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#f5f3ff 0%,#eef2ff 52%,#fff1f7 100%);
    border-right: 1px solid #e8e4f5;
}
.hero {
    padding: 10px 0 22px 0;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(38px, 5vw, 58px);
    line-height: 1.02;
    margin: 0;
    letter-spacing: -2.5px;
    background: linear-gradient(90deg,#6d28d9,#ec4899 55%,#2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { color:#6b7280; font-size:18px; margin:12px 0 0; }
.pill {
    display:inline-block; padding:7px 12px; margin-top:15px; margin-right:6px;
    border-radius:999px; background:#fff; border:1px solid #e9e5ff;
    color:#6d28d9; font-size:13px; font-weight:700;
    box-shadow:0 6px 18px rgba(99,102,241,.08);
}
.upload-title { font-size:22px; font-weight:800; color:#312e81; margin-bottom:4px; }
.upload-sub { color:#6b7280; margin-bottom:10px; }
[data-testid="stFileUploader"] {
    background:rgba(255,255,255,.82);
    border:2px dashed #a78bfa;
    border-radius:22px;
    padding:12px;
    box-shadow:0 12px 30px rgba(124,58,237,.08);
}
[data-testid="stFileUploader"]:hover { border-color:#ec4899; }
.stButton > button {
    width:100%; min-height:52px; border:0; border-radius:16px;
    background:linear-gradient(90deg,#7c3aed,#ec4899);
    color:#fff; font-weight:800; font-size:16px;
    box-shadow:0 10px 22px rgba(124,58,237,.18);
}
.stButton > button:hover { transform:translateY(-2px); }
.card {
    background:rgba(255,255,255,.88); border:1px solid #ebe7fa; border-radius:22px;
    padding:22px; min-height:135px; box-shadow:0 10px 30px rgba(99,102,241,.08);
}
.card-title { color:#6b7280; font-size:14px; font-weight:700; }
.card-value {
    font-family:'Space Grotesk',sans-serif; font-size:38px; font-weight:800; margin-top:8px;
    background:linear-gradient(90deg,#7c3aed,#ec4899); -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.section-title { font-family:'Space Grotesk',sans-serif; font-size:28px; font-weight:800; color:#312e81; margin:34px 0 16px; }
.skill {
    display:inline-block; padding:9px 15px; margin:5px; border-radius:999px;
    background:linear-gradient(135deg,#ede9fe,#fce7f3); color:#6d28d9;
    border:1px solid #ddd6fe; font-size:14px; font-weight:700;
}
.mini-card { background:#fff; border:1px solid #eee9ff; border-radius:18px; padding:17px; height:100%; box-shadow:0 7px 20px rgba(99,102,241,.06); }
.mini-card h4 { margin:0 0 7px; color:#312e81; }
.mini-card p { margin:0; color:#6b7280; font-size:14px; }
[data-testid="stAlert"] { border-radius:16px; border:0; }
.stDownloadButton > button { border-radius:15px; background:#f5f3ff; color:#6d28d9; border:1px solid #c4b5fd; font-weight:800; }
.footer { text-align:center; color:#9ca3af; font-size:13px; margin-top:40px; }
@media(max-width:768px){ .block-container{padding-top:1rem;} .hero h1{font-size:39px;} .card-value{font-size:30px;} }
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="font-family:'Space Grotesk';font-size:27px;font-weight:800;
    background:linear-gradient(90deg,#7c3aed,#ec4899);-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;">✨ Resume Glow-Up</div>
    <div style="color:#6b7280;margin-top:5px;">Smart, private & secure</div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌷 What you get")
for item in [
    "📊 Resume score",
    "🎯 ATS-style score",
    "🛠 Skill detection",
    "🚀 Skill gaps",
    "💼 Job-role suggestions",
    "✨ Actionable improvements",
]:
    st.sidebar.markdown(f"• {item}")
st.sidebar.markdown("---")
st.sidebar.info("🔒 **Private analysis.** Your resume is analyzed directly in this app.")

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>✨ AI Resume Analyzer</h1>
        <p>Your resume's glow-up starts here. Upload → Analyze → Improve → Get hired 🚀</p>
        <span class="pill">🔒 Private analysis</span>
        <span class="pill">⚡ Instant analysis</span>
        <span class="pill">📄 PDF support</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# RESUME KNOWLEDGE
# =========================================================

SKILLS = {
    "Python": ["python"], "Java": ["java"], "C++": ["c++", "cpp"],
    "C": ["c programming"], "JavaScript": ["javascript"], "HTML": ["html"],
    "CSS": ["css"], "React": ["react", "react.js"], "Node.js": ["node.js", "nodejs"],
    "Django": ["django"], "Flask": ["flask"], "PHP": ["php"], "SQL": ["sql"],
    "MySQL": ["mysql"], "MongoDB": ["mongodb"], "Git": ["git"], "GitHub": ["github"],
    "Machine Learning": ["machine learning", "machine-learning"], "Deep Learning": ["deep learning"],
    "Data Analysis": ["data analysis", "data analytics"], "Pandas": ["pandas"],
    "NumPy": ["numpy"], "Scikit-learn": ["scikit-learn", "sklearn"], "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"], "Power BI": ["power bi"], "Excel": ["excel"], "AWS": ["aws"],
    "Azure": ["azure"], "Docker": ["docker"], "Cybersecurity": ["cybersecurity", "cyber security"],
    "Networking": ["networking", "computer networks"], "Linux": ["linux"],
    "Cloud Computing": ["cloud computing", "cloud"], "REST API": ["rest api", "restful"],
    "Figma": ["figma"], "Canva": ["canva"],
}

SECTION_KEYWORDS = {
    "Education": ["education", "qualification", "academic", "degree", "bca", "b.tech", "btech", "mca"],
    "Experience": ["experience", "employment", "work history", "internship", "intern"],
    "Projects": ["projects", "project"],
    "Skills": ["skills", "technical skills", "technologies"],
    "Certifications": ["certification", "certifications", "certificate"],
    "Achievements": ["achievement", "achievements", "awards"],
    "Contact": ["email", "phone", "contact", "linkedin", "github"],
    "Summary": ["summary", "objective", "profile", "about me"],
}

ROLE_KEYWORDS = {
    "Python Developer": ["python", "django", "flask"],
    "Data Analyst": ["python", "sql", "pandas", "excel", "power bi", "data analysis"],
    "Machine Learning Engineer": ["python", "machine learning", "scikit-learn", "tensorflow", "pytorch"],
    "Web Developer": ["html", "css", "javascript"],
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["python", "django", "flask", "node.js", "sql"],
    "Cybersecurity Analyst": ["cybersecurity", "networking", "linux"],
    "Cloud Engineer": ["aws", "azure", "docker", "cloud computing", "linux"],
}

RECOMMENDED_SKILLS = [
    "Python", "SQL", "Git", "Data Analysis", "Machine Learning",
    "Cloud Computing", "Communication", "Problem Solving", "REST API",
]

ACTION_VERBS = {
    "developed", "built", "created", "implemented", "designed", "automated",
    "analyzed", "optimized", "deployed", "led", "managed", "improved",
    "engineered", "integrated", "tested", "configured", "delivered",
}

# =========================================================
# HELPERS
# =========================================================

def extract_text(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text += page_text + "\n"
    except Exception as exc:
        st.error(f"Could not read this PDF: {exc}")
    return text


def contains_keyword(text_lower: str, keyword: str) -> bool:
    if re.fullmatch(r"[a-zA-Z]+", keyword):
        return bool(re.search(rf"\b{re.escape(keyword.lower())}\b", text_lower))
    return keyword.lower() in text_lower


def find_skills(text: str):
    lower = text.lower()
    found = []
    for skill, keywords in SKILLS.items():
        if any(contains_keyword(lower, kw) for kw in keywords):
            found.append(skill)
    return found


def check_sections(text: str):
    lower = text.lower()
    return {
        section: any(contains_keyword(lower, kw) for kw in keywords)
        for section, keywords in SECTION_KEYWORDS.items()
    }


def analyze_resume(text: str):
    lower = text.lower()
    words = re.findall(r"\b[a-zA-Z][a-zA-Z+.#-]*\b", text)
    word_count = len(words)
    skills = find_skills(text)
    sections = check_sections(text)

    section_score = round(sum(sections.values()) / len(sections) * 100)
    skill_score = min(100, len(skills) * 8)
    length_score = 100 if 350 <= word_count <= 900 else 82 if 250 <= word_count <= 1100 else 60
    contact_score = 100 if sections["Contact"] else 30
    project_score = 100 if sections["Projects"] else 40
    experience_score = 100 if sections["Experience"] else 55
    achievement_score = 100 if sections["Achievements"] else 55

    quantified = len(re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|percent|x|k|m|hours|users|projects?)\b", lower))
    action_verbs = sum(1 for verb in ACTION_VERBS if re.search(rf"\b{re.escape(verb)}\b", lower))
    quant_score = min(100, quantified * 25)
    action_score = min(100, action_verbs * 10)

    resume_score = round(
        0.20 * section_score +
        0.18 * skill_score +
        0.14 * length_score +
        0.12 * contact_score +
        0.12 * project_score +
        0.10 * experience_score +
        0.07 * quant_score +
        0.07 * action_score
    )
    ats_score = round(0.35 * section_score + 0.25 * skill_score + 0.20 * length_score + 0.10 * quant_score + 0.10 * action_score)

    missing_skills = [s for s in RECOMMENDED_SKILLS if s not in skills]

    role_matches = []
    for role, required in ROLE_KEYWORDS.items():
        matched = 0
        for key in required:
            if contains_keyword(lower, key):
                matched += 1
        if matched:
            score = round(matched / len(required) * 100)
            role_matches.append((role, score))
    role_matches.sort(key=lambda x: x[1], reverse=True)
    role_matches = role_matches[:5] or [("Software Developer", 40), ("IT Support Specialist", 30)]

    strengths = []
    if sections["Skills"]:
        strengths.append("Your skills section is easy for a recruiter or ATS to locate.")
    if sections["Projects"]:
        strengths.append("Projects are present, which helps demonstrate practical ability.")
    if len(skills) >= 6:
        strengths.append(f"You have a solid technical stack with {len(skills)} detected skills.")
    if quantified:
        strengths.append("You use measurable details in parts of the resume.")
    if sections["Education"]:
        strengths.append("Education information is clearly represented.")
    if not strengths:
        strengths.append("The PDF contains readable resume content that can be analyzed.")

    weaknesses = []
    if not sections["Summary"]:
        weaknesses.append("Add a short 2–3 line professional summary tailored to the target role.")
    if not sections["Experience"]:
        weaknesses.append("If you have internships, training, or work experience, add a dedicated Experience section.")
    if not sections["Projects"]:
        weaknesses.append("Add 2–3 projects with your contribution, technologies and measurable results.")
    if not sections["Certifications"]:
        weaknesses.append("Relevant certifications can strengthen the profile.")
    if not quantified:
        weaknesses.append("Add numbers such as %, users, time saved, accuracy or project size where truthful.")
    if len(skills) < 5:
        weaknesses.append("Add more relevant job-specific skills instead of listing only generic tools.")
    if word_count < 250:
        weaknesses.append("The resume is quite short; add evidence of projects, achievements or experience.")
    if word_count > 1100:
        weaknesses.append("Trim repetitive content and keep the resume focused.")

    suggestions = [
        "Tailor the top third of the resume to the exact job description.",
        "Start bullet points with strong action verbs and show the outcome of your work.",
        "Keep dates, headings, spacing and bullet formatting consistent for ATS readability.",
    ]
    if missing_skills:
        suggestions.append("Prioritize only the missing skills that genuinely match the jobs you want; do not add skills you cannot use.")

    return {
        "resume_score": max(0, min(100, resume_score)),
        "ats_score": max(0, min(100, ats_score)),
        "skills": skills,
        "missing_skills": missing_skills,
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:6],
        "suggestions": suggestions,
        "role_matches": role_matches,
        "word_count": word_count,
        "pages": None,
        "score_breakdown": {
            "Skills": skill_score,
            "Sections": section_score,
            "Projects": project_score,
            "Experience": experience_score,
            "Impact": round((quant_score + action_score) / 2),
        },
        "sections": sections,
    }


def score_label(score: int):
    if score >= 85:
        return "Excellent ✨"
    if score >= 70:
        return "Good 💜"
    if score >= 55:
        return "Needs a glow-up 🌷"
    return "Needs improvement 🛠️"

# =========================================================
# UPLOAD
# =========================================================

st.markdown('<div class="upload-title">📄 Drop your resume here</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-sub">Let\'s see how recruiter-ready you are 👀</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "✨ Choose your PDF",
    type=["pdf"],
    help="Upload a text-based PDF resume. Scanned image-only PDFs may not have extractable text.",
)

if uploaded_file:
    file_bytes = uploaded_file.getvalue()
    st.success(f"✅ {uploaded_file.name} is ready")

    if st.button("✨ Give My Resume a Glow-Up 🚀"):
        with st.spinner("🔍 Reading your resume and checking recruiter essentials..."):
            resume_text = extract_text(file_bytes)

        if not resume_text.strip():
            st.error("❌ I couldn't extract text from this PDF. Try a text-based PDF instead of a scanned image PDF.")
            st.stop()

        data = analyze_resume(resume_text)
        st.session_state["resume_analysis"] = data

# =========================================================
# RESULTS
# =========================================================

if "resume_analysis" in st.session_state:
    data = st.session_state["resume_analysis"]

    st.markdown('<div class="section-title">📊 Your Resume Snapshot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🏆 Resume Score", f'{data["resume_score"]}/100', score_label(data["resume_score"])),
        ("🎯 ATS-style Score", f'{data["ats_score"]}/100', "Keyword + structure check"),
        ("🛠 Skills Found", str(len(data["skills"])), "Technical skills detected"),
        ("📝 Word Count", str(data["word_count"]), "Content length"),
    ]
    for col, (title, value, subtitle) in zip((c1, c2, c3, c4), cards):
        with col:
            st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-value">{value}</div><div style="color:#8b5cf6;font-size:13px;font-weight:700;margin-top:5px">{subtitle}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">💫 Quick Verdict</div>', unsafe_allow_html=True)
    st.info(f"Your resume currently looks **{score_label(data['resume_score'])}**. Focus first on the items under **Areas to Improve** and **Skills You Could Add**.")

    # Score + role match
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-title">📈 Score Breakdown</div>', unsafe_allow_html=True)
        b = data["score_breakdown"]
        fig = go.Figure(go.Scatterpolar(r=list(b.values()), theta=list(b.keys()), fill="toself", line=dict(width=3)))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#e5e7eb"), bgcolor="rgba(255,255,255,0.0)"),
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#312e81"), margin=dict(l=30,r=30,t=30,b=30), height=360,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        st.markdown('<div class="section-title">💼 Best-Match Roles</div>', unsafe_allow_html=True)
        for role, score in data["role_matches"]:
            st.markdown(f"**{role}** &nbsp; `{score}% match`")
            st.progress(score / 100)

    # Strengths / weaknesses
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="section-title">💪 Your Wins</div>', unsafe_allow_html=True)
        for item in data["strengths"]:
            st.success(f"✓ {item}")
    with b:
        st.markdown('<div class="section-title">⚠️ Level Up</div>', unsafe_allow_html=True)
        for item in data["weaknesses"]:
            st.warning(f"• {item}")

    # Skills
    st.markdown('<div class="section-title">🛠️ Your Skill Stack</div>', unsafe_allow_html=True)
    if data["skills"]:
        st.markdown("".join(f'<span class="skill">{skill}</span>' for skill in data["skills"]), unsafe_allow_html=True)
    else:
        st.warning("No common technical skills were detected. Add a clear Skills section with technologies you actually know.")

    st.markdown('<div class="section-title">🚀 Skills You Could Add</div>', unsafe_allow_html=True)
    if data["missing_skills"]:
        mc = st.columns(3)
        for i, skill in enumerate(data["missing_skills"]):
            with mc[i % 3]:
                st.markdown(f'<div class="mini-card"><h4>+ {skill}</h4><p>Consider it only if it fits your target role and you can genuinely demonstrate it.</p></div>', unsafe_allow_html=True)
    else:
        st.success("Your resume already covers the current recommended skill set. 🎉")

    # Sections checklist
    st.markdown('<div class="section-title">🧩 Resume Checklist</div>', unsafe_allow_html=True)
    section_cols = st.columns(4)
    for i, (section, present) in enumerate(data["sections"].items()):
        with section_cols[i % 4]:
            icon = "✅" if present else "➕"
            st.markdown(f'<div class="mini-card"><h4>{icon} {section}</h4><p>{"Found" if present else "Not detected"}</p></div>', unsafe_allow_html=True)

    # Suggestions
    st.markdown('<div class="section-title">✨ Your Glow-Up Plan</div>', unsafe_allow_html=True)
    for i, suggestion in enumerate(data["suggestions"], 1):
        st.markdown(f"**{i}.** {suggestion}")

    # Download report
    report = f"""AI RESUME ANALYZER\n==================\n\nResume Score: {data['resume_score']}/100\nATS-style Score: {data['ats_score']}/100\nWord Count: {data['word_count']}\n\nSKILLS\n------\n{', '.join(data['skills']) or 'None detected'}\n\nSTRENGTHS\n---------\n""" + "\n".join(f"- {x}" for x in data["strengths"]) + f"\n\nAREAS TO IMPROVE\n----------------\n" + "\n".join(f"- {x}" for x in data["weaknesses"]) + f"\n\nSKILLS TO CONSIDER\n------------------\n" + "\n".join(f"- {x}" for x in data["missing_skills"]) + f"\n\nRECOMMENDED ROLES\n-----------------\n" + "\n".join(f"- {role}: {score}% match" for role, score in data["role_matches"])

    st.download_button("📥 Download My Resume Analysis", report, file_name="resume_analysis.txt", mime="text/plain")

st.markdown('<div class="footer">Made with ✨ for a better resume • Private local analysis</div>', unsafe_allow_html=True)
