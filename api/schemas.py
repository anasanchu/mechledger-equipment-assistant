"""Pydantic schemas and request/response models for the MECHLEDGER API."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request payload schema for query endpoint."""
    question: str = Field(..., description="Troubleshooting or factual question")
    chat_id: str = Field(default="default", pattern=r"^[A-Za-z0-9_-]{1,64}$", description="Session identifier for multi-turn chats")
    equipment_context: str = Field(default="", max_length=2000, description="Optional operator-supplied equipment identification and observations")


class QueryResponse(BaseModel):
    """Response payload schema for query endpoint."""
    answer: str = Field(..., description="Synthesized troubleshooting response or RCA checklist")


class UploadResponse(BaseModel):
    """Response payload schema for document upload."""
    message: str = Field(..., description="Status message for the saved document")
    filename: str = Field(..., description="Uploaded document filename")
    status: str = Field(default="processing", description="Document processing status")


class DocumentListResponse(BaseModel):
    """Response payload schema for listing documents."""
    documents: List[str] = Field(..., description="List of active documents for the chat session")


class MessageResponse(BaseModel):
    """Generic status/message response schema."""
    message: str = Field(..., description="Action status message")


class ReportRequest(BaseModel):
    case_title: str = Field(..., max_length=200)
    equipment: Dict[str, str] = Field(default_factory=dict)
    problem: str = Field(default="", max_length=10000)
    messages: List[Dict[str, Any]] = Field(default_factory=list, max_length=100)
    documents: List[str] = Field(default_factory=list, max_length=100)
    remarks: str = Field(default="", max_length=10000)


__all__ = [
    "QueryRequest",
    "QueryResponse",
    "UploadResponse",
    "DocumentListResponse",
    "MessageResponse",
    "ReportRequest",
]
