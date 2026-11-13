
from src.config import (
    APP_NAME,
    APP_ENV,
    GROQ_API_KEY,
    GOOGLE_API_KEY,
    validate_config
)

print("Application:", APP_NAME)
print("Environment:", APP_ENV)

try:
    validate_config()
    print("Groq API Key: Available")
    print("Google API Key: Available")
    print("Configuration: Valid")

except ValueError as error:
    print(error)
