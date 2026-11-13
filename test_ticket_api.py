
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


print("\n========== CREATE SUPPORT TICKET ==========")

ticket_data = {
    "title": "API Test Laptop Issue",
    "description": "Laptop is not starting properly.",
    "requester_name": "Abhishek",
    "requester_email": "abhishek@example.com",
    "category": "Hardware",
    "priority": "High"
}

response = client.post(
    "/tickets",
    json=ticket_data
)

print("Status Code:", response.status_code)
print("Response:", response.json())

assert response.status_code == 201

ticket_number = response.json()["ticket_number"]


print("\n========== GET ALL TICKETS ==========")

response = client.get("/tickets")

print("Status Code:", response.status_code)
print("Total Tickets:", len(response.json()))

assert response.status_code == 200


print("\n========== GET SINGLE TICKET ==========")

response = client.get(
    f"/tickets/{ticket_number}"
)

print("Status Code:", response.status_code)
print("Response:", response.json())

assert response.status_code == 200


print("\n========== UPDATE TICKET STATUS ==========")

response = client.patch(
    f"/tickets/{ticket_number}/status",
    json={
        "new_status": "In Progress"
    }
)

print("Status Code:", response.status_code)
print("Updated Status:", response.json()["status"])

assert response.status_code == 200
assert response.json()["status"] == "In Progress"


print("\nTicket API Test Successful!")
