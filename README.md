# ✈️ TripMate AI — Multi-Agent Travel Planning System

<p align="center">
  <strong>An intelligent, multi-agent travel planner powered by LangGraph, MCP, and Human-in-the-Loop orchestration.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/MCP-Tool%20Integration-purple" alt="MCP"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Checkpointing-4169E1?logo=postgresql" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Status-Development-orange" alt="Development"/>
</p>

## 🌍 Overview

**TripMate AI** is a multi-agent travel planning application that transforms natural-language travel requests into structured, budget-aware travel plans.

Instead of relying on a single AI agent to handle every task, TripMate AI uses a **Supervisor-driven architecture** built with LangGraph. The Supervisor evaluates incoming requests, applies input guardrails, identifies relevant travel tasks, and coordinates specialized agents.

The system integrates external capabilities through the **Model Context Protocol (MCP)** and introduces a **Human-in-the-Loop (HITL)** approval stage, allowing users to review and approve a proposed itinerary before the workflow generates the final travel plan.

The goal is to demonstrate how multiple specialized AI agents, external tools, state management, and human feedback can work together in a practical AI application.

## ✨ Key Features

### 🧠 1. Supervisor-Based Multi-Agent Orchestration
- A central Supervisor coordinates the travel-planning workflow.
- Evaluates incoming requests using an input guardrail.
- Determines which specialized agents are relevant.
- Extracts and maintains trip constraints.
- Uses conditional routing to coordinate agent execution.

### 🛡️ 2. Input Guardrails
- Validates whether a request is related to travel planning.
- Identifies unrelated or inappropriate requests.
- Prevents requests rejected by the guardrail from proceeding through the normal travel workflow.

### ✈️ 3. Specialized Travel Agents

| Agent | Responsibility |
|---|---|
| Flight Agent | Retrieves aviation-related information and generates flight guidance. |
| Hotel Agent | Searches for accommodation information using Tavily MCP. |
| Weather Agent | Retrieves current weather and forecast information through a custom Weather MCP server. |
| Budget Agent | Evaluates estimated trip expenses, budget risks, and cost-saving opportunities. |
| Itinerary Agent | Combines travel information into a structured, practical itinerary. |

### 🔌 4. MCP-Based External Tool Integration

TripMate AI uses MCP to connect its agents with external tools and services.

- **Tavily MCP:** Travel-related web search and accommodation research.
- **AviationStack MCP:** Aviation and flight-related information.
- **Custom Weather MCP Server:** Current weather and forecast retrieval.

This architecture separates external tool access from the agent orchestration logic.

### 👤 5. Human-in-the-Loop (HITL)

TripMate AI introduces a human approval checkpoint before generating the final travel plan.

1. The Itinerary Agent generates a draft.
2. LangGraph pauses execution using `interrupt()`.
3. The draft is presented to the user.
4. The user can approve the itinerary or request revisions with feedback.
5. The workflow resumes using the existing conversation thread.
6. The Final Agent generates the final response.

This makes the workflow reviewable rather than automatically treating every AI-generated itinerary as approved.

### 💾 6. Persistent Workflow State

- Uses LangGraph checkpointing with PostgreSQL.
- Maintains workflow state across execution and approval stages.
- Uses thread IDs to identify individual travel-planning workflows.
- Supports resuming interrupted workflows through saved checkpoints.

### 🖥️ 7. Interactive Web Application

- FastAPI-powered backend.
- Browser-based travel request interface.
- Supervisor execution details and selected-agent information.
- Draft itinerary review and approval interface.
- Final travel plan presentation.
- Copy and PDF export functionality.

## 🏗️ System Architecture

The following diagram illustrates the main workflow:

```mermaid
flowchart TD
    A["User Travel Request"] --> B["FastAPI Application"]
    B --> C["Supervisor Agent"]
    C --> D{"Input Guardrail"}
    D -->|Rejected| E["Guardrail Response"]
    D -->|Allowed| F["Agent Selection & Routing"]

    F --> G["Flight Agent"]
    F --> H["Hotel Agent"]
    F --> I["Weather Agent"]

    G --> J["Budget Agent"]
    H --> J
    I --> J

    J --> K["Itinerary Agent"]
    K --> L["Draft Itinerary"]
    L --> M{"Human Approval"}

    M -->|Approve| N["Final Agent"]
    M -->|Request Revision| O["Human Feedback"]
    O --> N

    N --> P["Final Travel Plan"]

    Q["Tavily MCP"] -.-> H
    R["AviationStack MCP"] -.-> G
    S["Custom Weather MCP"] -.-> I

    T[("PostgreSQL Checkpointer")] -.-> C
    T -.-> M
    T -.-> N
```

*Note: The graph illustrates the major workflow stages and integrations. Actual agent execution follows the Supervisor's selected-agent routing and the graph's configured transitions.*

## 🔄 How It Works

**Step 1 — User Request**

The user enters a natural-language request, for example:

> Plan a 7-day Thailand trip from Bangladesh with budget hotels and sightseeing.

**Step 2 — Supervisor and Guardrails**

The Supervisor evaluates the request, checks whether it belongs to the travel-planning domain, and determines the relevant agents.

**Step 3 — Specialized Agent Execution**

Selected agents gather flight, accommodation, and weather information. The Budget Agent evaluates estimated costs and feasibility.

**Step 4 — Itinerary Generation**

The Itinerary Agent combines the available information and produces a structured draft.

**Step 5 — Human Review**

The workflow pauses at the HITL checkpoint. The user reviews the draft and either approves it or supplies revision feedback.

