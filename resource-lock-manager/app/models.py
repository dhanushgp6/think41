from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base
import datetime

class ResourceLock(Base):
    __tablename__ = "resource_locks"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String, unique=True, index=True, nullable=False)
    process_id = Column(String, nullable=False)
    locked_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    def is_expired(self):
        if self.expires_at is None:
            return False
        return datetime.datetime.now(datetime.timezone.utc) > self.expires_at
