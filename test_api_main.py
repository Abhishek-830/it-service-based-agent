
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


print("\n========== TEST ROOT ENDPOINT ==========")

response = client.get("/")

print("Status Code:", response.status_code)
print("Response:", response.json())


print("\n========== TEST HEALTH ENDPOINT ==========")

response = client.get("/health")

print("Status Code:", response.status_code)
print("Response:", response.json())


print("\n========== TEST INVALID CHAT REQUEST ==========")

response = client.post(
    "/agent/chat",
    json={
        "user_message": "Hi"
    }
)

print("Status Code:", response.status_code)
print("Response:", response.json())


print("\nFastAPI Basic Tests Completed!")
