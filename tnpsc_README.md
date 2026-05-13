# 🎯 TNPSC Coach — Premium Exam Preparation SaaS

A full-stack TNPSC exam preparation webapp built with Streamlit.

## Features

- 🔐 **Auth System** — Login, Signup, Onboarding
- 🏠 **Dashboard** — Streak, XP, Today's Goals, Weak Subjects, Mock Score Graph
- 📚 **PYQ Practice Hub** — 5,000+ questions, filters, 5 practice modes, instant explanations
- 📝 **Mock Tests** — Full-length & mini mocks with timer, question navigator, score analysis
- 📅 **Study Planner** — Personalised weekly plan with daily task tracking
- 🔁 **Revision System** — Spaced repetition (1/3/7/15/30 day intervals)
- 📊 **Analytics** — Accuracy trends, subject breakdown, speed analysis
- 🏆 **Achievements** — XP, Levels, Badges, Daily Challenges, Leaderboard
- 📰 **Current Affairs** — Daily news, MCQ practice, weekly PDF capsule

## Deploy on Streamlit Cloud (free)

### 1. Push to GitHub
```bash
cd tnpsc-coach
git init && git add . && git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/tnpsc-coach.git
git push -u origin main
```

### 2. Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub → New app
3. Repo: `your-username/tnpsc-coach` · Branch: `main` · File: `app.py`
4. Deploy → live in ~60 seconds

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Connecting Supabase (Phase 2)
1. Create a project at [supabase.com](https://supabase.com)
2. Add `SUPABASE_URL` and `SUPABASE_KEY` to Streamlit Secrets
3. Replace demo data arrays with real DB queries

© 2025 TNPSC Coach · Unauthorized redistribution prohibited
