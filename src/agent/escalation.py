
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Ticket, TicketActivity


ESCALATION_RULES = {
    "High": timedelta(minutes=30),
    "Medium": timedelta(hours=24),
    "Low": timedelta(hours=72)
}


def escalate_overdue_tickets(db: Session):
    now = datetime.utcnow()

    tickets = (
        db.query(Ticket)
        .filter(Ticket.status.in_(["Open", "In Progress"]))
        .all()
    )

    escalated_tickets = []

    for ticket in tickets:
        threshold = ESCALATION_RULES.get(ticket.priority)

        if not threshold or not ticket.created_at:
            continue

        created_at = ticket.created_at.replace(tzinfo=None)
        ticket_age = now - created_at

        if ticket_age >= threshold:
            old_status = ticket.status

            ticket.status = "Escalated"
            ticket.updated_at = now

            activity = TicketActivity(
                ticket_id=ticket.id,
                activity_type="Automatic Escalation",
                description=(
                    f"Ticket automatically escalated due to overdue response. "
                    f"Priority: {ticket.priority}, "
                    f"Previous status: {old_status}, "
                    f"New status: Escalated."
                ),
                performed_by="System"
            )

            db.add(activity)

            escalated_tickets.append({
                "ticket_number": ticket.ticket_number,
                "title": ticket.title,
                "priority": ticket.priority,
                "status": ticket.status
            })

    if escalated_tickets:
        db.commit()

    return escalated_tickets
