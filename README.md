# ATS Resume Optimizer (Groq Edition) - User Guide

## Overview
This application helps you optimize your resume for Applicant Tracking Systems (ATS) by comparing it against a Job Description (JD) using the ultra-fast **Groq** AI inference engine (Llama 3).

## Setup & Running

1.  **Open Terminal**: Navigate to the project directory:
    ```bash
    cd ATS_Resume_Optimizer
    ```
2.  **Install Dependencies** (if you haven't already):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## API Key Setup
1.  Get a free API Key from [console.groq.com/keys](https://console.groq.com/keys).
2.  Open the `.env` file in the project folder.
3.  Paste your key: `GROQ_API_KEY="gsk_..."`
4.  Restart the app.

## Usage Flow
1.  **Upload Resume**: Click "Browse files" to upload your PDF resume.
2.  **Job Description**: Paste the full job description text.
3.  **Analyze**: Click the "Analyze Resume" button.
    > [!TIP]
    > Groq is incredibly fast, so results should appear almost instantly!

## Results
- **Match Score**: See how well you fit the role.
- **Keyword Gap**: Identify missing technical keywords.
- **Critical Skills**: See if you are missing any required certifications or hard skills.
- **Section Advice**: Get specific tips for your Summary, Projects, and Experience.
- **ATS Check**: Ensure your PDF formatting is machine-readable.
