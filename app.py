# import nltk

# # Download required tokenizer(s)
# nltk.download('punkt')        # Most common tokenizer
# nltk.download('punkt_tab')    # Ignore error if it fails, just trying based on message

# # Tokenization example
# from nltk.tokenize import word_tokenize

# text = "Hello, this is an example."
# tokens = word_tokenize(text)
# print(tokens)
# import fitz  # PyMuPDF

# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# resume_text = extract_text_from_pdf("Yash resumeee.pdf")  # File ka exact naam likha gaya hai
# print("Resume Text:\n")
# print(resume_text)


# import fitz  # PyMuPDF
# import nltk
# from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import CountVectorizer

# nltk.download('punkt')
# nltk.download('punkt_tab')

# # 1. Extract text from resume
# with fitz.open("Yash resumeee.pdf") as doc:
#     resume_text = ""
#     for page in doc:
#         resume_text += page.get_text()

# print("Resume Text:\n")
# print(resume_text)

# # 2. Manually provide Job Description
# job_description = """
# We are looking for a candidate with strong communication skills, experience with MS Excel, and basic accounting knowledge. The ideal candidate should be a team player with a keen interest in business and finance.
# """

# # 3. Preprocess and Tokenize both texts
# resume_tokens = word_tokenize(resume_text.lower())
# jd_tokens = word_tokenize(job_description.lower())

# # 4. Extract keywords from JD (simple way)
# jd_keywords = set(jd_tokens) - set(nltk.corpus.stopwords.words('english'))

# # 5. Match keywords in resume
# matched_keywords = [word for word in resume_tokens if word in jd_keywords]
# match_score = len(matched_keywords)

# print("\nMatched Keywords:")
# print(matched_keywords)
# print(f"\nScore: {match_score} keywords matched from job description.")



# main code

from flask import Flask, render_template, request, redirect, url_for
import os
import PyPDF2
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy Job Description
job_description = """
We are looking for a skilled Full Stack Developer with expertise in Python (Flask/Django) and modern JavaScript frameworks (React/Angular/Vue). The ideal candidate should be able to design scalable backend APIs, integrate with frontend interfaces, and deploy applications using modern DevOps practices.
"""

# Extract keywords from job description
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = set(word for word in words if len(word) > 3)
    return keywords

job_keywords = extract_keywords(job_description)

# Extract text from resume
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.lower()

# Generate Searchability Suggestions
def generate_searchability_suggestions(resume_text):
    suggestions = []
    if "email" not in resume_text or not re.search(r'[\w\.-]+@[\w\.-]+', resume_text):
        suggestions.append("Add a professional email address to your resume.")
    if "phone" not in resume_text or not re.search(r'\+?\d[\d\s\-()]{7,}\d', resume_text):
        suggestions.append("Include a valid phone number.")
    if "summary" not in resume_text:
        suggestions.append("Consider adding a professional summary at the top of your resume.")
    return suggestions

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(request.url)

    resume_file = request.files['resume']
    if resume_file.filename == '':
        return redirect(request.url)

    if resume_file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)
        resume_words = set(re.findall(r'\b\w+\b', resume_text))

        matched_keywords = job_keywords & resume_words
        match_score = int((len(matched_keywords) / len(job_keywords)) * 100)

        # Metrics
        metrics = {
            "Searchability": 70,
            "Hard Skills": 90 if "sql" in resume_words else 60,
            "Soft Skills": 85,
            "Recruiter Tips": 40,
            "Formatting": 75
        }

        suggestions = generate_searchability_suggestions(resume_text)

        return render_template("result.html", score=match_score, metrics=metrics, suggestions=suggestions)

# ✅ Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    show_alert = request.method == 'POST'
    return render_template('login.html', show_alert=show_alert)

##✅ Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    show_alert = request.method == 'POST'
    return render_template('signup.html', show_alert=show_alert)

if __name__ == '__main__':
    app.run(debug=True)




