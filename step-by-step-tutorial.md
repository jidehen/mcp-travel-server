# Comprehensive Guide to Building an MCP Server

## Section 1: Preparing to Code

### Boilerplate Setup
#### Background
We will be using uv (https://docs.astral.sh/uv/) which is an extremely fast Python package and project manager, written in Rust.

uv is a cutting-edge Python package and project manager built with Rust, aims to change that. Combining the functionality of tools like pip, poetry, and virtualenv, uv streamlines tasks like dependency management, script execution, and project building—all with exceptional performance. Its seamless compatibility with pip commands, requiring no additional learning curve.

#### Install UV
```bash
brew install uv
```

#### Initialize the project with UV
```bash
uv init travelserver
```
This Initialized project `travelserver` at `/Users/username/Documents/Projects/mcp-servers/travelserver`

#### Create a virtual env with UV
```bash
uv venv
```
Activate with: 
```bash
source .venv/bin/activate
```

#### Install dependencies
```bash
uv add "mcp[cli]"
```
MCP CLI is a tool included in the MCP SDK that helps MCP server development

#### Create server.py file and delete main.py file just for stylistic purposes

### Provide Context to our Coding Assistant

#### Open Cursor
1. **Index Official MCP Documentation with Cursor and add to context**
   - Cursor Settings > Features > Docs
   - Add https://modelcontextprotocol.io/ which is MCP documentation
   - Cursor will crawl for all pages under this and index them so they can be added to llm context

2. **Index the MCP Python SDK with Cursor and add to context since we are writing in Python**
   - https://github.com/modelcontextprotocol/python-sdk 

3. **Provide context for the Duffle travel API as that is the API we will be using to get relevant travel information like available flights**
   - https://duffel.com/ 

4. **Update our project with cursor rules**
   - Give Cursor Rules in order to make it mimic as best as possible an "expert" software engineer
   - Create a .cursor directory in the project
   - Create a subdirectory called rules
   - Create a file in rules called python.mdc
   - The .mdc extension helps Cursor identify which files should be processed as rules, just like how .md helps systems identify regular Markdown files.
   - Visit https://cursor.directory/ which has a catalogue of cursor rules that other people have already created
   - Copy rules from https://cursor.directory/fastapi-python-cursor-rules 
   - Set the rule so it is attached to all requests

## Section 2: Coding the MCP Server
### Creating the initial server
1. **Open Cursor Agent**

2. **Type a message to prompt coding**
   ```
   "I want you to implement a simple MCP server from @MCP using the Python SDK @MCP Python SDK. The server should expose one tool, which is called get-flights, and allows a user to see what flights are available for a given set of search criteria. As a reference, you can view the flights-mcp server @MCP Flights as an example, which utilizes the @Duffle Offers api. Make this implementation simple."
   ```

3. **The following is what has been produced by the cursor agent**
   - Pyproject.toml updated to include description and additional dependencies
     - mcp
     - duffel-api
     - pydantic
     - python-dotenv
   - server.py updated to implement MCP server
     - MCP server setup with the get-flights tool
     - Pydantic models for request/response validation
     - Integration with the Duffel API
     - Error handling and response formatting
   - README.md updated with setup and usage instructions

4. **To use the server:**
   - You'll need to get a Duffel API key and add it to a .env file
   - Install the dependencies using pip install -e .
   - Run the server using python server.py

5. **The get-flights tool accepts the following parameters:**
   - origin: Airport code (e.g., 'LHR')
   - destination: Airport code (e.g., 'JFK')
   - departure_date: Date in YYYY-MM-DD format
   - return_date (optional): Return date for round trips
   - passengers (optional): Number of adult passengers
   - cabin_class (optional): Economy, business, or first class

6. **The server will return a list of available flights with details like airline, flight number, times, price, and number of stops.**

## Section 3: Configuring the MCP Server
### Setup Duffel API access
1. **Visit Duffel's registration page**
2. **Create an account (you can select "Personal Use" for Company Name)**
3. **Navigate to More > Developer to find your test API key (one is already provided)**

### Setup local env variable for api access ket
1. **Create a .env file to store your Duffel API token**
2. **Add .env to .gitignore to keep it secure**
3. **Create a .env file in your project root**
4. **Add Duffel API token to the .env file**

### Important security notes to remember:
- Never commit the .env file to version control
- Never share your API token publicly
- If you accidentally commit your token, rotate it immediately
- Keep your .env file secure and only share it through secure channels if needed
- Consider using a secrets manager for production environments
- Ensure that comments under @mcp.tool functions are very granular as this is how the client will know what each tool can do

### Run the mcp server with:
```bash
uv run server.py
```

## Section 4: Integrate MCP Server into Claude Desktop Client
1. Claude Desktop > Settings > Developer > Edit Config
2. Open claude_desktop_config.json
```json
{
  "mcpServers": {
    "travel-server": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "--directory",
        "/Users/jidehen/Documents/Projects/mcp-servers/travelserver",
        "run",
        "main.py"
      ]
    }
  }
}
```