import os
import json
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv

import google.generativeai as genai

# Load environment variables and configure the API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_ai_response(prompt: str) -> str:
    """Get a response from the AI model based on the input prompt."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def extract_pdf_text(uploaded_file) -> str:
    """Extract text from the uploaded PDF file."""
    reader = pdf.PdfReader(uploaded_file)
    text = ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# some of the prompts , they can be fine tuned and optimised for better functionalities and new functionalities can be added
data_science_prompt = """
Act like a skilled or very experienced ATS (Applicant Tracking System) with a deep understanding of tech fields, especially in data science, machine learning, and data analytics. Your task is to evaluate the resume based on the given job description. Consider that the job market is highly competitive and provide the best assistance for improving the resume. Assign the percentage matching based on the job description and identify the missing keywords with high accuracy.

Resume: {text}
Description: {jd}

Expected response structure: '{{"JD Match": "%", "Missing Keywords": [], "Profile Summary": ""}}'
"""


resume_feedback_prompt = """
Provide detailed feedback on the resume, focusing on the candidate's strengths and weaknesses in data science and machine learning. Highlight key areas such as project experience, programming languages proficiency (Python, R, SQL), analytical skills, statistical knowledge, and relevant coursework or certifications (e.g., TensorFlow certification, Coursera Machine Learning course).

Resume: {text}
"""

skill_improvement_prompt = """
Given the job description and the candidate's resume, identify specific data science and machine learning skills or areas the candidate could improve or learn. Offer actionable advice for improvement, considering the current job market trends and the technologies and methodologies that are in demand (e.g., deep learning, NLP, big data analytics, cloud computing skills).

Job Description: {jd}
Resume: {text}
"""

percentage_match_prompt = """
Evaluate the resume against the job description, focusing specifically on data science and machine learning skills, technologies, and methodologies mentioned. Calculate the match percentage and identify any crucial missing keywords or skills from the resume that are vital for the position. Consider technical skills (e.g., Python, R, SQL), soft skills (e.g., problem-solving, communication), and domain-specific knowledge (e.g., bioinformatics for a data science role in a biotech company).

Job Description: {jd}
Resume: {text}

Expected format: 'Match Percentage: %, Missing Keywords: []'
"""

def main():
    
    st.title('Data Science & ML Resume Analyzer')
    st.subheader('Optimize your resume for Data Science and ML roles')

    jd = st.text_area('Job Description')
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type='pdf')

    if uploaded_file and jd:
        resume_text = extract_pdf_text(uploaded_file)

        if st.button("Analyze Resume"):
            with st.spinner('Analyzing your resume... Please wait'):
                formatted_prompt = data_science_prompt.format(text=resume_text, jd=jd)
                response = get_ai_response(formatted_prompt)
                try:
                    response_data = json.loads(response)
                    st.json(response_data)
                except json.JSONDecodeError:
                    
                    st.write(response)

        if st.button("Detailed Resume Feedback"):
            with st.spinner('Generating detailed feedback... Please wait'):
                formatted_prompt = resume_feedback_prompt.format(text=resume_text)
                response = get_ai_response(formatted_prompt)
                try:
                    response_data = json.loads(response)
                    st.json(response_data)
                except json.JSONDecodeError:
                    
                    st.write(response)

        if st.button("Skill Improvement Suggestions"):
            with st.spinner('Suggesting skill improvements... Please wait'):
                formatted_prompt = skill_improvement_prompt.format(text=resume_text, jd=jd)
                response = get_ai_response(formatted_prompt)
                try:
                    response_data = json.loads(response)
                    st.json(response_data)
                except json.JSONDecodeError:
                    
                    st.write(response)

        if st.button("Percentage Match & Missing Keywords"):
            with st.spinner('Calculating percentage match and missing keywords... Please wait'):
                formatted_prompt = percentage_match_prompt.format(text=resume_text, jd=jd)
                response = get_ai_response(formatted_prompt)
                try:
                    response_data = json.loads(response)
                    st.json(response_data)
                except json.JSONDecodeError:
                    
                    st.write(response)
    else:
        st.error("Please upload a resume and paste a job description.")

if __name__ == "__main__":
    main()
