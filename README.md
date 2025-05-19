# Travel Server MCP

A modular MCP server for searching flights using the Duffel API. Built for extensibility, maintainability, and clarity.

## Step-by-Step Tutorial

If you want a guided walkthrough on how this server was created from scratch, check out the [Step-by-Step Tutorial](step-by-step-tutorial.md).

## Features
- Search for flights between any two airports using the Duffel API
- Granular, well-documented codebase with clear separation of concerns
- Detailed debug logging returned with every search
- Easily extensible for new tools, models, or providers

## Project Structure
```
travelserver/
├── main.py                # Entrypoint: sets up and runs the MCP server
├── duffel_client.py       # Duffel API HTTP logic (search_flights)
├── models/
│   ├── __init__.py
│   ├── flight_search_params.py
│   └── flight_offer.py
├── tools/
│   └── flight_tools.py    # MCP tool for flight search
├── .env                   # (not committed) Your Duffel API key
├── pyproject.toml         # Project dependencies
└── ...
```

## Setup
1. **Clone the repository**
```bash
git clone https://github.com/kidehen/mcp-travel-server.git
cd mcp-travel-server
```

2. **Create and activate a virtual environment with uv:**
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. **Install dependencies with uv:**
   ```bash
   uv pip install -e .
   ```
4. **Create a `.env` file in the project root:**
   ```
   DUFFEL_ACCESS_TOKEN=your_duffel_api_key_here
   ```

## Usage
- The MCP server exposes a `get_flights` tool for searching flights.
- When a user asks about flights, the client will call the `get_flights` tool with the appropriate parameters.
- The server returns a list of flight offers and a detailed debug log for troubleshooting.

### MCP Inspector using NPX 
```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-travel-server run main.py
```

### Claude Desktop MCP Server Configuration 
```json
    "mcp-travel-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-travel-server",
        "run",
        "main.py"
      ]
    }
```

## Extending the Project
- Add new models to `models/` (one per file)
- Add new tools to `tools/`
- Add new API integrations to their own directories (e.g., `duffel/`, `amadeus/`)
- Keep configuration in `config/` as needed

## FAQ
- **How does the MCP client know how to interact with the Duffel API?**
  > The MCP client never talks to Duffel directly. It calls this MCP server's tool, which handles all Duffel API logic internally and returns results to the client.
- **How does the MCP client know to trigger this server for flight queries?**
  > The MCP client discovers all available MCP servers and their tools. When a user asks about flights, the client uses natural language understanding to match the user's intent to the `get_flights` tool, and then calls it.

## License
MIT

## Available Tools

### get-flights

Search for available flights between two locations.

Parameters:
- `origin`: Origin airport code (e.g., 'LHR')
- `destination`: Destination airport code (e.g., 'JFK')
- `departure_date`: Departure date in YYYY-MM-DD format
- `return_date` (optional): Return date in YYYY-MM-DD format
- `passengers` (optional): Number of adult passengers (default: 1)
- `cabin_class` (optional): Cabin class (economy, business, first) (default: economy)

Example response:
```json
[
  {
    "airline": "British Airways",
    "flight_number": "BA178",
    "departure_time": "2024-03-20T10:00:00",
    "arrival_time": "2024-03-20T13:00:00",
    "price": 299.99,
    "currency": "USD",
    "stops": 0
  }
]
```
