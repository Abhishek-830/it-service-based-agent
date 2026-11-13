
from src.database.connection import SessionLocal
from src.database.crud import (
    create_ticket,
    get_ticket_by_id,
    get_ticket_by_number,
    get_all_tickets,
    update_ticket,
    delete_ticket
)


db = SessionLocal()

try:

    # CREATE
    print("\n--- CREATE TICKET ---")

    ticket = create_ticket(
        db=db,
        title="Internet Connection Problem",
        description="Office internet is not working.",
        requester_name="Abhishek",
        requester_email="abhishek@example.com",
        category="Network",
        priority="High"
    )

    print("Ticket Created:", ticket.ticket_number)


    # READ
    print("\n--- READ TICKET ---")

    fetched_ticket = get_ticket_by_id(db, ticket.id)

    print("Title:", fetched_ticket.title)
    print("Status:", fetched_ticket.status)


    # READ BY TICKET NUMBER
    print("\n--- SEARCH BY TICKET NUMBER ---")

    searched_ticket = get_ticket_by_number(
        db, ticket.ticket_number
    )

    print("Found:", searched_ticket.ticket_number)


    # UPDATE
    print("\n--- UPDATE TICKET ---")

    updated_ticket = update_ticket(
        db,
        ticket.id,
        {"status": "In Progress"}
    )

    print("Updated Status:", updated_ticket.status)


    # READ ALL
    print("\n--- ALL TICKETS ---")

    all_tickets = get_all_tickets(db)

    print("Total Tickets:", len(all_tickets))


    # DELETE
    print("\n--- DELETE TICKET ---")

    deleted = delete_ticket(db, ticket.id)

    print("Deleted:", deleted)


finally:
    db.close()
