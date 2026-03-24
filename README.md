# Multi-Agent System with LangGraph

A flexible, modular multi-agent system built with LangChain and LangGraph. Features intelligent agent routing, conversation memory, MCP server integration, and a modern web interface with real-time streaming.

## Architecture

The system follows a supervisor-agent pattern where a central supervisor routes requests to specialized agents:

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend (Web UI)                    │
│                    • Real-time streaming chat                │
│                    • Markdown rendering                      │
│                    • Agent status indicators                 │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP/Streaming
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  FastAPI Backend Server                      │
│             • RESTful API endpoints                          │
│             • Plain text streaming                           │
│             • CORS enabled                                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  Supervisor (LangGraph)                      │
│        • Analyzes user requests                              │
│        • Routes to appropriate agent                         │
│        • Maintains conversation memory                       │
│        • Returns streaming responses                         │
└────────────────────────┬─────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    File      │  │   Research   │  │   Weather    │
│ Operations   │  │    Agent     │  │    Agent     │
│              │  │              │  │              │
│ • Read files │  │ • Web search │  │ • MCP Server │
│ • Write files│  │ • Summarize  │  │ • Dynamic    │
│ • List dirs  │  │ • Analyze    │  │   tools      │
│ • Tool exec  │  │ • DuckDuckGo │  │ • Weather    │
└──────────────┘  └──────────────┘  └──────────────┘
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │ MCP Weather  │
                                    │    Server    │
                                    │ (External)   │
                                    └──────────────┘
```

### Key Components:

- **Frontend**: Single-page application with streaming chat interface
- **Backend**: FastAPI server with streaming endpoints
- **Supervisor**: LangGraph workflow for intelligent routing
- **Agents**: Specialized agents with unique capabilities
- **MCP Integration**: External tool servers via Model Context Protocol
- **Agent Registry**: Automatic agent discovery and registration

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Modern web browser

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment**:
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Install MCP Weather Server** (optional, for weather agent):
```bash
pip install mcp-weather-server
```

## Running the System

### Backend Server

Start the FastAPI backend server:

```bash
cd src
python api_server.py
```

The server will start on `http://127.0.0.1:8000`

**Server endpoints:**
- `GET /health` - Health check
- `GET /agents` - List all registered agents
- `POST /chat` - Non-streaming chat endpoint
- `POST /stream` - Streaming chat endpoint (recommended)

### Frontend

Open the frontend in your browser:

```bash
open frontend/index.html
```

Or simply double-click `frontend/index.html` in your file browser.

The frontend will automatically connect to the backend at `http://127.0.0.1:8000`

### CLI Mode (Alternative)

For command-line usage without the web interface:

```bash
python src/main.py
```

## Usage

Once both backend and frontend are running:

1. Open `frontend/index.html` in your browser
2. Type your message in the input box
3. Watch the response stream in real-time
4. The active agent will be highlighted in the right sidebar

**Example queries:**
- "What's the weather in London?"
- "List all files in the current directory"
- "Search for information about LangGraph"
- "Create a file called notes.txt with hello world"

## Project Structure

```
agent-builder/
├── src/
│   ├── core/                       # Core framework
│   │   ├── base_agent.py           # BaseAgent abstract class
│   │   ├── agent_registry.py       # Agent registration system
│   │   ├── state.py                # State schema with conversation memory
│   │   ├── supervisor.py           # LangGraph supervisor
│   │   └── mcp_client.py           # MCP client for external tools
│   ├── agents/                     # Agent implementations
│   │   ├── file_operations_agent.py
│   │   ├── research_agent.py
│   │   └── weather_agent.py
│   ├── api_server.py               # FastAPI backend server
│   └── main.py                     # CLI entry point
├── frontend/
│   └── index.html                  # Web UI (HTML + CSS + JS)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create this)
└── README.md                       # This file
```

## Available Agents

### 1. File Operations Agent
Handles file system operations using LangChain tools.

**Capabilities**: Read files, write files, list directories, move files, append to files

### 2. Research Agent
Performs web searches and information gathering using DuckDuckGo.

**Capabilities**: Web search, content summarization, information extraction, topic analysis

### 3. Weather Agent
Provides weather information via MCP server integration (demonstrates external tool usage).

**Capabilities**: Dynamically loaded from MCP server (current weather, forecasts, air quality, timezone info, etc.)

## Features

- ✅ **Intelligent Routing**: Supervisor automatically selects the best agent
- ✅ **Real-time Streaming**: Responses stream word-by-word to the frontend
- ✅ **Conversation Memory**: Maintains context across multiple messages
- ✅ **Markdown Support**: Rich text formatting in responses
- ✅ **MCP Integration**: Connect to external tool servers
- ✅ **Modular Design**: Easy to add new agents
- ✅ **Modern UI**: Clean, responsive web interface with dark mode
- ✅ **Agent Status**: Visual indicators show which agent is active

## Tech Stack

- **Backend**: FastAPI, LangChain, LangGraph, OpenAI
- **Frontend**: Vanilla JavaScript, HTML5, CSS3, Marked.js
- **Streaming**: Plain text streaming (StreamingResponse)
- **MCP**: Model Context Protocol for external tools
- **State Management**: LangGraph MemorySaver for conversation history

---

**Built with LangChain & LangGraph 🤖**
