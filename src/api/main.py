
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from src.config import APP_NAME

from src.database.connection import (
    Base,
    engine,
    get_db,
    SessionLocal
)
from src.database import models
from src.database.crud import (
    create_ticket,
    get_ticket_by_number,
    update_ticket,
    get_ticket_activities
)

from src.agent.agent import run_agent
from src.agent.priority_classifier import classify_ticket_priority
from src.agent.escalation import escalate_overdue_tickets

from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    TicketCreateRequest,
    TicketStatusUpdateRequest,
    TicketHandoffRequest,
    TicketResponse,
    TicketActivityResponse
)


# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# Scheduler Configuration
ESCALATION_INTERVAL = 300  # 5 minutes


# Run escalation check in a separate thread
def run_escalation_check():

    db = SessionLocal()

    try:

        escalated = escalate_overdue_tickets(db)

        return escalated

    finally:

        db.close()


# Background Ticket Escalation Scheduler
async def escalation_scheduler():

    logger.info("Ticket Escalation Scheduler Started.")

    try:

        while True:

            try:

                # Run synchronous database work outside async event loop
                escalated = await asyncio.to_thread(
                    run_escalation_check
                )

                if escalated:

                    logger.info(
                        "Automatically escalated %s tickets.",
                        len(escalated)
                    )

                    for ticket in escalated:

                        logger.info(
                            "Escalated Ticket: %s",
                            ticket["ticket_number"]
                        )

                else:

                    logger.info(
                        "Escalation check completed. No overdue tickets."
                    )

            except Exception:

                logger.exception(
                    "Background Escalation Error."
                )

            await asyncio.sleep(ESCALATION_INTERVAL)

    except asyncio.CancelledError:

        logger.info("Ticket Escalation Scheduler Stopped.")

        raise


# Application Startup and Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables initialized.")

    scheduler_task = asyncio.create_task(
        escalation_scheduler(),
        name="ticket-escalation-scheduler"
    )

    try:

        yield

    finally:

        scheduler_task.cancel()

        try:

            await scheduler_task

        except asyncio.CancelledError:

            pass

        logger.info("Application shutting down.")


# Initialize FastAPI
app = FastAPI(
    title=APP_NAME,
    description=(
        "AI-powered IT Service Desk Agent "
        "using RAG, MCP, Gemini and Groq."
    ),
    version="1.0.0",
    lifespan=lifespan
)


# Helper Function: Convert Ticket to Response
def format_ticket(ticket):

    return {
        "ticket_number": ticket.ticket_number,
        "title": ticket.title,
        "description": ticket.description,
        "requester_name": ticket.requester_name,
        "requester_email": ticket.requester_email,
        "category": ticket.category,
        "priority": ticket.priority,
        "status": ticket.status,
        "created_at": ticket.created_at,

        # Human Support Handoff
        "assigned_to": ticket.assigned_to,
        "escalation_reason": ticket.escalation_reason,
        "handoff_status": ticket.handoff_status
    }


# ROUTE 1: Home
@app.get("/")
def home():

    return {
        "application": APP_NAME,
        "message": "IT Service Desk AI Agent is running.",
        "version": "1.0.0"
    }


# ROUTE 2: Health Check
@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return HealthResponse(
        status="healthy",
        application=APP_NAME,
        version="1.0.0"
    )


# ROUTE 3: AI Agent Chat
@app.post(
    "/agent/chat",
    response_model=ChatResponse
)
async def chat_with_agent(request: ChatRequest):

    try:

        answer = await run_agent(
            user_message=request.user_message
        )

        return ChatResponse(answer=answer)

    except Exception:

        logger.exception("Agent API Error.")

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing your request."
        )


# ROUTE 4: Create Support Ticket with AI Priority
@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=201
)
def create_new_ticket(
    request: TicketCreateRequest,
    db: Session = Depends(get_db)
):

    try:

        priority = classify_ticket_priority(
            title=request.title,
            description=request.description
        )

        logger.info(
            "AI Classified Ticket Priority: %s",
            priority
        )

        ticket = create_ticket(
            db=db,
            title=request.title,
            description=request.description,
            requester_name=request.requester_name,
            requester_email=request.requester_email,
            category=request.category,
            priority=priority
        )

        return format_ticket(ticket)

    except Exception:

        logger.exception("Ticket Creation Error.")

        raise HTTPException(
            status_code=500,
            detail="Unable to create support ticket."
        )


