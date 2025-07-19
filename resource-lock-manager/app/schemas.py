from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LockRequest(BaseModel):
    resource_name: str
    process_id: str
    ttl_seconds: Optional[int] = None

class LockResponse(BaseModel):
    id: int
    resource_name: str
    process_id: str
    locked_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

class LockStatus(BaseModel):
    resource_name: str
    is_locked: bool
    locked_by: Optional[str] = None
    locked_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
