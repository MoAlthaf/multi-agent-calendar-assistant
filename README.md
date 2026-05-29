# ScheduleMe - Multi-Agent Google Calendar Assistant

A natural language calendar assistant powered by multiple specialized AI agents. Intelligently schedule meetings, check availability, edit events, and remove conflicts using conversational commands.

## Features

- **Intelligent Scheduling**: Schedule meetings with natural language
- **Availability Checking**: Check calendar availability before scheduling
- **Event Editing**: Modify existing calendar events with ease
- **Event Removal**: Delete or remove calendar conflicts
- **Multi-Agent Orchestration**: Supervisor agent routes requests to the best specialized agent
- **FastAPI Backend**: RESTful API for calendar operations
- **Streamlit UI**: User-friendly web interface

## Prerequisites

- Python 3.11+
- Google Account with Calendar API enabled
- OpenAI API key

## Setup Instructions

### 1. Clone and Install

```bash
git clone <repository-url>
cd ScheduleMe
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file and save it as `credentials.json` in the project root

### 5. Set Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
SCHEDULEME_API_URL=http://localhost:8000/api/v1
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 6. Run the Application

**Option A: Start FastAPI Backend + Streamlit UI**

```bash
# Terminal 1 - Start FastAPI backend
python main.py

# Terminal 2 - Start Streamlit UI
streamlit run ui/streamlit_app.py
```

**Option B: FastAPI Only**

```bash
python main.py
```

Access the API at `http://localhost:8000` and Swagger docs at `http://localhost:8000/docs`

## Usage

### Via Streamlit UI
- Open `http://localhost:8501` in your browser
- Type your calendar request in natural language
- Examples:
  - "Schedule a meeting with John next Monday at 2 PM"
  - "Check if I'm free on Wednesday"
  - "Move my 3 PM meeting to 4 PM"
  - "Remove the conflict on Friday"

### Via API
Send POST requests to `/api/v1/invoke` with your calendar request and thread ID.

## Project Structure

```
ScheduleMe/
├── agents/                      # Specialized AI agents
│   ├── supervisor_agent.py      # Routes requests to appropriate agent
│   ├── scheduler_agent.py       # Schedules new events
│   ├── availability_checking_agent.py  # Checks availability
│   ├── editing_agent.py         # Modifies events
│   └── removal_agent.py         # Deletes events
├── api/
│   └── routes.py               # FastAPI routes
├── graph/
│   └── workflow.py             # LangGraph workflow orchestration
├── tools/
│   └── calendar_tools.py       # Google Calendar API wrapper
├── schemas/
│   └── schemas.py              # Data models
├── prompts/
│   └── prompts.py              # Agent prompts
├── ui/
│   └── streamlit_app.py        # Web interface
├── test/                        # Unit tests
└── main.py                      # FastAPI app entry point
```

## How It Works

1. **User Input**: Request is sent via Streamlit UI or API
2. **Supervisor Agent**: Routes the request to the appropriate specialized agent
3. **Specialized Agent**: Processes the request (schedule/check/edit/remove)
4. **Calendar Tools**: Interacts with Google Calendar API
5. **Response**: Returns result to user

## Getting API Keys

### OpenAI API Key
1. Sign up at [OpenAI](https://openai.com)
2. Go to [API Keys](https://platform.openai.com/account/api-keys)
3. Create a new API key and add it to `.env`

### Google Calendar API Token
- The app handles OAuth flow automatically on first run
- You'll be redirected to Google login
- Grant calendar permissions
- Token is saved as `token.json` for future use

## Troubleshooting

- **"credentials.json not found"**: Download it from Google Cloud Console (see Setup step 4)
- **"No module named 'langchain'"**: Ensure virtual environment is activated and dependencies are installed
- **API connection errors**: Check that FastAPI server is running on `http://localhost:8000`

## Requirements

See `pyproject.toml` for full dependency list:
- LangChain & LangGraph (Agent framework)
- Google API Client (Calendar integration)
- OpenAI (LLM)
- FastAPI (Backend)
- Streamlit (UI)

## License

MIT

---

For issues or contributions, please refer to the project repository.
