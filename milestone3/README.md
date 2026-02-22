
---

# 🚀 Hackathon – Smart Support Ticket Routing Engine

## 📌 Milestone 3

An AI-powered **real-time support ticket routing system** that classifies, deduplicates, prioritizes, and routes incidents using ML models, Redis queues, orchestration logic, and a live monitoring dashboard.

---

# 🧠 What This Milestone Implements

Milestone 3 introduces:

* ✅ ML-based ticket classification (Lightweight + Transformer model support)
* ✅ Intelligent routing engine
* ✅ Deduplication logic
* ✅ Circuit breaker mechanism
* ✅ Redis-backed queue system
* ✅ Worker-based orchestration
* ✅ Real-time dashboard (React)
* ✅ Incident simulation for stress testing
* ✅ Webhook support

---

# 🏗️ Architecture Overview

```
Incoming Ticket
       ↓
Webhook / API (FastAPI)
       ↓
Incident Manager
       ↓
ML Classification (Embeddings + Model)
       ↓
Deduplication
       ↓
Router
       ↓
Redis Queue
       ↓
Worker (Orchestrator)
       ↓
Storage + Dashboard
```

---

# 📂 Project Structure

```
HACKATHON-SMART-SUPPORT-TICKET-ROUTING-ENGINE
│
├── backend/
│   ├── ml/
│   │   ├── embeddings.py
│   │   ├── lightweight_model.py
│   │   ├── transformer_model.py
│   │   └── circuit_breaker.py
│   │
│   ├── orchestration/
│   │   ├── agent_registry.py
│   │   ├── deduplication.py
│   │   ├── incident_manager.py
│   │   └── router.py
│   │
│   ├── storage/
│   │   └── redis_storage.py
│   │
│   ├── ticket_queue/
│   │   ├── broker.py
│   │   └── redis_client.py
│   │
│   ├── worker/
│   │   └── orchestrator_worker.py
│   │
│   ├── utils/
│   │   ├── locks.py
│   │   └── time_utils.py
│   │
│   ├── app.py
│   ├── config.py
│   ├── webhook.py
│   ├── simulate_tickets_batched.py
│   ├── requirements.txt
│   └── Procfile
│
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── pages/
    │   └── utils/
```

---

# ⚙️ Backend Setup

## 1️⃣ Navigate to backend

```bash
cd backend
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Start Redis (Required)

Make sure Redis server is running:

```bash
redis-server
```

---

## 5️⃣ Run FastAPI Server

```bash
uvicorn app:app --reload
```

Runs on:

```
http://127.0.0.1:8000
```

---

## 6️⃣ Start Worker (Important)

In a new terminal:

```bash
python worker/orchestrator_worker.py
```

The worker consumes tickets from Redis and processes routing logic.

---

# 💻 Frontend Setup

## 1️⃣ Navigate to frontend

```bash
cd frontend
```

## 2️⃣ Install dependencies

```bash
npm install
```

## 3️⃣ Run frontend

```bash
npm run dev
```

Runs on:

```
http://localhost:5173
```

---

# 🔌 Key API Endpoints

### 📥 Submit Ticket

```
POST /webhook
```

### 📋 Get Incidents

```
GET /incidents
```

### 🧪 Simulate Batch Tickets

```
python simulate_tickets_batched.py
```

---

# 🧠 ML Layer

Milestone 3 supports:

### 🔹 Embedding-based similarity

* `embeddings.py`

### 🔹 Lightweight Model

* Fast classification for real-time routing

### 🔹 Transformer Model

* Higher accuracy classification

### 🔹 Circuit Breaker

* Prevents model overload
* Automatically falls back to lightweight model

---

# 🔄 Orchestration Layer

### 🔹 Incident Manager

Central control for ticket processing

### 🔹 Deduplication Engine

Prevents duplicate ticket routing

### 🔹 Router

Assigns correct agent/team

### 🔹 Agent Registry

Tracks available agents and load

---

# 📦 Queue & Storage

* Redis queue for async processing
* Redis storage for state persistence
* Worker-based architecture
* Locking utilities for concurrency control

---

# 📊 Frontend Dashboard Features

* 📋 Live ticket table
* 🔥 Flash flood monitoring panel
* ⚡ Circuit breaker status
* 👥 Agent load board
* 📊 Incident panel
* 📅 Time formatting utilities

---

# 🧪 Load Testing

Run batch simulation:

```bash
python simulate_tickets_batched.py
```

Used to test:

* Queue behavior
* Circuit breaker activation
* Routing stability
* Worker scaling behavior

---

# 🎯 Milestone 3 Deliverables Achieved

* ✔ Asynchronous queue processing
* ✔ ML-based routing
* ✔ Deduplication engine
* ✔ Circuit breaker pattern
* ✔ Worker-based orchestration
* ✔ Real-time dashboard monitoring
* ✔ Redis-backed distributed system

---
