✨ AI Resume Analyzer

A modern, lightweight Resume Analyzer built with Streamlit. Upload a PDF resume and get an instant resume snapshot with ATS-style scoring, skill detection, skill gaps, job-role suggestions, strengths, weaknesses, and improvement recommendations.

🌸 Highlights

📄 PDF resume upload

📊 Resume score

🎯 ATS-style score

🛠 Technical skill detection

🚀 Recommended / missing skills

💼 Suitable job-role suggestions

💪 Resume strengths

⚠️ Areas to improve

📈 Resume score breakdown

📝 Resume word count

📥 Downloadable text analysis report

🎨 Light, colorful Gen-Z-inspired interface

🔒 Private local analysis

☁️ Streamlit deployment ready

🧰 Tech Stack

Python

Streamlit

pdfplumber — PDF text extraction

Plotly — score visualization

📁 Project Structure

AI_Resume_Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── config.toml

🚀 Run Locally

1. Clone or download the project

Open the project folder in VS Code.

2. Install dependencies

pip install -r requirements.txt

3. Start Streamlit

streamlit run app.py

The application will open in your browser.

☁️ Deploy on Streamlit Community Cloud

Create a GitHub repository.

Upload:

app.py

requirements.txt

README.md

.streamlit/config.toml

Open Streamlit Community Cloud.

Select Deploy an app.

Choose your GitHub repository and app.py.

Deploy.

No API-key configuration is required for this version.

🧠 How It Works

Upload Resume PDF
       ↓
Extract PDF Text
       ↓
Detect Resume Sections
       ↓
Detect Technical Skills
       ↓
Calculate Resume / ATS-style Scores
       ↓
Find Skill Gaps
       ↓
Suggest Job Roles
       ↓
Generate Improvement Suggestions
       ↓
Display Resume Dashboard

📊 Analysis Areas

Resume Score

An overall score based on detected resume sections, skills, content length, contact information, projects, and experience.

ATS-style Score

A rule-based estimate of how complete and readable the resume structure is for an ATS-oriented review.

Skill Detection

The analyzer checks the resume text for common technologies and skills such as:

Python

Java

C / C++

JavaScript

HTML / CSS

React

Django / Flask

SQL / MySQL

Git / GitHub

Machine Learning

Data Analysis

Pandas / NumPy

Scikit-learn

TensorFlow / PyTorch

Power BI / Excel

AWS / Azure

Docker

Linux

Cybersecurity

Networking

Cloud Computing

Job Roles

Possible roles are suggested according to the skills detected in the uploaded resume.

🔐 Privacy

The application is designed for local, rule-based resume analysis. It does not require the user to enter an external AI API key.

Note: Despite the product name AI Resume Analyzer, this version uses programmatic/rule-based analysis rather than a generative AI model. Scores and recommendations should therefore be treated as guidance, not as a guarantee of ATS or recruiter outcomes.

⚠️ PDF Limitation

The analyzer works best with text-based PDFs. Scanned/image-only resumes may not contain extractable text and may produce limited results.

🎓 Project Use

This project is suitable for:

College mini projects

Final-year projects

Python / Streamlit projects

Resume-analysis demonstrations

Portfolio projects

GitHub projects

📌 Future Enhancements

Possible future improvements include:

Job-description matching

More advanced NLP

Semantic skill matching

Resume section quality analysis

Resume rewriting

Cover-letter generation

Interview-question generation

PDF report generation

Multiple resume formats

Resume version comparison

📄 License

This project can be used and modified for educational and portfolio purposes.