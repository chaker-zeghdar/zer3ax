# Python Chatbot Configuration

Complete Python implementation of the Zer3aZ chatbot with independent prompt and tools configuration.

## 📁 Project Structure

```
zer3ax/
├── src/
│   ├── config/
│   │   ├── chatbot_prompt.py      # System prompt & personality
│   │   └── chatbot_tools.py       # Tool functions & registry
│   ├── services/
│   │   └── ai_service.py          # AI integration (OpenAI, Claude)
│   └── api/
│       └── chatbot_api.py         # Flask REST API
└── python-chatbot/
    ├── requirements.txt           # Python dependencies
    └── README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd zer3ax

# Install Python dependencies
pip install -r python-chatbot/requirements.txt
```

### 2. Run the API Server

```bash
# Run the Flask API
python src/api/chatbot_api.py
```

The API will be available at: `http://localhost:5000`

### 3. Test the API

```bash
# Test the chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "search wheat"}'

# Get chatbot configuration
curl http://localhost:5000/api/config

# List available tools
curl http://localhost:5000/api/tools
```

## 📚 File Descriptions

### 1. `chatbot_prompt.py` - Configuration

Contains all chatbot personality and prompt settings:

```python
from config.chatbot_prompt import chatbot_config, get_response_template

# Get the system prompt
system_prompt = chatbot_config["system_prompt"]

# Get initial greeting
greeting = chatbot_config["initial_greeting"]

# Get a response template
template = get_response_template("hybridization_question")
```

**What you can customize:**
- System prompt
- Initial greeting
- Personality settings (name, tone, expertise)
- Response templates
- Platform context

### 2. `chatbot_tools.py` - Tools & Functions

Defines all available tools the chatbot can use:

```python
from config.chatbot_tools import execute_tool, chatbot_tools

# Execute a tool
results = execute_tool("search_plants", query="wheat")

# Get all tools
all_tools = chatbot_tools

# Access a specific tool
search_tool = chatbot_tools["search_plants"]
```

**Available Tools:**
- `search_plants(query)` - Search for plants
- `get_plant_details(plant_id)` - Get plant details
- `calculate_trait_similarity(plant_a, plant_b)` - Compare traits
- `get_plants_by_zone(zone)` - Filter by zone
- `predict_hybridization(plant_a_id, plant_b_id)` - Predict success
- `get_zone_statistics(zone)` - Get zone stats
- `get_recommendations(criteria)` - Get recommendations

### 3. `ai_service.py` - AI Integration

Provides integration with AI services:

```python
from services.ai_service import OpenAIService, AnthropicService, simple_chat_response

# Simple rule-based (no API needed)
response = simple_chat_response("Tell me about wheat")

# OpenAI integration (requires API key)
openai_service = OpenAIService()
response = await openai_service.chat("Tell me about wheat")

# Anthropic Claude integration (requires API key)
claude_service = AnthropicService()
response = await claude_service.chat("Tell me about wheat")
```

### 4. `chatbot_api.py` - REST API

Flask API for the chatbot:

**Endpoints:**
- `POST /api/chat` - Send messages
- `GET /api/config` - Get configuration
- `GET /api/tools` - List tools
- `POST /api/tool/<name>` - Execute a tool
- `GET /api/health` - Health check

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Using with AI Services

#### OpenAI Integration

1. Install OpenAI SDK:
```bash
pip install openai
```

2. Set API key in `.env`:
```bash
OPENAI_API_KEY=sk-...
```

3. Uncomment OpenAI code in `ai_service.py`

4. Use in your code:
```python
from services.ai_service import get_ai_service

ai = get_ai_service("openai")
response = await ai.chat("How do I cross wheat and barley?")
```

#### Anthropic Claude Integration

1. Install Anthropic SDK:
```bash
pip install anthropic
```

2. Set API key in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

3. Uncomment Claude code in `ai_service.py`

4. Use in your code:
```python
from services.ai_service import get_ai_service

ai = get_ai_service("anthropic")
response = await ai.chat("What plants grow in the Sahara?")
```

