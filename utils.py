import os
from groq import Groq
import PyPDF2 as pdf
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file uploaded via Streamlit.
    """
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            _page = reader.pages[page]
            text += str(_page.extract_text())
        return text
    except Exception as e:
        logging.error(f"Error extracting PDF text: {e}")
        return None

def get_groq_response(input_prompt, pdf_content, jd_text, api_key):
    """
    Sends the resume content and JD to Groq and retrieves the analysis.
    """
    client = Groq(api_key=api_key)
    
    # Construct the full prompt
    full_prompt = f"""
    {input_prompt}
    
    Job Description:
    {jd_text}
    
    Resume Content:
    {pdf_content}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error communicating with Groq: {e}")
        raise e

def parse_json_response(response_text):
    """
    Parses the JSON string returned by Gemini.
    Handles potential markdown fencing (```json ... ```).
    """
    try:
        if not response_text:
            return None
        # Clean the response text to remove markdown code blocks if present
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        return None

# Prompt Template
ANALYSIS_PROMPT = """
You are a strict, no-nonsense Senior Technical Recruiter and ATS Optimization Expert. 
Your task is to brutally evaluate the provided resume against the given Job Description (JD). 
Do not sugarcoat your feedback. Be direct and critical. Point out every flaw, missing skill, and weakness. 

Please provide a detailed analysis in a strictly structured JSON format. 
Do not include any introductory or concluding text, only the valid JSON object.

The JSON object must have the following structure:
{
    "match_percentage": "Integer between 0 and 100",
    "match_summary": "A brief 2-3 sentence summary of the overall fit.",
    "hiring_manager_persona": "A brief description of the persona evaluating this resume (e.g., 'Senior Python Developer' or 'HR Manager')",
    "missing_keywords": ["List", "of", "important", "technical", "keywords", "missing", "from", "the", "resume"],
    "critical_skills_gap": ["List", "of", "critical", "skills", "or", "certifications", "required", "by", "JD", "but", "absent"],
    "section_analysis": {
        "professional_summary": "Specific advice to improve the summary section.",
        "projects": "Specific advice to improve the projects section.",
        "work_experience": "Specific advice to improve the work experience section (e.g., quantifiable metrics)."
    },
    "ats_check": {
        "status": "Pass/Warning/Fail",
        "issues": ["List", "of", "formatting", "or", "structure", "issues", "that", "might", "confuse", "ATS"]
    }
}
"""
