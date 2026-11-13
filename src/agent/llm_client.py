
from groq import (
    Groq,
    APIError,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError
)

from src.config import GROQ_API_KEY


MODEL_NAME = "openai/gpt-oss-20b"

REQUEST_TIMEOUT = 20.0
MAX_RETRIES = 1


def get_llm_response(
    user_message: str,
    system_prompt: str = None,
    temperature: float = 0.3,
    max_completion_tokens: int = 500,
    reasoning_effort: str = None
) -> str:

    if not isinstance(user_message, str) or not user_message.strip():
        return "Error: Please provide a valid message."

    if not GROQ_API_KEY:
        return "Error: Groq API key is missing. Check your .env file."

    try:
        client = Groq(
            api_key=GROQ_API_KEY,
            timeout=REQUEST_TIMEOUT,
            max_retries=MAX_RETRIES
        )

        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        else:
            messages.append({
                "role": "system",
                "content": (
                    "You are an IT Service Desk AI Assistant. "
                    "Help users with IT-related problems. "
                    "Give clear, professional and practical answers."
                )
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        request_params = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": temperature,
            "max_completion_tokens": max_completion_tokens
        }

        if reasoning_effort:
            request_params["reasoning_effort"] = reasoning_effort

        response = client.chat.completions.create(**request_params)

        if not response.choices:
            return "Error: Groq returned an empty response."

        content = response.choices[0].message.content

        if not content:
            return "Error: Groq returned empty message content."

        return content.strip()

    except AuthenticationError:
        return "Error: Groq API authentication failed. Check your API key."

    except RateLimitError:
        return "Error: Groq API rate limit reached. Please try again later."

    except APITimeoutError:
        return "Error: Groq API request timed out. Please try again."

    except APIConnectionError:
        return "Error: Unable to connect to Groq. Check your internet connection."

    except APIError:
        return "Error: Groq API request failed. Please try again later."

    except Exception:
        return "Error: An unexpected error occurred while processing your request."