**Step 6 — Final Response**

After approval, the workflow resumes and the Final Agent produces the final travel plan.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Model Provider | Groq |
| Tool Integration | Model Context Protocol (MCP) |
| Flight Information | AviationStack MCP |
| Web Search | Tavily MCP |
| Weather Information | Custom Weather MCP Server |
| Database | PostgreSQL |
| Workflow Persistence | LangGraph PostgreSQL Checkpointer |
| Frontend | HTML, CSS, JavaScript |
| Development Environment | VS Code, Conda |

## 📁 Project Structure

```text
Plan_My_Trip---MultiAgent-AI-Travel-Planner/
│
├── app.py
│   └── FastAPI application and API endpoints
│
├── backend.py
│   └── LangGraph workflow, Supervisor, agents,
│       guardrails, HITL, and checkpointing
│
├── mcp_client.py
│   └── MCP client configuration and tool helpers
│
├── custom_weather_mcp_server.py
│   └── Custom weather and forecast MCP server
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have:

- Python 3.11
- Git
- Conda or Python virtual environment
- PostgreSQL database
- Groq API key
- Tavily API key
- AviationStack API key
- OpenWeather API key
- `uv` / `uvx` for the AviationStack MCP server

### 1. Clone the Repository

```bash
git clone https://github.com/Purnima-nallamilli/Plan_My_Trip---MultiAgent-AI-Travel-Planner.git
```

```bash
cd Plan_My_Trip---MultiAgent-AI-Travel-Planner
```

### 2. Create and Activate the Environment

```bash
conda create -n travel python=3.11 -y
conda activate travel
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Install `uv` if it is not already available:

```bash
pip install uv
```

Verify:

```bash
uvx --version
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add the required configuration:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATION_STACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

Replace the example values with your own credentials.

**Security:** Never commit your `.env` file, API keys, or database credentials to GitHub.

### 5. Configure MCP Server Paths

The current MCP client implementation contains Windows-specific paths for the Python executable and custom weather server.

Before running the project on another machine, update these paths in `mcp_client.py` to match your local environment, or replace them with configurable environment variables.

Also ensure the required PostgreSQL database is accessible.

### 6. Run the Application

Start the FastAPI application from the project root:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open your browser:

```text
http://127.0.0.1:8000
```

You can now submit travel-planning requests through the TripMate AI interface.

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the travel planner web interface. |
| POST | `/api/travel` | Starts a new travel-planning workflow. |
| POST | `/api/travel/approve` | Resumes the workflow with approval or revision feedback. |
| GET | `/health` | Checks application health. |

### Example: Create a Travel Plan

**POST** `/api/travel`

```json
{
  "message": "Plan a 7-day Thailand trip from Bangladesh with budget hotels and sightseeing.",
  "thread_id": null
}
```

### Example: Approve a Draft

**POST** `/api/travel/approve`

```json
{
  "thread_id": "your-existing-thread-id",
  "approved": true,
  "feedback": ""
}
```

To request revisions, set `approved` to `false` and provide feedback.

## 🧪 Example Prompts

Try these requests in the application:

**Budget Travel**

> Plan a 5-day Thailand trip from Bangladesh with budget hotels and sightseeing.

**International Travel**

> Plan a 7-day Japan trip with flight guidance, weather information, accommodation suggestions, and a daily itinerary.

**Budget Analysis**

> Plan a 4-day Dubai trip within a limited budget and suggest ways to reduce expenses.

**Travel Research**

> Help me plan a trip to Singapore and include flight information, accommodation, weather, and sightseeing recommendations.

## 🔐 Engineering Highlights

This project demonstrates practical concepts used in modern AI application development:

- Stateful multi-agent orchestration with LangGraph.
- Supervisor-based agent selection and conditional routing.
- Input validation using guardrail logic.
- External tool integration through MCP.
- Persistent workflow execution using PostgreSQL checkpointing.
- Interrupt-driven Human-in-the-Loop approval.
- Thread-based workflow resumption.
- REST API development using FastAPI.
- Separation of orchestration, integrations, backend, and frontend responsibilities.

## ⚠️ Limitations and Notes

- Travel costs and airfare guidance should be treated as estimates unless verified against a booking provider.
- Search results and external API responses depend on service availability and API limits.
- The application provides travel planning and recommendations; it does not itself complete flight or hotel bookings.
- API credentials and PostgreSQL configuration are required for the relevant integrations.
- MCP server paths must be configured for the machine running the application.
- AI-generated information should be independently verified before making travel or financial decisions.

## 🚀 Future Enhancements

Potential improvements include:

- Live flight and hotel availability integrations.
- Interactive maps and route optimization.
- Multi-destination itinerary planning.
- Currency conversion and detailed budget breakdowns.
- User authentication and saved trip history.
- Automated itinerary PDF generation with richer formatting.
- Unit and integration tests for individual agents and graph execution.
- Cloud deployment with environment-based configuration.
- Improved observability, retry handling, and workflow monitoring.

## 👩‍💻 Author

**Purnima Nallamilli**

B.Tech — Information Technology

Interested in AI Engineering, Multi-Agent Systems, Cloud Computing, and Backend Development.

- GitHub: [@Purnima-nallamilli](https://github.com/Purnima-nallamilli)
- Project Repository: [TripMate AI](https://github.com/Purnima-nallamilli/Plan_My_Trip---MultiAgent-AI-Travel-Planner)

---

<p align="center">
  <strong>Built with Python, LangGraph, MCP, and a human-centered approach to AI.</strong>
</p>
