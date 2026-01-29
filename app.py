import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, get_groq_response, parse_json_response, ANALYSIS_PROMPT
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="ResuMate - AI Resume Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ... (CSS styles remain same, so I will target just the configuration and main title blocks separately if needed, or just replace the chunks)
# Actually, I can just replace the specific lines since they are separate.

# Let's target the page config first


# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        color: #1e1e1e;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# API Key Handling (Local .env or Cloud Secrets)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = None

if not api_key:
    st.warning("⚠️ **API Key Missing**: Please set `GROQ_API_KEY` in your `.env` file (local) or Streamlit Secrets (cloud).")


# Main Title and Description
st.title("🚀 ResuMate")
st.caption("Your AI-powered partner for landing the perfect job.")
st.markdown("Optimize your resume, beat the ATS, and get hired faster. Upload your PDF and paste the JD below.")

# Input Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf", help="Upload your resume in PDF format.")

with col2:
    st.subheader("2. Job Description")
    jd_text = st.text_area("Paste Job Description Here", height=250, placeholder="Paste the full job description here...")

# Analysis Button
analyze_button = st.button("Analyze Resume")

if analyze_button:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not uploaded_file:
        st.error("Please upload a PDF resume.")
    elif not jd_text:
        st.error("Please paste a job description.")
    else:
        with st.spinner("⏳ Analyzing (Llama 3 is fast!)..."):
            # 1. Extract Text
            text = extract_text_from_pdf(uploaded_file)
            
            if text:
                # 2. Get AI Response
                try:
                    response_text = get_groq_response(ANALYSIS_PROMPT, text, jd_text, api_key)
                    
                    # 3. Parse Response
                    data = parse_json_response(response_text)
                    
                    if data:
                        st.success("Analysis Complete!")
                        time.sleep(0.5) # Brief pause for effect
                        
                        # --- Results Layout ---
                        
                        # Row 1: Score and Summary
                        score_col, summary_col = st.columns([1, 2])
                        
                        with score_col:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>Match Score</h3>
                                <h1 style="color: #4CAF50; font-size: 64px;">{data.get('match_percentage', 0)}%</h1>
                            </div>
                            """, unsafe_allow_html=True)
                            st.progress(int(data.get('match_percentage', 0)) / 100)
                        
                        with summary_col:
                            st.markdown("### 📝 Analysis Summary")
                            st.info(data.get('match_summary', 'No summary provided.'))
                            st.markdown(f"**Persona:** *{data.get('hiring_manager_persona', 'Recruiter')}*")

                        st.markdown("---")
                        
                        # Row 2: Keyword Gap Analysis
                        st.subheader("🔑 Keyword Analysis")
                        missing = data.get('missing_keywords', [])
                        critical_gap = data.get('critical_skills_gap', [])
                        
                        k_col1, k_col2 = st.columns(2)
                        
                        with k_col1:
                            st.markdown("#### Missing Keywords")
                            if missing:
                                st.write("These keywords are in the JD but missing from your resume:")
                                # Display chips or bullets
                                for kw in missing:
                                    st.markdown(f"- ❌ {kw}")
                            else:
                                st.success("Great job! No major keywords missing.")
                                
                        with k_col2:
                            st.markdown("#### Critical Skills Gap")
                            if critical_gap:
                                st.error("⚠️ Critical missing skills/certs:")
                                for skill in critical_gap:
                                    st.markdown(f"- {skill}")
                            else:
                                st.success("You have all the critical skills listed!")

                        st.markdown("---")

                        # Row 3: Section Analysis
                        st.subheader("📄 Section-by-Section Improvements")
                        sections = data.get('section_analysis', {})
                        
                        with st.expander("Professional Summary", expanded=True):
                            st.write(sections.get('professional_summary', 'No feedback.'))
                            
                        with st.expander("Projects"):
                            st.write(sections.get('projects', 'No feedback.'))
                            
                        with st.expander("Work Experience"):
                            st.write(sections.get('work_experience', 'No feedback.'))

                        st.markdown("---")
                        
                        # Row 4: ATS Check
                        ats = data.get('ats_check', {})
                        st.subheader("🤖 ATS Compatibility Check")
                        status = ats.get('status', 'Warning')
                        
                        if status == "Pass":
                            st.success("✅ Your resume format is ATS friendly!")
                        elif status == "Fail":
                            st.error("❌ Your resume formatting might cause critical issues.")
                        else:
                            st.warning("⚠️ Potential formatting issues detected.")
                            
                        if ats.get('issues'):
                            for issue in ats['issues']:
                                st.write(f"- {issue}")

                    else:
                        st.error("Failed to parse the AI analysis. Please try again.")

                except Exception as e:
                     st.error(f"Groq API Error: {str(e)}")
            else:
                st.error("Failed to read the PDF file. Please ensure it is a valid text-based PDF.")

# Footer & About
st.markdown("---")
with st.expander("ℹ️ About this Tool"):
    st.markdown("""
    This tool uses **Groq AI (Llama 3)** to compare your resume against a job description.
    
    **Privacy Note**: Your data is sent to Groq for analysis but is not stored by this application.
    """)
st.markdown("Made with ❤️ for Job Seekers")
