# Weather-Based Post Delay Prediction and SMS Notification System

This project delivers a full-stack system for India Post to predict weather-based delivery delays and send SMS notifications **only after admin approval**.

## Tech Stack
- **Frontend:** React (Vite)
- **Backend:** FastAPI (Python)
- **Machine Learning:** Random Forest (custom lightweight ensemble + optional scikit-learn)
- **Database:** MySQL
- **Notification:** SMS (provider integration stubbed)

## Project Structure
```
backend/
  app/                # FastAPI app, services, models, schemas
  data/               # Training data and model artifact
  db/                 # MySQL schema
  scripts/            # ML training script
frontend/
  src/                # React UI
```

## Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the API
```bash
uvicorn app.main:app --reload
```

### Train the Random Forest Model
```bash
PYTHONPATH=backend python backend/scripts/train_model.py --data backend/data/sample_delivery_history.csv
```

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## MySQL Schema
The schema is provided at `backend/db/schema.sql` for provisioning the database tables.

## Key Workflow
1. Postal staff books posts and tracks status.
2. Weather snapshots are fetched for post office locations.
3. The ML model predicts delay risk and duration.
4. Admin reviews predictions and approves or rejects notifications.
5. SMS notifications are sent to registered sender and receiver numbers only after approval.

## SMS Message Format
```
Due to adverse weather conditions, your post delivery is delayed by X days.
```