## 🎯 Usage Examples

### Example 1: Customize the Prompt

Edit `src/config/chatbot_prompt.py`:

```python
chatbot_config = {
    "system_prompt": """You are AgriBot, a friendly agricultural assistant...""",
    "initial_greeting": "Hey there! Ready to talk plants?",
    "personality": {
        "name": "AgriBot",
        "tone": "casual and fun",
        "expertise": "agriculture",
        "response_style": "simple and direct"
    }
}
```

### Example 2: Add a New Tool

Edit `src/config/chatbot_tools.py`:

```python
def get_weather_forecast(zone: str) -> Dict[str, Any]:
    """Get weather forecast for a zone."""
    # Your implementation
    return {"zone": zone, "forecast": "sunny"}

# Register the tool
chatbot_tools["get_weather_forecast"] = {
    "name": "get_weather_forecast",
    "description": "Get weather forecast for a climate zone",
    "parameters": {
        "zone": {"type": "string", "description": "Climate zone"}
    },
    "execute": get_weather_forecast
}
```

### Example 3: Connect React Frontend

Update your React `Chatbot.jsx` to call the Python API:

```javascript
const handleSend = async () => {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: inputValue,
      conversation_history: messages
    })
  });
  
  const data = await response.json();
  // Add bot response to messages
  setMessages([...messages, {
    type: 'bot',
    text: data.response,
    timestamp: new Date().toLocaleTimeString()
  }]);
};
```

## 🧪 Testing

### Test Tools Directly

```python
# test_tools.py
from config.chatbot_tools import execute_tool

# Test search
results = execute_tool("search_plants", query="wheat")
print(f"Found {len(results)} plants")

# Test zone statistics
stats = execute_tool("get_zone_statistics", zone="Northern")
print(f"Zone has {stats['plant_count']} plants")

# Test prediction
prediction = execute_tool("predict_hybridization", plant_a_id=1, plant_b_id=2)
print(f"Success rate: {prediction['success_rate']}%")
```

### Test API Endpoints

```python
# test_api.py
import requests

# Test chat
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'search for wheat'
})
print(response.json())

# Test config
config = requests.get('http://localhost:5000/api/config')
print(config.json())
```

## 🔍 Troubleshooting

**Import errors:**
- Make sure you're running from the correct directory
- Check that `src` is in your Python path

**API not responding:**
- Verify Flask is running: `python src/api/chatbot_api.py`
- Check the port (default: 5000) isn't in use

**AI service errors:**
- Verify API keys are set in `.env`
- Check that SDK is installed (`pip install openai` or `pip install anthropic`)
- Uncomment the integration code in `ai_service.py`

## 📖 Best Practices

1. **Separation of Concerns**
   - Keep prompts in `chatbot_prompt.py`
   - Keep tools in `chatbot_tools.py`
   - Keep AI logic in `ai_service.py`

2. **Type Hints**
   - Use Python type hints for better code clarity
   - Document all functions with docstrings

3. **Error Handling**
   - Always handle API errors gracefully
   - Provide fallback responses

4. **Testing**
   - Test tools independently
   - Test API endpoints
   - Test with different prompts

## 🚀 Deployment

### Deploy with Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
ENV FLASK_APP=src/api/chatbot_api.py

CMD ["python", "src/api/chatbot_api.py"]
```

Build and run:
```bash
docker build -t zer3a-chatbot .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key zer3a-chatbot
```

### Deploy to Cloud

The Flask API can be deployed to:
- **Heroku**: `heroku create && git push heroku main`
- **AWS Lambda**: Use Zappa or Serverless Framework
- **Google Cloud Run**: Deploy as a container
- **Azure App Service**: Deploy Python web app

## 📝 License

This chatbot configuration is part of the Zer3aZ project.

## 🤝 Contributing

To add new features:
1. Add tools to `chatbot_tools.py`
2. Update prompts in `chatbot_prompt.py`
3. Add API endpoints in `chatbot_api.py`
4. Update this README with examples
