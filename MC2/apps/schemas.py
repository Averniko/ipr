from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    id: int
    session_id: int
    mc1_timestamp: Optional[datetime] = None
    mc2_timestamp: Optional[datetime] = None
    mc3_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None
