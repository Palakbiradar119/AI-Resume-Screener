import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze(resume, jd):
    prompt = f"""
    Compare this resume with job description.
    Resume:
    {resume}
    Job Description:
    {jd}
    Give output like:
    Match Score: XX%
    Missing Skills:
    - skill1
    - skill2
    Suggestions:
    - suggestion1
    Final Verdict: Selected/Rejected
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

st.title("📄 AI Resume Screener")
file = st.file_uploader("Upload Resume", type="pdf")
jd = st.text_area("Paste Job Description")

if file and jd:
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            resume_text = extract_text(file)
            result = analyze(resume_text, jd)
        st.success("Analysis Completed!")
        st.write(result)
