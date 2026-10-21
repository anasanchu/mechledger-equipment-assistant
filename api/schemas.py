"""Pydantic schemas and request/response models for the IKB-RAG API."""

from typing import List
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request payload schema for query endpoint."""
    question: str = Field(..., description="Troubleshooting or factual question")
    chat_id: str = Field(default="default", description="Session identifier for multi-turn chats")


class QueryResponse(BaseModel):
    """Response payload schema for query endpoint."""
    answer: str = Field(..., description="Synthesized troubleshooting response or RCA checklist")


class UploadResponse(BaseModel):
    """Response payload schema for document upload."""
    message: str = Field(..., description="Status message detailing indexed chunks")
    filename: str = Field(..., description="Uploaded document filename")


class DocumentListResponse(BaseModel):
    """Response payload schema for listing documents."""
    documents: List[str] = Field(..., description="List of active documents for the chat session")


class MessageResponse(BaseModel):
    """Generic status/message response schema."""
    message: str = Field(..., description="Action status message")


__all__ = [
    "QueryRequest",
    "QueryResponse",
    "UploadResponse",
    "DocumentListResponse",
    "MessageResponse",
]
