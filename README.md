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

## Deployment

### Building the Container

Build the container image using Podman (or Docker):

```bash
podman build -t adk-agent-playground:latest .
```

### Running the Container

Run the container with the required environment variables:

```bash
podman run --rm -it -p 8080:8080 -e PORT=8080 -e GMP_API_KEY=your_api_key_here adk-agent-playground:latest
```

Or use a different port:

```bash
podman run --rm -it -p 3000:3000 -e PORT=3000 -e GMP_API_KEY=your_api_key_here adk-agent-playground:latest
```

**Note:** Make sure to replace `your_api_key_here` with your actual Google Maps Platform API key.

## Future Agents

More agents will be added as experiments continue.
