from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TranscriptData(BaseModel):
    content: str
    start_timestamp_in_seconds: float
    end_time_timestamp_in_seconds: Optional[float] = None
    speaker: Optional[str] = None
    subject: Optional[str] = None  # 主体
    action: Optional[str] = None  # 做了什么