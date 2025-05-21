
import streamlit as st
import openai
import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")

st.set_page_config(page_title="MACROSCOPE – Real-Time Risk Intelligence", layout="wide")
st.title("🌍 MACROSCOPE")
st.markdown("**AI-powered geopolitical and financial risk signals — updated with real-time headlines.**")

# Fetch headlines from NewsAPI
def get_headlines():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&pageSize=10&apiKey={newsapi_key}"
    )
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles if article.get("title")]
    except Exception as e:
        st.error(f"Error fetching headlines: {e}")
        return []

headlines = get_headlines()
if headlines:
    st.subheader("Latest News Headlines")
    for hl in headlines:
        st.markdown(f"• {hl}")

    if st.button("Analyze Headlines"):
        output_data = []
        for hl in headlines:
            with st.spinner(f"Analyzing: {hl[:50]}..."):
                prompt = f'''
                You are a geopolitical and macroeconomic risk analyst using AI to classify news events.

                Given the following headline:
                "{hl}"

                Classify and summarize it:

                - Region: (e.g., MENA, East Asia, Europe)
                - Topic: (e.g., conflict, energy, trade)
                - Financial Relevance Score (0–10): 
                - Summary: (2–3 sentence professional summary)
                - Investor Impact: (short note on market implications)
                '''

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a geopolitical finance analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.4
                    )
                    result = response.choices[0].message.content
                    output_data.append({"headline": hl, "analysis": result})
                    time.sleep(1.5)
                except Exception as e:
                    output_data.append({"headline": hl, "analysis": f"Error: {str(e)}"})

        st.subheader("🔎 Analysis Results")
        for item in output_data:
            st.markdown(f"**Headline:** {item['headline']}")
            st.markdown(f"```\n{item['analysis']}```")
            st.markdown("---")
else:
    st.warning("No headlines available or NewsAPI quota exhausted.")
