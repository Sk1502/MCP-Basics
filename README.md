# MCP Basics

A practical implementation of the Model Context Protocol (MCP) demonstrating how to build and connect multiple AI tools using LangGraph and LangChain.

## Table of Contents
- [What is MCP?](#what-is-mcp)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Transport Protocols](#transport-protocols)
- [Troubleshooting](#troubleshooting)

---

## What is MCP?

MCP is a standardized protocol that allows AI models to reliably interact with tools and data sources. Unlike generic APIs:

✅ **Automatic Tool Discovery** - AI models know available tools and their parameters  
✅ **Standardized Communication** - Consistent protocol across implementations  
✅ **Structured Results** - Predictable, typed responses from tool calls  
✅ **Built-in Validation** - Parameter validation at protocol level  

### MCP vs FastAPI

| Aspect | FastAPI | MCP |
|--------|---------|-----|
| Purpose | General web APIs | AI tool integration |
| Tool Discovery | Manual (requires prompting) | Automatic (schema provided) |
| Error Handling | Variable | Standardized |
| Learning Curve | Easy | Moderate |
| Best For | Web services | AI agents with tools |

---

## Project Structure

```
MCP_Basics/
├── client.py           # Main LangGraph agent combining both servers
├── mathserver.py       # Math tools (add, multiply) - Stdio transport
├── weather.py          # Weather tools (get_weather) - HTTP transport
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project metadata
└── README.md           # This file
```

## Components

### 1. Math Server (`mathserver.py`)
**Transport:** Stdio (direct process communication)  
**Port:** N/A (subprocess)  
**Status:** Auto-started by client  
**Tools:**
- `add(a: int, b: int)` → int
- `multiply(a: int, b: int)` → int

### 2. Weather Server (`weather.py`)
**Transport:** HTTP (streamable-http)  
**Port:** localhost:8000  
**Status:** Manual start required  
**Tools:**
- `get_weather(location: str)` → str

### 3. Client Agent (`client.py`)
**Framework:** LangGraph + LangChain  
**LLM:** Groq (Llama 3.1 8B)  
**Responsibilities:**
- Connect to both MCP servers
- Retrieve available tools automatically
- Route user requests to appropriate servers
- Orchestrate multi-step tool calls via LLM

---

## Setup Instructions

### Step 1: Install Dependencies

```powershell
uv add -r requirements.txt
```

Or with pip:
```powershell
pip install -r requirements.txt
```

### Step 2: Create .env File

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/

### Step 3: Start Weather Server (Terminal 1)

```powershell
python weather.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 4: Run Client (Terminal 2)

```powershell
python client.py
```

**Expected Output:**
```
Math response: The result of the calculation is 184.
Weather response: its always sunny in Hyderabad
```

---

## How It Works

### Architecture Diagram

```
                    ┌─────────────────────────────┐
                    │   Client (LangGraph Agent)  │
                    │  - LLM: Groq Llama 3.1 8B   │
                    │  - Framework: LangChain     │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
         ┌──────────▼────────┐   ┌───────▼──────────┐
         │  Math Server      │   │ Weather Server   │
         │  (Stdio)          │   │ (HTTP)           │
         │                   │   │                  │
         │ • add()           │   │ • get_weather()  │
         │ • multiply()      │   │                  │
         └───────────────────┘   └──────────────────┘
```

### Request Flow Example: "Calculate (3+5) × 23"

```
1. User: "Calculate (3+5) × 23"
   ↓
2. Client fetches tools from both servers
   ↓
3. LLM analyzes: "Need add(3, 5) first"
   ↓
4. Math Server: add(3, 5) → 8
   ↓
5. LLM analyzes: "Now multiply(8, 23)"
   ↓
6. Math Server: multiply(8, 23) → 184
   ↓
7. Response: "The result is 184"
```

---

## Transport Protocols

### Stdio Transport (Math Server)

**How:** Direct stdin/stdout communication between processes

**Pros:**
- ✅ No network overhead
- ✅ Fast process-to-process communication
- ✅ No port conflicts
- ✅ Secure by default (local-only)
- ✅ Simple setup (auto-spawned)

**Cons:**
- ❌ Local-only (no remote access)
- ❌ Single connection per instance
- ❌ Limited scalability

**Best For:** Development, local tools, Claude Desktop

### HTTP Transport (Weather Server)

**How:** Standard HTTP API on localhost:8000

**Pros:**
- ✅ Remote access capability
- ✅ Multiple simultaneous clients
- ✅ Standard protocol
- ✅ Cloud-ready
- ✅ Load balanceable

**Cons:**
- ❌ Network overhead
- ❌ Port management required
- ❌ Requires authentication for security
- ❌ More complex setup

**Best For:** Remote servers, cloud deployment, multiple clients

### Comparison Table

| Feature | Stdio | HTTP |
|---------|-------|------|
| **Performance** | 🚀 Fastest | ⏱️ Network latency |
| **Remote Access** | ❌ | ✅ |
| **Multiple Clients** | ❌ | ✅ |
| **Complexity** | 🟢 Simple | 🟠 Moderate |
| **Setup Time** | ⚡ Auto | 🔧 Manual |
| **Port Conflicts** | ❌ | ⚠️ Possible |
| **Security** | 🔒 Built-in | 🔐 Auth needed |

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'langchain'"

**Cause:** Dependencies not installed  
**Solution:**
```powershell
uv add -r requirements.txt
```

### Error: "GROQ_API_KEY environment variable not set"

**Cause:** Missing .env file or wrong key name  
**Solution:**
1. Create `.env` file in project root
2. Add: `GROQ_API_KEY=your_actual_key`
3. Get key from: https://console.groq.com/

### Error: "Cannot connect to weather server"

**Cause:** Weather server not running  
**Solution:**
```powershell
# Terminal 1
python weather.py

# Terminal 2 (in another terminal)
python client.py
```

### Error: "Weather response: Unfortunately, I can't verify the weather"

**Cause:** LLM not calling the weather tool  
**Solution:**
- Ensure weather.py is running (see above)
- Check for connection errors in weather.py terminal
- The client prompt already guides the LLM to use the tool

---

## Why MCP vs FastAPI?

### FastAPI Approach
```python
@app.get("/add")
def add(a: int, b: int):
    return a + b
```

**Model perspective:**
- ❓ What endpoints exist?
- ❓ What parameters do they need?
- ❓ How are errors communicated?
- Requires custom prompting to explain all this

### MCP Approach
```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

**Model perspective:**
- ✅ Tool "add" exists with parameters a, b (both int)
- ✅ Returns int
- ✅ Has automatic documentation
- ✅ No prompting needed—uses standardized protocol

---

## Key Concepts

### Tool Schema
Each MCP tool automatically provides:
- **Name:** Function identifier
- **Description:** Natural language explanation
- **Parameters:** Type-defined inputs with descriptions
- **Return Type:** Expected output type
- **Validation:** Parameter checking

### Multi-Server Architecture
- Each MCP server manages its own domain
- Client aggregates all tools into one interface
- Servers can be deployed independently
- Tools are automatically discovered via introspection

### Agent Orchestration
LangGraph agents can:
- Detect available tools
- Call tools in sequence
- Remember tool results
- Use results for subsequent calls
- Handle errors gracefully

---

## Learning Outcomes

After completing this project, you'll understand:

✅ What MCP is and why it's important for AI integration  
✅ How to build MCP servers with FastMCP  
✅ Difference between Stdio and HTTP transports  
✅ Building AI agents that use multiple tools  
✅ Multi-server architecture and coordination  
✅ Tool schemas and automatic discovery  
✅ Effective prompting for reliable tool usage  

---

## Next Steps & Ideas

1. **Add More Tools:** Database queries, file operations, external APIs
2. **Deploy to Cloud:** Push weather server to AWS/GCP
3. **Add Authentication:** Secure the HTTP server
4. **Web Interface:** Build dashboard for agent interactions
5. **Custom Error Handling:** Implement retry logic
6. **Claude Desktop Integration:** Connect to Claude via MCP
7. **Performance Monitoring:** Add logging and metrics
8. **Tool Composition:** Chain multiple servers for complex workflows

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP (Python)](https://github.com/modelcontextprotocol/python-sdk)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Groq API Docs](https://console.groq.com/docs)
- [Claude Desktop with MCP](https://modelcontextprotocol.io/clients/claude-desktop)

---

## License

MIT#   M C P - B a s i c s  
 