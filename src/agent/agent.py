
import asyncio
import json
import logging

from groq import (
    Groq,
    APIError,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError
)

from src.config import GROQ_API_KEY
from src.agent.llm_client import MODEL_NAME
from src.agent.mcp_client import connect_to_mcp_server


logger = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 5
REQUEST_TIMEOUT = 30.0


SYSTEM_PROMPT = """
You are an intelligent IT Service Desk AI Agent.

Your responsibilities:
1. Understand IT-related user problems.
2. Search the IT Support Knowledge Base for troubleshooting information.
3. Provide clear and practical solutions using retrieved knowledge.
4. Create support tickets when the user explicitly requests it.
5. Check ticket details and status when requested.
6. Update ticket status when requested.
7. List tickets when requested.

TOOL USAGE RULES:

1. For IT troubleshooting questions:
   - Use the search_knowledge_base tool first.
   - Read the retrieved information carefully.
   - Give an answer based on the retrieved knowledge.
   - Mention the source document and page number when available.
   - Do not invent troubleshooting steps.

2. For ticket-related requests:
   - Use the appropriate MCP ticket tool.
   - Never invent ticket numbers or ticket details.
   - Ask for missing information before creating a ticket.
   - Never create a ticket without explicit user permission.

3. If the knowledge base does not contain enough information:
   - Clearly tell the user that the available knowledge base
     does not provide enough information.
   - Recommend contacting the appropriate IT support team.

4. Do not call unnecessary tools.

5. Explain tool results clearly and professionally.

6. Never expose API keys, passwords, or confidential information.
"""


async def run_agent(user_message: str) -> str:
    """
    Run IT Service Desk AI Agent using Groq and MCP tools.
    Handles LLM, MCP and tool execution errors.
    """

    if not isinstance(user_message, str) or not user_message.strip():
        return "Error: Please provide a valid message."

    if not GROQ_API_KEY:
        return "Error: Groq API key is missing."

    try:
        client = Groq(
            api_key=GROQ_API_KEY,
            timeout=REQUEST_TIMEOUT,
            max_retries=1
        )

        async with connect_to_mcp_server() as session:

            # Get available MCP tools
            mcp_tools = await session.list_tools()

            groq_tools = []

            for tool in mcp_tools.tools:
                groq_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                })

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Agent tool-calling loop
            for iteration in range(MAX_TOOL_ITERATIONS):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=groq_tools,
                    tool_choice="auto",
                    max_completion_tokens=1500
                )

                if not response.choices:
                    return "Error: Groq returned an empty response."

                assistant_message = response.choices[0].message

                messages.append(
                    assistant_message.model_dump(exclude_none=True)
                )

                # Return final answer if no tool is required
                if not assistant_message.tool_calls:
                    return (
                        assistant_message.content
                        or "No response generated."
                    )

                # Execute MCP tool calls
                for tool_call in assistant_message.tool_calls:

                    tool_name = tool_call.function.name

                    try:
                        arguments = json.loads(
                            tool_call.function.arguments
                        )

                        if not isinstance(arguments, dict):
                            raise ValueError(
                                "Tool arguments must be a JSON object."
                            )

                    except (json.JSONDecodeError, ValueError):
                        logger.exception(
                            "Invalid arguments for MCP tool: %s",
                            tool_name
                        )

                        tool_result = "Error: Invalid tool arguments."

                    else:
                        try:
                            logger.info(
                                "Executing MCP Tool: %s",
                                tool_name
                            )

                            result = await session.call_tool(
                                tool_name,
                                arguments=arguments
                            )

                            tool_result = "\n".join(
                                block.text
                                for block in result.content
                                if hasattr(block, "text")
                            )

                            if getattr(result, "isError", False):
                                tool_result = (
                                    "Tool execution failed: "
                                    + (tool_result or "Unknown tool error.")
                                )

                            elif not tool_result:
                                tool_result = "No result returned."

                        except Exception:
                            logger.exception(
                                "MCP tool execution failed: %s",
                                tool_name
                            )
                            tool_result = (
                                "Error: MCP tool execution failed."
                            )

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_result
                    })

            return "Maximum tool-calling limit reached. Please try again."

    except AuthenticationError:
        logger.exception("Groq authentication failed.")
        return "Error: Groq API authentication failed. Check your API key."

    except RateLimitError:
        logger.exception("Groq rate limit reached.")
        return "Error: Groq API rate limit reached. Please try again later."

    except APITimeoutError:
        logger.exception("Groq API request timed out.")
        return "Error: Groq API request timed out."

    except APIConnectionError:
        logger.exception("Groq connection failed.")
        return "Error: Unable to connect to Groq."

    except APIError:
        logger.exception("Groq API request failed.")
        return "Error: Groq API request failed."

    except Exception:
        logger.exception("Unexpected Agent error.")
        return "Error: Agent encountered an unexpected problem."


if __name__ == "__main__":

    question = input("\nYou: ")

    answer = asyncio.run(
        run_agent(question)
    )

    print("\nAI Agent:")
    print(answer)
