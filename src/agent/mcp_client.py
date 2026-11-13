
import sys
import asyncio
import logging
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Logger Configuration
logger = logging.getLogger(__name__)


# MCP Server Configuration
server_params = StdioServerParameters(
    command=sys.executable,
    args=["-m", "src.mcp_server.server"]
)

# Connection timeout
CONNECTION_TIMEOUT = 20


@asynccontextmanager
async def connect_to_mcp_server():
    """
    Connect to MCP Server and provide an active client session.
    Handles connection, initialization and timeout errors.
    """

    try:
        logger.info("Connecting to MCP Server...")

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                # Initialize MCP connection with timeout
                try:
                    await asyncio.wait_for(
                        session.initialize(),
                        timeout=CONNECTION_TIMEOUT
                    )

                except asyncio.TimeoutError:
                    logger.error("MCP Server initialization timed out.")
                    raise

                except Exception:
                    logger.exception("MCP Server initialization failed.")
                    raise

                logger.info("MCP Server connected successfully.")

                yield session

                logger.info("MCP Client session closed.")

    except OSError:
        logger.exception("Unable to start or connect to MCP Server.")
        raise

    except Exception:
        logger.exception("MCP Client encountered an unexpected error.")
        raise
