
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ==========================================
# 1. USER REQUEST FOR AI AGENT
# ==========================================

class ChatRequest(BaseModel):

    user_message: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="User's IT support question"
    )


# ==========================================
# 2. AI AGENT RESPONSE
# ==========================================

class ChatResponse(BaseModel):

    answer: str = Field(
        ...,
        description="AI Agent generated response"
    )


# ==========================================
# 3. API HEALTH RESPONSE
# ==========================================

class HealthResponse(BaseModel):

    status: str
    application: str
    version: str


# ==========================================
# 4. CREATE SUPPORT TICKET REQUEST
# ==========================================

class TicketCreateRequest(BaseModel):

    title: str = Field(
        ...,
        min_length=3,
        max_length=200
    )

    description: str = Field(
        ...,
        min_length=5
    )

    requester_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    requester_email: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    category: str = Field(
        default="General",
        max_length=100
    )


# ==========================================
# 5. UPDATE TICKET STATUS REQUEST
# ==========================================

class TicketStatusUpdateRequest(BaseModel):

    new_status: Literal[
        "Open",
        "In Progress",
        "Resolved",
        "Escalated"
    ]


# ==========================================
# 6. HUMAN SUPPORT HANDOFF REQUEST
# ==========================================

class TicketHandoffRequest(BaseModel):

    assigned_to: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name of human support person or team"
    )

    escalation_reason: str = Field(
        ...,
        min_length=5,
        description="Reason for transferring ticket to human support"
    )


# ==========================================
# 7. TICKET RESPONSE
# ==========================================

class TicketResponse(BaseModel):

    ticket_number: str
    title: str
    description: str
    requester_name: str
    requester_email: str
    category: str | None
    priority: str
    status: str
    created_at: datetime | None

    # Human Support Handoff Information
    assigned_to: str | None
    escalation_reason: str | None
    handoff_status: str


# ==========================================
# 8. TICKET ACTIVITY HISTORY RESPONSE
# ==========================================

class TicketActivityResponse(BaseModel):

    id: int
    ticket_id: int
    activity_type: str
    description: str
    performed_by: str
    created_at: datetime | None

    class Config:
        from_attributes = True
