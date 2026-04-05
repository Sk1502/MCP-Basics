from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
async def get_weather() -> str:
    """
    Get the weather for the Hyderabad
    """
    return "its always sunny in Hyderabad"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")