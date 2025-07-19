# Resource Lock Manager

A REST API for managing exclusive locks on named resources with TTL (Time-To-Live) support. Built with FastAPI and SQLAlchemy.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

**Clone the repository:**
```bash
git clone https://github.com/dhanushgp6/think41
cd resource-lock-manager
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Alternative:**
```bash
python app/main.py
```

### Access Points
- **🌐 Interactive API Documentation**: http://localhost:8000/docs
- **📊 Health Check**: http://localhost:8000/health
- **📋 Alternative Docs**: http://localhost:8000/redoc

## 📖 API Endpoints

### 🔒 Acquire Lock
**Endpoint:** `POST /locks/request`

**Request Body:**
```json
{
  "resource_name": "database_backup",
  "process_id": "process_123",
  "ttl_seconds": 300
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Lock acquired successfully for resource 'database_backup'",
  "data": {
    "lock_id": 1,
    "resource_name": "database_backup",
    "process_id": "process_123",
    "locked_at": "2024-01-15T10:30:00.123456+00:00",
    "expires_at": "2024-01-15T10:35:00.123456+00:00"
  }
}
```

**Conflict Response (409):**
```json
{
  "detail": "Resource 'database_backup' is already locked by process 'other_process'"
}
```

### 🔓 Release Lock
**Endpoint:** `DELETE /locks/release`

**Query Parameters:**
- `resource_name`: Name of the resource to release
- `process_id`: ID of the process that owns the lock

**Success Response (200):**
```json
{
  "success": true,
  "message": "Lock released successfully for resource 'database_backup'",
  "data": {
    "resource_name": "database_backup",
    "process_id": "process_123",
    "released_at": "2024-01-15T10:35:00.123456+00:00"
  }
}
```

### 📊 Check Lock Status
**Endpoint:** `GET /locks/status`

**Query Parameters:**
- `resource_name`: Name of the resource to check

**Response (Locked):**
```json
{
  "success": true,
  "message": "Resource 'database_backup' status retrieved successfully",
  "data": {
    "resource_name": "database_backup",
    "is_locked": true,
    "locked_by": "process_123",
    "locked_at": "2024-01-15T10:30:00.123456+00:00",
    "expires_at": "2024-01-15T10:35:00.123456+00:00"
  }
}
```

**Response (Not Locked):**
```json
{
  "success": true,
  "message": "Resource 'database_backup' is not locked",
  "data": {
    "resource_name": "database_backup",
    "is_locked": false,
    "locked_by": null,
    "locked_at": null,
    "expires_at": null
  }
}
```

### 📋 List All Locked Resources
**Endpoint:** `GET /locks/all-locked`

**Response:**
```json
{
  "success": true,
  "message": "Retrieved 2 active locks",
  "data": {
    "total_locks": 2,
    "locks": [
      {
        "id": 1,
        "resource_name": "database_backup",
        "process_id": "process_123",
        "locked_at": "2024-01-15T10:30:00.123456+00:00",
        "expires_at": "2024-01-15T10:35:00.123456+00:00"
      },
      {
        "id": 2,
        "resource_name": "file_upload",
        "process_id": "process_456",
        "locked_at": "2024-01-15T10:32:00.123456+00:00",
        "expires_at": null
      }
    ]
  }
}
```

## 🧪 Testing the API

### Method 1: Interactive Documentation (Recommended)
1. Start the server: `python -m uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Click on any endpoint to expand it
4. Click "Try it out" button
5. Fill in the parameters
6. Click "Execute" to test

