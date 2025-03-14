import streamlit as st
from pdf_rag import upload_pdf, extract_text_from_pdf, split_text, analyze_resume_with_gemini, generate_interview_questions
from resume_screening import match_resume_with_job,calculate_resume_score
from pdf_extraction_feature import extract_text_from_pdf

# Streamlit UI
st.set_page_config(page_title="AI Resume Interview", layout="wide")

st.title("📄 AI Resume Interview & Screening")

# File uploader: Accept only PDF resumes
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf", accept_multiple_files=False)

if uploaded_file:
    with st.spinner("Processing resume..."):
        file_path = upload_pdf(uploaded_file)  # ✅ Save file locally
        extracted_text = extract_text_from_pdf(file_path)  # ✅ Get text
        text_chunks = split_text(extracted_text)  # ✅ Split text

        # Convert chunks into a single text block
        indexed_resume = " ".join(text_chunks)

        # AI-powered resume analysis
        resume_data = analyze_resume_with_gemini(indexed_resume)
        if resume_data:
            st.success("✅ Resume processed successfully!")
            st.subheader("Extracted Resume Information")
            st.json(resume_data)

             # 📌 Generate Resume Quality Score & Feedback
            if st.button("Analyze Resume Quality"):
                with st.spinner("Analyzing resume..."):
                    resume_analysis = calculate_resume_score(extracted_text)
            
                if "error" not in resume_analysis:
                    st.subheader("📊 Resume Quality Score")
                    st.metric("Score (0-100%)", resume_analysis["score"])
                    st.metric("Readability Score", resume_analysis["readability"])

                    st.subheader("⚠️ Missing Sections")
                    st.write(resume_analysis["missing_sections"])

                    st.subheader("✍️ Grammar Issues")
                    st.write(resume_analysis["grammar_issues"])

                    st.subheader("🔍 Suggestions")
                    st.write(resume_analysis["suggestions"])
                else:
                    st.error(resume_analysis["error"])

            # ✅ Generate AI-Powered Interview Questions
            if st.button("Generate Interview Questions"):
                with st.spinner("Generating questions..."):
                    questions = generate_interview_questions(resume_data)  # ✅ Correct input
                st.subheader("🤖 Interview Questions")
                for q in questions:
                    st.write(f"**Q{q['id']}: {q['question']}**")

        # Resume Screening (Job Matching)
        job_description = st.text_area("Paste Job Description Here:")
        if st.button("Match Resume with Job"):
            with st.spinner("Analyzing resume match..."):
                match_result = match_resume_with_job(resume_data, job_description)
            if match_result:
                st.subheader("📊 Resume Match Results")
                st.write(f"✅ **Match Percentage:** {match_result['match_percentage']}%")
                st.write(f"❌ **Missing Skills:** {', '.join(match_result['missing_skills'])}")