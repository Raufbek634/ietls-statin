# IELTS Pro

IELTS tayyorgarlik platformasi — Reading, Listening, Writing, Speaking, Vocabulary, Mock Exam.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL (production) / SQLite (local)
- **Deploy:** Vercel

## Local Development

```bash
pip install -r requirements.txt
python seed.py
python run.py
```

## Deploy to Vercel

1. Push to GitHub
2. Import repo in Vercel
3. Set `DATABASE_URL` environment variable (PostgreSQL)
4. Deploy
