#  Smart Support — Milestone 2  The Intelligent Queue
## Intelligent Asynchronous Ticket Routing Engine

---

## Overview

Milestone 2 upgrades the Smart Support system into a **production-style asynchronous ML pipeline**.

This version introduces:

- Transformer-based ticket classification  
- Continuous urgency scoring (S ∈ [0,1])  
- Redis-based asynchronous message broker  
- Background worker processing  
- Webhook triggering for high urgency tickets  
- Real-time React monitoring dashboard  
- Latency tracking per ticket  

The system now mimics a real-world scalable SaaS support routing architecture.

---

# 🏗 System Architecture
React Frontend
↓
FastAPI Backend (returns 202 immediately)
↓
Redis Queue (Message Broker)
↓
Background Worker
↓
Transformer Models (ML)
↓
Redis (Status Store)
↓
Frontend Polling Dashboard

---


---

# 🧠 Machine Learning Components

## 1️⃣ Transformer-Based Classification

Model:
- `facebook/bart-large-mnli`

Approach:
- Zero-shot classification
- No keyword rules
- Context-aware predictions

Supported categories:
- Billing
- Technical
- Legal

---

## 2️⃣ Continuous Urgency Scoring

Urgency score:
- [0,1] range
- Sentiment-weighted keywords
- Critical > High > Medium
- Keyword cascading

Scoring logic combines:

- Sentiment analysis
- Critical keywords (down, breach, outage, crash)
- Urgent indicators (ASAP, immediately)
- Moderate severity signals (error, slow, failed)

---

# Setup Instructions

## Backend

1. Install dependencies and start FastAPI server:
```bash
cd milestone2/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
uvicorn app:app --reload
```

2. Start Redis server in a separate terminal:
```bash
redis-server
```

3. Start background worker in a separate terminal:
```bash
cd milestone2/backend
source venv/bin/activate
python worker.py
```
## Frontend

1. Install dependencies and start React server:
```bash
cd milestone2/frontend
npm install
npm run dev
```



