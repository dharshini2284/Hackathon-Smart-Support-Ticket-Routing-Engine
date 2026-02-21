# 🚀 Smart Support — Milestone 1  
## Minimum Viable Router (MVR)

---

## 📌 Overview

Milestone 1 establishes the foundational architecture for the Smart Support system.

This version implements a **synchronous, end-to-end ticket routing pipeline** with:

- ML-based ticket classification  
- Regex-based urgency detection  
- In-memory priority queue  
- REST API using FastAPI  
- Deterministic FIFO prioritization  

This milestone validates the core routing logic before introducing asynchronous processing and distributed architecture in later stages.

---

# 🏗 System Architecture

Client (Frontend or API Client)  
↓  
FastAPI Backend  
↓  
ML Classification (TF-IDF + Logistic Regression)  
↓  
Urgency Detection (Regex-based)  
↓  
In-Memory Priority Queue (heapq)  

---

# 🧠 Machine Learning Components

## 1️⃣ Baseline Ticket Classification

**Model Used:**
- TF-IDF Vectorization  
- Logistic Regression  

**Approach:**
- Lightweight supervised learning  
- Fast inference  
- Suitable for low-latency routing  

**Supported Categories:**

- Billing  
- Technical  
- Legal  

The model is trained using a small labeled dataset (`sample_train_data.csv`) and loaded at server startup.

---

## 2️⃣ Urgency Detection (Rule-Based)

Urgency is determined using regex pattern matching.

**Keywords Detected:**

- ASAP  
- urgent  
- immediately  
- broken  
- critical  

If detected:

```
priority = 0  (High Priority)
```

Otherwise:

```
priority = 1  (Normal Priority)
```

---

# 📦 Queue Management

Milestone 1 uses Python’s built-in `heapq` module.

Queue structure:

```python
(priority, timestamp, ticket)
```

**Routing Logic:**

1. Urgent tickets are processed first  
2. Within the same priority → FIFO order maintained  
3. Category does NOT affect queue order  

This ensures deterministic and predictable behavior.

---

# 🌐 API Endpoints

## 1️⃣ Submit Ticket

**POST /tickets**

Request:

```json
{
  "text": "API is broken ASAP"
}
```

Response:

```json
{
  "ticket_id": "uuid",
  "category": "Technical",
  "urgent": true,
  "status": "queued"
}
```

---

## 2️⃣ View Queue Size

**GET /queue**

Response:

```json
{
  "queue_size": 3
}
```

---

## 3️⃣ View All Tickets (Non-destructive)

**GET /tickets**

Returns the current queue state sorted by priority.

---

## 4️⃣ Pop Next Ticket

**GET /next-ticket**

Returns and removes the highest-priority ticket.

---

# 🎨 Frontend (Milestone 1 Dashboard)

Milestone 1 includes a lightweight dashboard with:

- Ticket submission interface  
- Live queue size metric  
- Current queue table  
- Urgency highlighting  

**Architecture:**

HTML + CSS + Vanilla JS  
↓  
Fetch API  
↓  
FastAPI Backend  

No Node.js or build tools required.

---

# ⚙️ Setup Instructions

## Backend

```bash
cd milestone1/backend
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Frontend

Open directly in browser:

```
milestone1/frontend/index.html
```

Ensure backend is running before using frontend.

---

# ⚠️ Limitations (Intentional for MVR)

- No persistence (data lost on restart)  
- No asynchronous processing  
- No distributed queue  
- No concurrency handling  
- No semantic deduplication  
- No webhook integration  

These enhancements are introduced in:

- Milestone 2 — Intelligent Queue  
- Milestone 3 — Autonomous Orchestrator  

---

# 🎯 Purpose of Milestone 1

Milestone 1 validates:

- End-to-end classification pipeline  
- Priority-based routing  
- API contract  
- Queue logic correctness  

It serves as the **baseline fallback model** for advanced stages.

---

# 📌 Next Evolution

Milestone 2 upgrades this system into:

- Asynchronous architecture  
- Redis message broker  
- Transformer-based classification  
- Continuous urgency scoring  
- Webhook triggering  
- Real-time monitoring dashboard  

---

# ✅ Status

✔ Functional end-to-end pipeline  
✔ Deterministic routing  
✔ Lightweight ML  
✔ Frontend dashboard  
✔ Production-ready foundation  