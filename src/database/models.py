
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.database.connection import Base


class Ticket(Base):

    __tablename__ = "tickets"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Ticket Information
    ticket_number = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(String(200), nullable=False)

    description = Column(Text, nullable=False)

    # User Information
    requester_name = Column(String(100), nullable=False)

    requester_email = Column(String(150), nullable=False)

    # Ticket Classification
    category = Column(String(100), nullable=True)

    priority = Column(
        String(20),
        default="Medium",
        nullable=False
    )

    status = Column(
        String(30),
        default="Open",
        nullable=False
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Human Support Handoff
    assigned_to = Column(
        String(100),
        nullable=True
    )

    escalation_reason = Column(
        Text,
        nullable=True
    )

    handoff_status = Column(
        String(30),
        default="Pending",
        nullable=False
    )


# Ticket Activity History Model
class TicketActivity(Base):

    __tablename__ = "ticket_activities"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Related Ticket
    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    # Activity Information
    activity_type = Column(
        String(100),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    performed_by = Column(
        String(100),
        default="System",
        nullable=False
    )

    # Activity Timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
