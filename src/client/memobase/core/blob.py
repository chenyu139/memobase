# Synced from backend 0.0.5
from enum import StrEnum
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class OpenAICompatibleMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    alias: Optional[str] = None
    created_at: Optional[str] = None


class TranscriptStamp(BaseModel):
    content: str
    start_timestamp_in_seconds: float
    end_time_timestamp_in_seconds: Optional[float] = None
    speaker: Optional[str] = None
    subject: Optional[str] = None  # 主体
    action: Optional[str] = None  # 做了什么
    metrics: Optional[dict] = None  # 关键衡量数据
    result: Optional[dict] = None  # 做的结果


class BlobType(StrEnum):
    chat = "chat"
    doc = "doc"
    image = "image"
    code = "code"
    transcript = "transcript"
    action = "action"


class Blob(BaseModel):
    type: BlobType
    fields: Optional[dict] = None
    created_at: Optional[datetime] = None

    def get_blob_data(self):
        return self.model_dump(exclude={"type", "fields", "created_at"})

    def to_request(self):
        return {
            "blob_type": self.type,
            "fields": self.fields,
            "blob_data": self.get_blob_data(),
        }


class ChatBlob(Blob):
    messages: list[OpenAICompatibleMessage]
    type: Literal[BlobType.chat] = BlobType.chat


class DocBlob(Blob):
    content: str
    type: Literal[BlobType.doc] = BlobType.doc


class ActionBlob(Blob):
    transcripts: list[TranscriptStamp]
    type: Literal[BlobType.action] = BlobType.action


class CodeBlob(Blob):
    content: str
    language: Optional[str] = None
    type: Literal[BlobType.code] = BlobType.code


class ImageBlob(Blob):
    url: Optional[str] = None
    base64: Optional[str] = None
    type: Literal[BlobType.image] = BlobType.image


class TranscriptBlob(Blob):
    transcripts: list[TranscriptStamp]
    type: Literal[BlobType.transcript] = BlobType.transcript


class BlobData(BaseModel):
    blob_type: BlobType
    blob_data: dict  # messages/doc/images...
    fields: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_blob(self) -> Blob:
        if self.blob_type == BlobType.chat:
            return ChatBlob(
                **self.blob_data, fields=self.fields, created_at=self.created_at
            )
        elif self.blob_type == BlobType.doc:
            return DocBlob(
                **self.blob_data, fields=self.fields, created_at=self.created_at
            )
        elif self.blob_type == BlobType.action:
            return ActionBlob(
                **self.blob_data, fields=self.fields, created_at=self.created_at
            )
        elif self.blob_type == BlobType.transcript:
            return TranscriptBlob(
                **self.blob_data, fields=self.fields, created_at=self.created_at
            )
        elif self.blob_type == BlobType.image:
            raise NotImplementedError("ImageBlob not implemented yet.")
