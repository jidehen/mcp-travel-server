from mcp.server.fastmcp import FastMCP
from tools.flight_tools import register_flight_tools

# Create the MCP server instance
mcp = FastMCP("Travel Server")

# Register all tools (currently just flights)
register_flight_tools(mcp)

if __name__ == "__main__":
    mcp.run() 