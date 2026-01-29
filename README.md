# ResuMate

**Your AI-powered partner for landing the perfect job.**

ResuMate helps you optimize your resume for Applicant Tracking Systems (ATS) by comparing it against a Job Description (JD) using advanced AI.

## Features
- **Match Percentage**: See exactly how well your resume fits the role.
- **Keyword Gap Analysis**: Find out which technical skills you are missing.
- **Section-by-Section Review**: Get actionable feedback for improvements.
- **ATS Compatibility Check**: Ensure your resume is machine-readable.

## Setup & Running

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/Cypher-redeye/ResuMate.git
    cd ResuMate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Configuration
This app requires an API Key.
1.  Obtain your API Key from your provider (Groq).
2.  Set it in the `.env` file: `GROQ_API_KEY="your_key_here"`.
