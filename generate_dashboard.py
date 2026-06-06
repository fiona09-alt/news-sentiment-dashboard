"""
News Sentiment Dashboard — Auto-generator
Runs daily via GitHub Actions, publishes to GitHub Pages
"""

import requests
import pandas as pd
import numpy as np
import json
import os
import re
from datetime import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────
API_KEY    = os.environ.get('NEWS_API_KEY', '')
CATEGORIES = ['technology', 'business', 'science', 'health', 'sports']

SAMPLE_HEADLINES = [
    {'category':'technology','title':'AI Breakthrough Promises Faster Drug Discovery','description':'Scientists use machine learning to cut drug development time.','source':'TechCrunch','url':'#','published_at':'2024-01-15'},
    {'category':'technology','title':'New Quantum Computer Shatters Speed Records','description':'IBM unveils a 1000-qubit processor in a historic leap.','source':'Wired','url':'#','published_at':'2024-01-15'},
    {'category':'technology','title':'Social Media Giant Faces Massive Data Breach','description':'Over 500 million user records exposed in cybersecurity incident.','source':'BBC','url':'#','published_at':'2024-01-15'},
    {'category':'technology','title':'Electric Vehicle Sales Hit Record High Globally','description':'EV adoption accelerates as battery costs continue to fall.','source':'Reuters','url':'#','published_at':'2024-01-15'},
    {'category':'technology','title':'Tech Layoffs Continue as Companies Restructure','description':'Major technology firms announce thousands of job cuts.','source':'Bloomberg','url':'#','published_at':'2024-01-15'},
    {'category':'business','title':'Stock Markets Surge on Positive Economic Data','description':'Dow Jones hits new all-time high amid strong employment figures.','source':'CNBC','url':'#','published_at':'2024-01-15'},
    {'category':'business','title':'Inflation Rate Falls to Two Year Low','description':'Consumer prices ease as central bank policies take effect.','source':'FT','url':'#','published_at':'2024-01-15'},
    {'category':'business','title':'Major Bank Collapses Sparking Financial Fears','description':'Regulators intervene as regional bank failures trigger panic.','source':'WSJ','url':'#','published_at':'2024-01-15'},
    {'category':'business','title':'Startup Raises Record Breaking Funding Round','description':'Silicon Valley unicorn secures 2 billion in Series D.','source':'Forbes','url':'#','published_at':'2024-01-15'},
    {'category':'business','title':'Supply Chain Disruptions Hit Global Manufacturing','description':'Factory output drops sharply as shipping delays worsen.','source':'Reuters','url':'#','published_at':'2024-01-15'},
    {'category':'science','title':'Scientists Discover New Species in Amazon Rainforest','description':'Researchers identify dozens of previously unknown species.','source':'Nature','url':'#','published_at':'2024-01-15'},
    {'category':'science','title':'Mars Mission Returns Stunning New Images','description':'NASA rover captures breathtaking photographs of Martian riverbeds.','source':'Space.com','url':'#','published_at':'2024-01-15'},
    {'category':'science','title':'Climate Change Accelerating Faster Than Predicted','description':'New study shows ice caps melting at twice the predicted rate.','source':'Guardian','url':'#','published_at':'2024-01-15'},
    {'category':'health','title':'New Cancer Vaccine Shows Remarkable Early Results','description':'mRNA technology targets tumours with unprecedented precision.','source':'Lancet','url':'#','published_at':'2024-01-15'},
    {'category':'health','title':'Mental Health Crisis Deepens Among Young Adults','description':'Depression and anxiety rates reach historic levels globally.','source':'WHO','url':'#','published_at':'2024-01-15'},
    {'category':'health','title':'Breakthrough Drug Reverses Alzheimer Symptoms','description':'Clinical trial results show significant cognitive improvement.','source':'NEJM','url':'#','published_at':'2024-01-15'},
    {'category':'sports','title':'Underdog Team Wins Championship in Stunning Upset','description':'Nobody predicted this incredible victory in the final match.','source':'ESPN','url':'#','published_at':'2024-01-15'},
    {'category':'sports','title':'Star Player Suffers Serious Injury Ending Season','description':'Team faces major setback after losing their best performer.','source':'SportsBBC','url':'#','published_at':'2024-01-15'},
    {'category':'sports','title':'Olympics 2024 Sets New Viewership World Record','description':'Billions tune in to watch historic athletic performances.','source':'AP','url':'#','published_at':'2024-01-15'},
    {'category':'sports','title':'Doping Scandal Rocks International Athletics','description':'Multiple gold medal winners stripped of titles after tests.','source':'Reuters','url':'#','published_at':'2024-01-15'},
]


