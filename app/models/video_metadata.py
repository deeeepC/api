from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class VideoMetadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: str
    start_timestamp: datetime
    end_timestamp: datetime
    file_path: str