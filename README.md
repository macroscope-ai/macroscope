# MACROSCOPE

MACROSCOPE is an AI-powered tool that uses GPT-4 and real-time news data to classify and summarize global geopolitical and financial risks.

## Setup

1. Create a `.env` file in the root with your API keys:
```
OPENAI_API_KEY=your_openai_key
NEWSAPI_KEY=your_newsapi_key
```

2. Install requirements:
```
pip install -r requirements.txt
```

3. Run the app:
```
streamlit run macroscope_with_newsapi.py
```