def fetch_headlines(category, api_key, max_articles=20):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {'category': category, 'language': 'en',
              'pageSize': max_articles, 'apiKey': api_key}
    try:
        r = requests.get(url, params=params, timeout=10)
        articles = r.json().get('articles', [])
        rows = []
        for a in articles:
            title = a.get('title', '') or ''
            desc  = a.get('description', '') or ''
            if title and '[Removed]' not in title:
                rows.append({
                    'category': category,
                    'title': title,
                    'description': desc,
                    'source': a.get('source', {}).get('name', 'Unknown'),
                    'url': a.get('url', '#'),
                    'published_at': a.get('publishedAt', '')[:10],
                })
        return rows
    except Exception as e:
        print(f'Error fetching {category}: {e}')
        return []


def analyze_sentiment(text):
    blob   = TextBlob(str(text))
    vader  = analyzer.polarity_scores(str(text))
    compound = round(vader['compound'], 4)
    label = ('Positive' if compound >= 0.05
             else 'Negative' if compound <= -0.05
             else 'Neutral')
    return {
        'tb_polarity':    round(blob.sentiment.polarity, 4),
        'tb_subjectivity': round(blob.sentiment.subjectivity, 4),
        'vader_compound': compound,
        'vader_pos': round(vader['pos'], 4),
        'vader_neg': round(vader['neg'], 4),
        'vader_neu': round(vader['neu'], 4),
        'sentiment': label,
    }


def run():
    # 1. Fetch
    all_articles = []
    if API_KEY:
        print('Fetching live headlines...')
        for cat in CATEGORIES:
            arts = fetch_headlines(cat, API_KEY)
            all_articles.extend(arts)
            print(f'  {cat}: {len(arts)} articles')
    else:
        print('No API key — using sample headlines')
        all_articles = SAMPLE_HEADLINES

    df = pd.DataFrame(all_articles)
    df['text'] = df['title'] + ' ' + df.get('description', '')

    # 2. Sentiment
    print('Running sentiment analysis...')
    sentiment_data = df['text'].apply(lambda t: pd.Series(analyze_sentiment(t)))
    df = pd.concat([df, sentiment_data], axis=1)

    # 3. Build JSON for dashboard
    records = df.to_dict(orient='records')
    stats = {
        'total': len(df),
        'positive': int((df['sentiment'] == 'Positive').sum()),
        'negative': int((df['sentiment'] == 'Negative').sum()),
        'neutral':  int((df['sentiment'] == 'Neutral').sum()),
        'avg_score': round(float(df['vader_compound'].mean()), 3),
        'generated_at': datetime.now().strftime('%A, %d %B %Y at %H:%M UTC'),
        'categories': {}
    }
    for cat in CATEGORIES:
        sub = df[df['category'] == cat]
        if len(sub) == 0:
            continue
        stats['categories'][cat] = {
            'total': len(sub),
            'positive': int((sub['sentiment'] == 'Positive').sum()),
            'negative': int((sub['sentiment'] == 'Negative').sum()),
            'neutral':  int((sub['sentiment'] == 'Neutral').sum()),
            'avg_score': round(float(sub['vader_compound'].mean()), 3),
        }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w') as f:
        json.dump({'stats': stats, 'articles': records}, f, indent=2)
    print(f'Saved docs/data.json — {len(df)} articles')
    return df, stats


if __name__ == '__main__':
    run()
