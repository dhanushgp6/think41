from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import datetime
import uuid

from app.database import engine, get_db, Base
from app.models import ResourceLock
from app.schemas import LockRequest, LockResponse, LockStatus, ApiResponse

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resource Lock Manager", version="1.0.0")

def cleanup_expired_locks(db: Session):
    """Remove expired locks from the database"""
    now = datetime.datetime.now(datetime.timezone.utc)
    expired_locks = db.query(ResourceLock).filter(
        ResourceLock.expires_at <= now,
        ResourceLock.is_active == True
    ).all()
    
    for lock in expired_locks:
        lock.is_active = False
    
    db.commit()
    return len(expired_locks)

@app.post("/locks/request", response_model=ApiResponse)
async def acquire_lock(lock_request: LockRequest, db: Session = Depends(get_db)):
    """Acquire an exclusive lock on a named resource"""
    try:
        # Clean up expired locks first
        cleanup_expired_locks(db)
        
        # Check if resource is already locked
        existing_lock = db.query(ResourceLock).filter(
            ResourceLock.resource_name == lock_request.resource_name,
            ResourceLock.is_active == True
        ).first()
        
        if existing_lock and not existing_lock.is_expired():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Resource '{lock_request.resource_name}' is already locked by process '{existing_lock.process_id}'"
            )
        
        # If lock exists but is expired, deactivate it
        if existing_lock and existing_lock.is_expired():
            existing_lock.is_active = False
            db.commit()
        
        # Calculate expiration time
        expires_at = None
        if lock_request.ttl_seconds:
            expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=lock_request.ttl_seconds)
        
        # Create new lock
        new_lock = ResourceLock(
            resource_name=lock_request.resource_name,
            process_id=lock_request.process_id,
            expires_at=expires_at,
            is_active=True
        )
        
        db.add(new_lock)
        db.commit()
        db.refresh(new_lock)
        
        return ApiResponse(
            success=True,
            message=f"Lock acquired successfully for resource '{lock_request.resource_name}'",
            data={
                "lock_id": new_lock.id,
                "resource_name": new_lock.resource_name,
                "process_id": new_lock.process_id,
                "locked_at": new_lock.locked_at.isoformat(),
                "expires_at": new_lock.expires_at.isoformat() if new_lock.expires_at else None
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to acquire lock: {str(e)}"
        )

@app.delete("/locks/release", response_model=ApiResponse)
async def release_lock(resource_name: str, process_id: str, db: Session = Depends(get_db)):
    """Release a lock on a named resource"""
    try:
        lock = db.query(ResourceLock).filter(
            ResourceLock.resource_name == resource_name,
            ResourceLock.process_id == process_id,
            ResourceLock.is_active == True
        ).first()
        
        if not lock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No active lock found for resource '{resource_name}' by process '{process_id}'"
            )
        
        lock.is_active = False
        db.commit()
        
        return ApiResponse(
            success=True,
            message=f"Lock released successfully for resource '{resource_name}'",
            data={
                "resource_name": resource_name,
                "process_id": process_id,
                "released_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to release lock: {str(e)}"
        )

@app.get("/locks/status", response_model=ApiResponse)
async def get_lock_status(resource_name: str, db: Session = Depends(get_db)):
    """Get the status of a specific resource lock"""
    try:
        # Clean up expired locks first
        cleanup_expired_locks(db)
        
        lock = db.query(ResourceLock).filter(
            ResourceLock.resource_name == resource_name,
            ResourceLock.is_active == True
        ).first()
        
        if not lock:
            return ApiResponse(
                success=True,
                message=f"Resource '{resource_name}' is not locked",
                data={
                    "resource_name": resource_name,
                    "is_locked": False,
                    "locked_by": None,
                    "locked_at": None,
                    "expires_at": None
                }
            )
        
        return ApiResponse(
            success=True,
            message=f"Resource '{resource_name}' status retrieved successfully",
            data={
                "resource_name": resource_name,
                "is_locked": True,
                "locked_by": lock.process_id,
                "locked_at": lock.locked_at.isoformat(),
                "expires_at": lock.expires_at.isoformat() if lock.expires_at else None
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get lock status: {str(e)}"
        )

@app.get("/locks/all-locked", response_model=ApiResponse)
async def get_all_locked_resources(db: Session = Depends(get_db)):
    """Get all currently locked resources"""
    try:
        # Clean up expired locks first
        cleanup_expired_locks(db)
        
        active_locks = db.query(ResourceLock).filter(
            ResourceLock.is_active == True
        ).all()
        
        locks_data = []
        for lock in active_locks:
            locks_data.append({
                "id": lock.id,
                "resource_name": lock.resource_name,
                "process_id": lock.process_id,
                "locked_at": lock.locked_at.isoformat(),
                "expires_at": lock.expires_at.isoformat() if lock.expires_at else None
            })
        
        return ApiResponse(
            success=True,
            message=f"Retrieved {len(locks_data)} active locks",
            data={
                "total_locks": len(locks_data),
                "locks": locks_data
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all locked resources: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Resource Lock Manager"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
