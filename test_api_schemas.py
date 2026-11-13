
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse
)


print("\n========== TESTING CHAT REQUEST ==========")

request = ChatRequest(
    user_message="My laptop is not connecting to Wi-Fi."
)

print(request.model_dump())


print("\n========== TESTING CHAT RESPONSE ==========")

response = ChatResponse(
    answer="Please check whether Wi-Fi is enabled."
)

print(response.model_dump())


print("\n========== TESTING HEALTH RESPONSE ==========")

health = HealthResponse(
    status="healthy",
    application="IT Service Desk AI Agent",
    version="1.0.0"
)

print(health.model_dump())


print("\nAPI Schemas Test Successful!")
