import os
from dotenv import load_dotenv
import json
import re
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 1: Configure Gemini API
# Load API key from .env file
load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GENAI_API_KEY:
    st.error("Missing Gemini API key. Set it as an environment variable.")
else:
    genai.configure(api_key=GENAI_API_KEY)

# ✅ Step 2: Upload and save PDF
pdf_directory = "uploads/"
def upload_pdf(file):
    os.makedirs(pdf_directory, exist_ok=True)
    file_path = os.path.join(pdf_directory, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

# ✅ Step 3: Extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# ✅ Step 4: Split text into chunks
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

# ✅ Step 5: Analyze resume using Gemini AI
def analyze_resume_with_gemini(text):
    prompt = f"""
    Extract key information from the resume in strict JSON format:
    {{
        "domain": "Extracted domain",
        "skills": ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5"],
        "work_experience": "Work experience summary",
        "strength": "One strong point",
        "weakness": "One area of improvement"
    }}
    Resume Content:
    {text}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}|\[.*\]', response.text.strip(), re.DOTALL)
        return json.loads(match.group(0)) if match else None
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None

# ✅ Step 6: Generate Interview Questions
def generate_interview_questions(resume_data):
    prompt = f"""
    Generate 5 interview questions based on the resume, along with correct answers:
    
    Resume Data:
    {json.dumps(resume_data, indent=4)}
    
    Response Format:
    [
        {{"id": 1, "question": "Question 1", "answer": "Correct answer 1"}},
        {{"id": 2, "question": "Question 2", "answer": "Correct answer 2"}},
        {{"id": 3, "question": "Question 3", "answer": "Correct answer 3"}},
        {{"id": 4, "question": "Question 4", "answer": "Correct answer 4"}},
        {{"id": 5, "question": "Question 5", "answer": "Correct answer 5"}}
    ]
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}|\[.*\]', response.text.strip(), re.DOTALL)
        return json.loads(match.group(0)) if match else None
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None