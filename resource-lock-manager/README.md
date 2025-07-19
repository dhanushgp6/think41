# Resource Lock Manager

A REST API for managing exclusive locks on named resources with TTL support.

## 🚀 Quick Start

### Installation
```bash
git clone <https://github.com/dhanushgp6/think41>
cd resource-lock-manager
pip install -r requirements.txt
```

### Run
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Access
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 API Endpoints

### Acquire Lock
```bash
POST /locks/request
{
  "resource_name": "file1.txt",
  "process_id": "proc123",
  "ttl_seconds": 300
}
```

### Release Lock
```bash
DELETE /locks/release?resource_name=file1.txt&process_id=proc123
```

### Check Status
```bash
GET /locks/status?resource_name=file1.txt
```

### List All Locks
```bash
GET /locks/all-locked
```

## 🧪 Test Example
```bash
# Acquire lock
curl -X POST "http://localhost:8000/locks/request" \
  -H "Content-Type: application/json" \
  -d '{"resource_name": "test", "process_id": "proc1", "ttl_seconds": 60}'

# Check status
curl "http://localhost:8000/locks/status?resource_name=test"

# Release lock
curl -X DELETE "http://localhost:8000/locks/release?resource_name=test&process_id=proc1"
```

## 📁 Structure
```
app/
├── main.py      # API endpoints
├── models.py    # Database models
├── database.py  # DB config
└── schemas.py   # Request/response models
```

## ⚙️ Features
- Exclusive resource locking
- TTL expiration support
- Automatic cleanup of expired locks
- SQLite database (default)
- Interactive API documentation

---
**Ready to use! Visit http://localhost:8000/docs for interactive testing.**
