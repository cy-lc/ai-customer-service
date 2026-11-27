
from mcp.server.fastmcp import FastMCP
mcp=FastMCP("weather")
@mcp.tool()
def get_weather(city):
    """
    Get the weather in a city.
    :param city:
    :return:
    """

    return f"{city}天气100°."

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="stdio")






