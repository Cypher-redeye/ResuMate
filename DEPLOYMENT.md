# Deployment Guide: ATS Resume Optimizer

This guide will show you how to deploy your app for free using **Streamlit Community Cloud**.

## Prerequisites
1.  **GitHub Account**: You need a GitHub account.
2.  **Groq API Key**: Have your key ready from [console.groq.com](https://console.groq.com/keys).

## Step 1: Push Code to GitHub
1.  Initialize Git in your project folder (if not done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a **new repository** on GitHub.
3.  Push your code:
    ```bash
    git remote add origin <your-repo-url>
    git push -u origin main
    ```

## Step 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository, branch (`main`), and file path (`app.py`).
4.  Click **"Deploy!"**.

## Step 3: Configure API Key (Critical!)
Your app will fail initially because the API Key is missing in the cloud.
1.  On your deployed app dashboard, click only **"Manage app"** (bottom right) -> three dots **⋮** -> **Settings**.
2.  Go to the **Secrets** tab.
3.  Paste the following:
    ```toml
    GROQ_API_KEY = "gsk_your_actual_api_key_here"
    ```
4.  Click **Save**.

## Step 4: Restart
The app should automatically detect the new secret and restart. You are now live! 🚀