# ROUTE 5: Get All / Filter Support Tickets
@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets(
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    db: Session = Depends(get_db)
):

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Escalated"
    ]

    allowed_priorities = [
        "Low",
        "Medium",
        "High"
    ]

    if status and status not in allowed_statuses:

        raise HTTPException(
            status_code=422,
            detail="Invalid status filter."
        )

    if priority and priority not in allowed_priorities:

        raise HTTPException(
            status_code=422,
            detail="Invalid priority filter."
        )

    query = db.query(models.Ticket)

    if status:

        query = query.filter(
            models.Ticket.status == status
        )

    if priority:

        query = query.filter(
            models.Ticket.priority == priority
        )

    tickets = query.order_by(
        models.Ticket.created_at.desc()
    ).all()

    return [
        format_ticket(ticket)
        for ticket in tickets
    ]


# ROUTE 6: Get Ticket by Ticket Number
@app.get(
    "/tickets/{ticket_number}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_number: str,
    db: Session = Depends(get_db)
):

    ticket = get_ticket_by_number(
        db,
        ticket_number
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    return format_ticket(ticket)


# ROUTE 7: Update Ticket Status
@app.patch(
    "/tickets/{ticket_number}/status",
    response_model=TicketResponse
)
def update_ticket_status(
    ticket_number: str,
    request: TicketStatusUpdateRequest,
    db: Session = Depends(get_db)
):

    ticket = get_ticket_by_number(
        db,
        ticket_number
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    updated_ticket = update_ticket(
        db,
        ticket.id,
        {"status": request.new_status}
    )

    return format_ticket(updated_ticket)


# ROUTE 8: Manual Ticket Escalation
@app.post("/tickets/escalate")
def escalate_tickets(
    db: Session = Depends(get_db)
):

    try:

        escalated = escalate_overdue_tickets(db)

        return {
            "message": "Ticket escalation process completed.",
            "total_escalated": len(escalated),
            "escalated_tickets": escalated
        }

    except Exception:

        logger.exception("Ticket Escalation API Error.")

        raise HTTPException(
            status_code=500,
            detail="Unable to escalate tickets."
        )


# ROUTE 9: Human Support Handoff
@app.post(
    "/tickets/{ticket_number}/handoff",
    response_model=TicketResponse
)
def handoff_ticket_to_human(
    ticket_number: str,
    request: TicketHandoffRequest,
    db: Session = Depends(get_db)
):

    ticket = get_ticket_by_number(
        db,
        ticket_number
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    if ticket.status == "Resolved":

        raise HTTPException(
            status_code=400,
            detail="Resolved tickets cannot be handed off."
        )

    if ticket.handoff_status == "Assigned":

        raise HTTPException(
            status_code=400,
            detail="Ticket is already assigned to human support."
        )

    try:

        updated_ticket = update_ticket(
            db,
            ticket.id,
            {
                "status": "Escalated",
                "assigned_to": request.assigned_to,
                "escalation_reason": request.escalation_reason,
                "handoff_status": "Assigned"
            }
        )

        logger.info(
            "Ticket %s assigned to %s",
            ticket_number,
            request.assigned_to
        )

        return format_ticket(updated_ticket)

    except Exception:

        logger.exception("Human Handoff Error.")

        raise HTTPException(
            status_code=500,
            detail="Unable to assign ticket to human support."
        )


# ROUTE 10: Get Ticket Activity History
@app.get(
    "/tickets/{ticket_number}/history",
    response_model=list[TicketActivityResponse]
)
def get_ticket_history(
    ticket_number: str,
    db: Session = Depends(get_db)
):

    ticket = get_ticket_by_number(
        db,
        ticket_number
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    activities = get_ticket_activities(
        db,
        ticket.id
    )

    return activities
