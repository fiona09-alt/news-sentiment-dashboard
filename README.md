# 📰 News Sentiment Dashboard v2

> **Project 2 of the ML + MLOps Automation Series**  
> Fully automated, interactive, live-updating news sentiment dashboard — powered by GitHub Actions + GitHub Pages

[![Live Dashboard](https://img.shields.io/badge/🌐_Live_Dashboard-Visit_Now-a78bfa?style=for-the-badge)](https://fiona09-alt.github.io/news-sentiment-dashboard)
[![Auto Update](https://img.shields.io/badge/Auto_Update-Daily_8AM_UTC-4ade80?style=for-the-badge&logo=github-actions)](https://github.com/fiona09-alt/news-sentiment-dashboard/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![NLP](https://img.shields.io/badge/NLP-TextBlob%20%7C%20VADER-purple)

---

## 🎯 What makes this special

This isn't just a notebook — it's a **production-grade automated pipeline:**

```
Every day at 8AM UTC (automatically):
GitHub Actions → Python script → NewsAPI
→ TextBlob + VADER sentiment analysis
→ JSON data file updated
→ Interactive dashboard deployed to GitHub Pages
→ Live at: fiona09-alt.github.io/news-sentiment-dashboard
```

**No manual work. No clicking. Fully automated.**

---

## ✨ Dashboard Features

- 🔍 **Search** headlines in real time
- 🎛️ **Filter** by category or sentiment (Positive / Neutral / Negative)
- 📊 **4 interactive charts** — donut, stacked bar, histogram, scatter
- 📋 **Paginated headlines table** with sentiment badges and score bars
- 🌙 **Dark mode** UI
- 📱 **Mobile responsive**
- ⚡ **Instant** — no page reloads, pure JavaScript

---

## 🚀 Setup (5 minutes)

### Step 1 — Fork this repo
Click **Fork** on GitHub

### Step 2 — Add your NewsAPI key (free)
- Get key at [newsapi.org/register](https://newsapi.org/register)
- Go to repo **Settings → Secrets → Actions → New secret**
- Name: `NEWS_API_KEY`, Value: your key

### Step 3 — Enable GitHub Pages
- Go to **Settings → Pages**
- Source: **Deploy from branch**
- Branch: `main`, Folder: `/docs`
- Click **Save**

### Step 4 — Trigger first run
- Go to **Actions → Daily News Sentiment Dashboard**
- Click **Run workflow**

Your live dashboard will be at:
`https://YOUR_USERNAME.github.io/news-sentiment-dashboard`

---

## 🗂️ Project Structure

```
news-sentiment-dashboard/
├── .github/workflows/
│   └── daily_update.yml      ← GitHub Actions (runs daily 8AM)
├── docs/
│   ├── index.html             ← Interactive dashboard (GitHub Pages)
│   └── data.json              ← Auto-updated sentiment data
├── generate_dashboard.py      ← Python pipeline script
├── requirements.txt
└── README.md
```

---

## 🛠️ Skills Demonstrated

- **Web scraping & APIs** — requests, NewsAPI
- **NLP / ML** — TextBlob, VADER sentiment analysis
- **MLOps automation** — GitHub Actions CI/CD pipeline
- **Frontend** — Interactive dashboard with Chart.js
- **DevOps** — GitHub Pages deployment, secrets management
- **Python** — Clean, modular, production-ready code

---

## 📚 ML + MLOps Automation Series

| # | Project | Skills | Status |
|---|---------|--------|--------|
| 1 | [Auto Data Report Generator](https://github.com/fiona09-alt/auto-data-report) | pandas, EDA, PDF | ✅ |
| 2 | **News Sentiment Dashboard** ← here | NLP, CI/CD, GitHub Pages | ✅ |
| 3 | ML Pipeline with Auto-Retraining | MLflow, Docker | 🔜 |
| 4 | Model Monitoring Bot | FastAPI, Evidently AI | 🔜 |
| 5 | End-to-End MLOps Pipeline | Prefect, Kubernetes | 🔜 |

---

*Auto-updated daily · Built with Python, TextBlob, VADER, Chart.js, GitHub Actions*