### Method 2: Python Script
Create a test file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_lock_manager():
    print("🧪 Testing Resource Lock Manager\n")
    
    # 1. Health Check
    print("1. Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # 2. Acquire Lock
    print("2. Acquiring lock...")
    data = {
        "resource_name": "test_resource",
        "process_id": "test_process_123",
        "ttl_seconds": 60
    }
    response = requests.post(f"{BASE_URL}/locks/request", json=data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 3. Check Status
    print("3. Checking lock status...")
    response = requests.get(f"{BASE_URL}/locks/status?resource_name=test_resource")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 4. Try to acquire same lock (should fail)
    print("4. Trying to acquire same lock (should fail)...")
    data2 = {
        "resource_name": "test_resource",
        "process_id": "different_process"
    }
    response = requests.post(f"{BASE_URL}/locks/request", json=data2)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 5. View all locks
    print("5. Viewing all locks...")
    response = requests.get(f"{BASE_URL}/locks/all-locked")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 6. Release lock
    print("6. Releasing lock...")
    response = requests.delete(f"{BASE_URL}/locks/release?resource_name=test_resource&process_id=test_process_123")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    # Install requests if not already installed
    # pip install requests
    test_lock_manager()
```

Run the test:
```bash
pip install requests
python test_api.py
```

### Method 3: Command Line Testing

#### For Windows (PowerShell):
```powershell
# Acquire lock
$body = @{
    resource_name = "test_resource"
    process_id = "proc123"
    ttl_seconds = 300
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/locks/request" -Method Post -Body $body -ContentType "application/json"

# Check status
Invoke-RestMethod -Uri "http://localhost:8000/locks/status?resource_name=test_resource" -Method Get

# Release lock
Invoke-RestMethod -Uri "http://localhost:8000/locks/release?resource_name=test_resource&process_id=proc123" -Method Delete
```

#### For Mac/Linux (curl):
```bash
# Acquire lock
curl -X POST "http://localhost:8000/locks/request" \
  -H "Content-Type: application/json" \
  -d '{
    "resource_name": "test_resource",
    "process_id": "proc123",
    "ttl_seconds": 300
  }'

# Check status
curl "http://localhost:8000/locks/status?resource_name=test_resource"

# Release lock
curl -X DELETE "http://localhost:8000/locks/release?resource_name=test_resource&process_id=proc123"
```

## 📁 Project Structure

```
resource-lock-manager/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application and endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── database.py          # Database configuration
│   └── schemas.py           # Pydantic request/response models
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── README.md               # This file
└── resource_locks.db       # SQLite database (auto-created)
```

## ⚙️ Key Features

- **🔐 Exclusive Locking**: Only one process can lock a resource at a time
- **⏰ TTL Support**: Locks can automatically expire after specified seconds
- **🧹 Auto Cleanup**: Expired locks are automatically removed
- **🗄️ Persistent Storage**: Uses SQLite database (easily switchable to PostgreSQL)
- **📚 Interactive Docs**: Built-in Swagger UI for easy testing
- **🛡️ Error Handling**: Comprehensive error responses with proper HTTP status codes
- **🔄 Concurrent Safe**: Handles multiple simultaneous requests safely

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./resource_locks.db
```

For PostgreSQL:
```env
DATABASE_URL=postgresql://username:password@localhost/resource_locks
```

### Database Schema
The application uses a single table `resource_locks` with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| resource_name | String | Unique resource identifier |
| process_id | String | Process that owns the lock |
| locked_at | DateTime | When the lock was acquired |
| expires_at | DateTime | When the lock expires (nullable) |
| is_active | Boolean | Whether the lock is currently active |

## 🚨 Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Lock not found |
| 409 | Resource already locked |
| 422 | Invalid request data |
| 500 | Internal server error |

## 🧪 Example Test Scenarios

### Scenario 1: Basic Lock/Release
1. Acquire lock on "database_backup"
2. Verify lock status shows locked
3. Try to acquire same resource with different process (should fail)
4. Release lock
5. Verify lock status shows unlocked

### Scenario 2: TTL Expiration
1. Acquire lock with 5-second TTL
2. Wait 6 seconds
3. Try to acquire same resource (should succeed as lock expired)

### Scenario 3: Multiple Resources
1. Acquire locks on multiple resources
2. List all locked resources
3. Release specific locks
4. Verify remaining locks

## 🔍 Health Check

The API includes a health check endpoint:

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "service": "Resource Lock Manager"
}
```

## 📝 Development Notes

- The application automatically creates the database tables on startup
- SQLite is used by default for development (no setup required)
- All timestamps are stored in UTC
- The API follows REST conventions
- Comprehensive logging is included for debugging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 🚀 Quick Verification

After starting the server, verify everything works:

1. **Health Check**: Visit http://localhost:8000/health
2. **API Docs**: Visit http://localhost:8000/docs
3. **Run Test**: Execute `python test_api.py` (after creating the test file above)

**✅ Ready for production use!**
