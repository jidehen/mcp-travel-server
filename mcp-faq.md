# Flight Server FAQ

This section answers common questions about the Travel Server MCP and its flight search tool.

## Questions & Answers

**Q: How does the MCP client know how to interact with the Duffel API?**

A: The MCP client (such as Claude Desktop) does **NOT** interact with the Duffel API directly. Instead, it communicates with this MCP server using the MCP protocol. This server acts as a bridge: it exposes a tool (`get_flights`) that the client can call. When the tool is invoked, the server code makes the actual HTTP requests to the Duffel API, processes the results, and returns them to the client. The client only needs to know the tool's interface (parameters and return type), not the details of the Duffel API.

**Q: How does the MCP client know that it should trigger this MCP server when a user asks about flights?**

A: The MCP client discovers available MCP servers and their tools via the MCP protocol. Each server registers its tools (like `get_flights`) with a name and description. When a user asks about flights, the client uses natural language understanding (NLU) to match the user's intent to available tools. If the user's query matches the description or parameters of the `get_flights` tool, the client will call this tool on the MCP server. The matching process is handled by the client (e.g., Claude Desktop), not by this server.

**Q: How is context persisted across sessions, or is it not persisted?**

A: MCP servers are designed to be stateless. They receive a request (like a tool call) and return a response. They do not inherently maintain conversation context or session state across multiple interactions or separate runs. The persistence of context, if any, is handled by the MCP client (e.g., Claude Desktop) which manages the conversation history and can provide relevant context back to the server in subsequent requests if the protocol supports it for that type of interaction. For tool calls like `get_flights`, each invocation is typically independent. 