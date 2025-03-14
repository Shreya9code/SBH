import json
import re
import textstat  # For readability analysis
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ✅ Load API Key from .env
load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GENAI_API_KEY:
    st.error("Missing Gemini API key. Set it as an environment variable.")
else:
    genai.configure(api_key=GENAI_API_KEY)


def calculate_resume_score(resume_text):
    """Generates a quality score for a resume based on clarity, structure, and grammar."""
    
    # ✅ Readability Score (Higher is better)
    #readability_score = textstat.flesch_reading_ease(resume_text)
    readability_score = textstat.flesch_reading_ease(resume_text)
    if readability_score < 0:
        readability_score = 0  # Ensure no negative scores

    # ✅ Check for Missing Sections
    missing_sections = []
    important_sections = ["Experience", "Education", "Skills", "Achievements", "Projects"]
    for section in important_sections:
        if section.lower() not in resume_text.lower():
            missing_sections.append(section)

    # ✅ Grammar & Spelling Check with Gemini
    prompt = f"""
    Analyze the following resume and return a quality score (0-100%).
    Evaluate based on grammar, clarity, structure, and keyword optimization.

    Resume Content:
    {resume_text}

    Response Format:
    {{
        "score": "Calculated score (0-100%)",
        "grammar_issues": ["Issue 1", "Issue 2"],
        "suggestions": "Improvement tips"
    }}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}|\[.*\]', response.text.strip(), re.DOTALL)
        ai_feedback = json.loads(match.group(0)) if match else {}

        return {
            "score": ai_feedback.get("score", "N/A"),
            "readability": readability_score,
            "missing_sections": missing_sections,
            "grammar_issues": ai_feedback.get("grammar_issues", []),
            "suggestions": ai_feedback.get("suggestions", "No suggestions")
        }
    except Exception as e:
        return {"error": f"Gemini API error: {e}"}
# ✅ Function: Match Resume with Job Description
def match_resume_with_job(resume_data, job_description):
    """Compares resume details with job description & returns a match percentage."""
    # ✅ Extract Keywords from Job Description (For ATS Matching)
    job_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
    resume_words = set(re.findall(r'\b\w+\b', resume_data.lower()))
    matched_keywords = job_keywords.intersection(resume_words)

    # ✅ Calculate ATS Score (Keyword Match Percentage)
    ats_score = round((len(matched_keywords) / len(job_keywords)) * 100, 2) if job_keywords else 0

    prompt = f"""
    You are an AI that evaluates resumes based on job descriptions. Given the following resume and job description, return:
    - `"match_percentage"`: How well the resume fits the job (0-100%).
    - `"missing_skills"`: List of missing skills.
    - `"ats_score"`: Percentage of job description keywords present in resume.

    Resume Data:
    {json.dumps(resume_data, indent=4)}

    Job Description:
    {job_description}

    Response Format:
    {{
        "match_percentage": "Calculated match percentage",
        "missing_skills": ["Missing skill 1", "Missing skill 2", "Missing skill 3"],
        "ats_score": "{ats_score}"

    }}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}|\[.*\]', response.text.strip(), re.DOTALL)
        ai_result = json.loads(match.group(0)) if match else {}
        ai_result["ats_score"] = ats_score  # Add ATS Score to Response
        return ai_result
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None
