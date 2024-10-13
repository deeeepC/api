from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class SensorData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int
    value: float
    timestamp: datetime