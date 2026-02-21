# Smart Support - Hackathon

## Milestone 1 Completed

### Features
- FastAPI REST API
- ML-based ticket classification (Billing, Technical, Legal)
- Regex urgency detection
- In-memory priority queue using heapq

### Run Locally

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload