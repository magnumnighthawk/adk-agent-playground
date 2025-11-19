# Agent Playground

A playground project for experimenting with Google ADK (Agent Development Kit) and building various AI agents using its Python library.

## Current Agents

### Simple Weather Agent
Returns weather information for the user's current location using Google Maps Geocoding API and Google Weather API.

**Features:**
- Fetches user location details (city, country, coordinates)
- Retrieves current weather conditions
- Provides friendly, formatted weather summaries

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Google API key:
   ```
   GMP_API_KEY=your_api_key_here
   ```

4. Run the agent:
   ```bash
   adk web --port 3000
   ```

## Project Structure

```
agent_playground/
├── simple_agent/
│   ├── agent.py          # Weather agent implementation
│   └── instructions.py   # Agent behavior instructions
├── requirements.txt
└── .env                  # API credentials (not tracked)
```

## Future Agents

More agents will be added as experiments continue.
