# ArthCafe Backend

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your DATABASE_URL and other credentials

# 4. Run schema on your PostgreSQL
psql $DATABASE_URL < schema.sql

# 5. Seed sample data
python -m seed

# 6. Start server
uvicorn app.main:app --reload --port 8000
```

API Docs: http://localhost:8000/docs

## Deployment (Render)

1. Push to GitHub
2. Connect repo on Render
3. Set environment variables
4. Deploy!
