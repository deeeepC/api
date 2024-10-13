from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class CANMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int
    signal_name: str
    signal_value: float
    timestamp: datetime