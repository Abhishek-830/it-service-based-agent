
import json

from mcp.server.fastmcp import FastMCP

from src.rag.retriever import semantic_search

from src.database.connection import SessionLocal
from src.database.crud import (
    create_ticket,
    get_ticket_by_number,
    get_all_tickets,
    update_ticket
)

from src.agent.priority_classifier import classify_ticket_priority


# Initialize MCP Server
mcp = FastMCP("IT Service Desk MCP Server")


# Helper function to format ticket data
def ticket_to_dict(ticket):

    return {
        "ticket_number": ticket.ticket_number,
        "title": ticket.title,
        "description": ticket.description,
        "requester_name": ticket.requester_name,
        "requester_email": ticket.requester_email,
        "category": ticket.category,
        "priority": ticket.priority,
        "status": ticket.status,
        "created_at": str(ticket.created_at)
    }


# TOOL 1: Create Support Ticket with AI Priority
@mcp.tool()
def create_support_ticket(
    title: str,
    description: str,
    requester_name: str,
    requester_email: str,
    category: str = "General"
) -> str:
    """
    Create a new IT support ticket.
    Automatically classify ticket priority using AI.
    """

    db = SessionLocal()

    try:

        # Step 1: Classify priority using AI
        priority = classify_ticket_priority(
            title=title,
            description=description
        )

        print(f"AI Classified Ticket Priority: {priority}")

        # Step 2: Create ticket in database
        ticket = create_ticket(
            db=db,
            title=title,
            description=description,
            requester_name=requester_name,
            requester_email=requester_email,
            category=category,
            priority=priority
        )

        return json.dumps(
            ticket_to_dict(ticket),
            indent=2,
            ensure_ascii=False
        )

    except Exception as error:

        return json.dumps({
            "error": "Unable to create support ticket.",
            "details": str(error)
        }, ensure_ascii=False)

    finally:
        db.close()


# TOOL 2: Get Ticket Status
@mcp.tool()
def get_support_ticket(ticket_number: str) -> str:
    """Find a support ticket and return its current details."""

    db = SessionLocal()

    try:
        ticket = get_ticket_by_number(db, ticket_number)

        if not ticket:
            return "Ticket not found."

        return json.dumps(
            ticket_to_dict(ticket),
            indent=2
        )

    finally:
        db.close()


# TOOL 3: List All Tickets
@mcp.tool()
def list_support_tickets() -> str:
    """Return all support tickets."""

    db = SessionLocal()

    try:
        tickets = get_all_tickets(db)

        result = [
            ticket_to_dict(ticket)
            for ticket in tickets
        ]

        return json.dumps(result, indent=2)

    finally:
        db.close()


# TOOL 4: Update Ticket Status
@mcp.tool()
def update_support_ticket_status(
    ticket_number: str,
    new_status: str
) -> str:
    """Update the status of an existing support ticket."""

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Escalated"
    ]

    if new_status not in allowed_statuses:
        return (
            "Invalid status. Allowed values: "
            + ", ".join(allowed_statuses)
        )

    db = SessionLocal()

    try:
        ticket = get_ticket_by_number(db, ticket_number)

        if not ticket:
            return "Ticket not found."

        updated_ticket = update_ticket(
            db,
            ticket.id,
            {"status": new_status}
        )

        return json.dumps(
            ticket_to_dict(updated_ticket),
            indent=2
        )

    finally:
        db.close()


# TOOL 5: Search IT Knowledge Base (RAG)
@mcp.tool()
def search_knowledge_base(
    query: str,
    top_k: int = 3
) -> str:
    """
    Search the IT Support Knowledge Base for relevant
    troubleshooting information.
    """

    if not query.strip():
        return json.dumps({
            "error": "Search query cannot be empty."
        })

    if top_k < 1 or top_k > 5:
        return json.dumps({
            "error": "top_k must be between 1 and 5."
        })

    try:
        results = semantic_search(
            query=query,
            top_k=top_k
        )

        return json.dumps({
            "query": query,
            "total_results": len(results),
            "results": results
        }, indent=2, ensure_ascii=False)

    except Exception as error:
        return json.dumps({
            "error": str(error)
        }, ensure_ascii=False)


# Start MCP Server
if __name__ == "__main__":
    mcp.run(transport="stdio")
