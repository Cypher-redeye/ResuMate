# Deployment Guide: ResuMate

This guide will show you how to deploy your app for free using **Streamlit Community Cloud**.

## Prerequisites
1.  **GitHub Account**.
2.  **API Key**: You will need your provider's API Key.

## Step 1: Push Code to GitHub
(Already done if you are reading this on GitHub!)

## Step 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository (`Cypher-redeye/ResuMate`), branch (`main`), and file path (`app.py`).
4.  Click **"Deploy!"**.

## Step 3: Configure API Key (Critical!)
Your app will fail initially because the API Key is missing in the cloud.
1.  On your deployed app dashboard, click **"Manage app"** -> **Settings**.
2.  Go to the **Secrets** tab.
3.  Paste the following (updating with your actual key):
    ```toml
    GROQ_API_KEY = "your_actual_api_key_here"
    ```
4.  Click **Save**.

## Step 4: Restart
The app should automatically detect the new secret and restart. You are now live! 🚀
