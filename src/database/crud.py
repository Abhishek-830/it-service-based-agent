
from sqlalchemy.orm import Session
from src.database.models import Ticket, TicketActivity
import uuid


# CREATE: Create a new ticket
def create_ticket(
    db: Session,
    title: str,
    description: str,
    requester_name: str,
    requester_email: str,
    category: str = "General",
    priority: str = "Medium"
):

    ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"

    new_ticket = Ticket(
        ticket_number=ticket_number,
        title=title,
        description=description,
        requester_name=requester_name,
        requester_email=requester_email,
        category=category,
        priority=priority,
        status="Open"
    )

    db.add(new_ticket)
    db.flush()

    # Automatically record ticket creation
    activity = TicketActivity(
        ticket_id=new_ticket.id,
        activity_type="Ticket Created",
        description=f"Ticket {ticket_number} was created with priority {priority}.",
        performed_by="System"
    )

    db.add(activity)

    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# READ: Get ticket by ID
def get_ticket_by_id(db: Session, ticket_id: int):

    return db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()


# READ: Get ticket by ticket number
def get_ticket_by_number(db: Session, ticket_number: str):

    return db.query(Ticket).filter(
        Ticket.ticket_number == ticket_number
    ).first()


# READ: Get all tickets
def get_all_tickets(db: Session):

    return db.query(Ticket).order_by(
        Ticket.created_at.desc()
    ).all()


# UPDATE: Update ticket details
def update_ticket(db: Session, ticket_id: int, update_data: dict):

    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return None

    allowed_fields = [
        "title",
        "description",
        "category",
        "priority",
        "status",
        "assigned_to",
        "escalation_reason",
        "handoff_status"
    ]

    changes = []

    for field, value in update_data.items():

        if field in allowed_fields:

            old_value = getattr(ticket, field)

            if old_value != value:

                setattr(ticket, field, value)

                changes.append(
                    f"{field}: {old_value} -> {value}"
                )

    # Record update activity
    if changes:

        if "handoff_status" in update_data and update_data["handoff_status"] == "Assigned":

            activity_type = "Human Handoff"

        elif "status" in update_data:

            activity_type = "Status Updated"

        else:

            activity_type = "Ticket Updated"

        activity = TicketActivity(
            ticket_id=ticket.id,
            activity_type=activity_type,
            description="; ".join(changes),
            performed_by="System"
        )

        db.add(activity)

    db.commit()
    db.refresh(ticket)

    return ticket


# DELETE: Delete a ticket
def delete_ticket(db: Session, ticket_id: int):

    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return False

    db.delete(ticket)
    db.commit()

    return True


# CREATE: Create ticket activity
def create_ticket_activity(
    db: Session,
    ticket_id: int,
    activity_type: str,
    description: str,
    performed_by: str = "System"
):

    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return None

    activity = TicketActivity(
        ticket_id=ticket_id,
        activity_type=activity_type,
        description=description,
        performed_by=performed_by
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


# READ: Get all activities of a ticket
def get_ticket_activities(db: Session, ticket_id: int):

    return db.query(TicketActivity).filter(
        TicketActivity.ticket_id == ticket_id
    ).order_by(
        TicketActivity.created_at.asc(),
        TicketActivity.id.asc()
    ).all()
