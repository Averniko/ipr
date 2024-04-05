from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    id: int
    session_id: int
    mc1_timestamp: Optional[datetime] = None
    mc2_timestamp: Optional[datetime] = None
    mc3_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None


class MetricsBase(BaseModel):
    session_id: int
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
    duration: Optional[timedelta] = None
    messages_count: int = 0
    rps: float = 0.0
