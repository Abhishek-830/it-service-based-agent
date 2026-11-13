from src.api.schemas import (
    TicketCreateRequest,
    TicketStatusUpdateRequest
)

ticket = TicketCreateRequest(
    title="Laptop Not Working",
    description="My office laptop is not starting.",
    requester_name="Abhishek",
    requester_email="abhishek@example.com",
    category="Hardware",
    priority="High"
)

print("\nTicket Request:")
print(ticket.model_dump())

update = TicketStatusUpdateRequest(
    new_status="In Progress"
)

print("\nStatus Update:")
print(update.model_dump())

try:
    TicketCreateRequest(
        title="Laptop Issue",
        description="Laptop is not working.",
        requester_name="Abhishek",
        requester_email="abhishek@example.com",
        priority="Urgent"
    )
except Exception:
    print("\nInvalid priority rejected successfully.")

print("\nTicket API Schemas Test Successful!")