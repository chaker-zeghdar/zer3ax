# 🤖 Clean Chatbot v2 - From Scratch

A modular, production-ready AI chatbot supporting **Claude**, **Gemini**, and **OpenAI** with easy customization.

## 📁 File Structure

```
chatbot_v2/
├── config.py       # Configuration (API keys, prompts, settings)
├── tools.py        # Custom tools/functions for the chatbot
├── chatbot.py      # Core chatbot implementation
├── api.py          # Flask REST API
└── README.md       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install required packages
pip install anthropic google-generativeai openai flask flask-cors

# Or use requirements file (if created)
pip install -r requirements.txt
```

### 2. Configure Your Chatbot

Edit `config.py`:

```python
# Set your API key
API_KEY = "your-api-key-here"

# Or use environment variable
export CHATBOT_API_KEY="your-api-key-here"

# Choose AI service
AI_SERVICE = "claude"  # or "gemini" or "openai"
```

### 3. Customize the System Prompt

Edit the `SYSTEM_PROMPT` in `config.py`:

```python
SYSTEM_PROMPT = """You are a specialized AI assistant for [YOUR DOMAIN].

YOUR EXPERTISE:
- [Expertise area 1]
- [Expertise area 2]

YOUR KNOWLEDGE BASE:
[Add your domain-specific data here]
"""
```

### 4. Add Custom Tools

Edit `tools.py` to add your custom functions:

```python
@tool_registry.register(
    name="search_database",
    description="Search your custom database",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    }
)
def search_database(query: str) -> dict:
    # Your custom implementation
    results = your_database.search(query)
    return results
```

### 5. Run the Chatbot

**Option A: Command Line**
```bash
python chatbot.py
```

**Option B: API Server**
```bash
python api.py
```

## 🎯 API Endpoints

### Health Check
```bash
GET /api/health
```

### Send Message
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "user-123",
  "conversation_history": []  # optional
}
```

### Reset Conversation
```bash
POST /api/reset
Content-Type: application/json

{
  "session_id": "user-123"
}
```

### Get History
```bash
GET /api/history?session_id=user-123
```

## ⚙️ Configuration Options

### Model Settings (`config.py`)

```python
MODELS = {
    "claude": {
        "model_name": "claude-3-5-sonnet-20241022",
        "max_tokens": 2048,
        "temperature": 0.7,
    },
    # ... customize other models
}
```

### Chatbot Settings

```python
SETTINGS = {
    "chat_history_limit": 10,   # Messages to keep
    "streaming": False,          # Enable streaming
    "enable_tools": True,        # Enable function calling
    "debug_mode": True,          # Debug output
}
```

## 🛠️ Customization Guide

### 1. Change API Service

```python
# In config.py
AI_SERVICE = "gemini"  # Switch to Gemini
```

### 2. Add Domain Knowledge

```python
# In config.py
SYSTEM_PROMPT = f"""You are an expert in plant breeding.

PLANT DATABASE:
{plant_data}

CLIMATE ZONES:
{zone_data}

Answer questions using this data."""
```

### 3. Enable Tools

```python
# In config.py
SETTINGS = {
    "enable_tools": True,  # Turn on function calling
}

# In tools.py - add your tools
@tool_registry.register(...)
def your_custom_tool():
    pass
```

### 4. Customize Error Messages

```python
# In config.py
ERROR_MESSAGES = {
    "api_error": "Custom error message",
    "rate_limit": "Custom rate limit message",
}
```

## 🔑 API Keys

### Claude (Anthropic)
```bash
export CHATBOT_API_KEY="sgamp_user_..."
AI_SERVICE = "claude"
```

### Gemini (Google)
```bash
export CHATBOT_API_KEY="AIzaSy..."
AI_SERVICE = "gemini"
```

### OpenAI
```bash
export CHATBOT_API_KEY="sk-..."
AI_SERVICE = "openai"
```

## 📊 Usage Examples

### Python Usage

```python
from chatbot import Chatbot

# Create chatbot
bot = Chatbot(api_key="your-key", service="claude")

# Chat
response = bot.chat("Hello!")
print(response)

# Get history
history = bot.get_history()

# Reset
bot.reset()
```

### API Usage (JavaScript/React)

```javascript
const response = await fetch('http://localhost:5001/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello!',
    session_id: 'user-123'
  })
});

const data = await response.json();
console.log(data.response);
```

## 🎨 Integration with Your Frontend

The chatbot is already compatible with your existing React frontend. Just update the API endpoint:

```javascript
// In your Chatbot.jsx or Predict.jsx
const API_URL = 'http://localhost:5001/api/chat';

const response = await fetch(API_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userMessage,
    conversation_history: messages
  })
});
```

## 🔒 Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Validate input** - Check user messages before processing
3. **Rate limiting** - Add rate limiting in production
4. **Session management** - Use proper session storage (Redis, DB)
5. **HTTPS** - Always use HTTPS in production

## 🐛 Troubleshooting

### Import Errors
```bash
pip install anthropic google-generativeai openai flask flask-cors
```

### API Key Not Found
```bash
# Set environment variable
export CHATBOT_API_KEY="your-key-here"

# Or hardcode in config.py (not recommended)
API_KEY = "your-key-here"
```

### Service Not Initialized
Check that you have the correct package installed for your chosen service.

## 📝 Next Steps

1. ✅ Set your API key in `config.py`
2. ✅ Customize `SYSTEM_PROMPT` for your domain
3. ✅ Add custom tools in `tools.py`
4. ✅ Run `python api.py` to start the server
5. ✅ Test with `curl` or your frontend

## 🎉 Features

- ✅ Multi-service support (Claude, Gemini, OpenAI)
- ✅ Tool/function calling
- ✅ Conversation history management
- ✅ Session-based chats
- ✅ Clean, modular architecture
- ✅ Easy customization
- ✅ REST API ready
- ✅ Production-ready error handling

---

**Made from scratch with ❤️ - Clean, simple, and powerful!**
