# Google Gemini AI Integration - Quick Start Guide

Your Zer3aZ chatbot is now powered by **Google Gemini AI** with your API key pre-configured!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies including Gemini SDK
pip install -r python-chatbot/requirements.txt
```

### 2. Verify Installation

```bash
# Test that Gemini is installed
python -c "import google.generativeai as genai; print('✓ Gemini SDK installed successfully!')"
```

### 3. Start the API Server

```bash
python src/api/chatbot_api.py
```

You should see:
```
✓ Gemini AI service initialized successfully
Starting Zer3aZ Chatbot API...
API available at: http://localhost:5000
```

## 🧪 Test the Integration

### Test 1: Simple Chat

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about wheat and barley hybridization"
  }'
```

### Test 2: Generate Detailed Report

```bash
curl -X POST http://localhost:5000/api/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "plant_a_id": 1,
    "plant_b_id": 2
  }'
```

### Test 3: Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Zer3aZ Chatbot API",
  "gemini_available": true
}
```

## 📊 API Endpoints

### POST /api/chat
Send chat messages to Gemini AI

**Request:**
```json
{
  "message": "How can I improve drought resistance in wheat?",
  "conversation_history": [
    {"type": "user", "text": "Previous message"},
    {"type": "bot", "text": "Previous response"}
  ]
}
```

**Response:**
```json
{
  "response": "AI-generated response...",
  "success": true,
  "service": "Gemini AI"
}
```

### POST /api/generate-report
Generate comprehensive breeding analysis reports

**Request:**
```json
{
  "plant_a_id": 1,
  "plant_b_id": 2
}
```

**Response:**
```json
{
  "report": "Detailed markdown report...",
  "success": true,
  "service": "Gemini AI"
}
```

### GET /api/config
Get chatbot configuration

### GET /api/tools
List available tools

### GET /api/health
Health check and service status

## 🎯 Key Features

### 1. **Advanced System Prompt**
Your chatbot now has an expert-level system prompt that:
- Specializes in genetic analysis and trait improvement
- Generates detailed breeding reports
- Provides scientific explanations with confidence levels
- Offers actionable recommendations

### 2. **Comprehensive Report Generation**
Generate detailed reports that include:
- Executive Summary
- Parent Species Analysis
- Trait Compatibility Analysis
- Hybridization Predictions
- F1 Characteristics
- Improvement Recommendations (short-term & long-term)
- Environmental Adaptability Assessment
- Risk Assessment with mitigation strategies

### 3. **Smart Tool Integration**
The chatbot can:
- Search plant databases
- Calculate trait similarities
- Predict hybridization success
- Analyze climate zones
- Generate recommendations

## 🔧 Configuration

### Your API Key
Pre-configured in [ai_service.py](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/services/ai_service.py):
```python
GEMINI_API_KEY = "AIzaSyD1sB4FJqCSLu1sCdnmEcyAEsMxJV80jPw"
```

### Modify System Prompt
Edit [chatbot_prompt.py](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/config/chatbot_prompt.py):
```python
chatbot_config = {
    "system_prompt": """Your custom prompt here...""",
    # ... rest of config
}
```

### Add New Tools
Edit [chatbot_tools.py](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/config/chatbot_tools.py):
```python
def your_new_tool(params):
    # Implementation
    return result

chatbot_tools["your_tool"] = {
    "name": "your_tool",
    "description": "What it does",
    "parameters": {...},
    "execute": your_new_tool
}
```

## 📱 Connect React Frontend

Update your React [Chatbot.jsx](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/pages/Chatbot.jsx):

```javascript
const handleSend = async () => {
  if (!inputValue.trim()) return;

  // Add user message
  const userMessage = {
    type: 'user',
    text: inputValue,
    timestamp: new Date().toLocaleTimeString()
  };
  setMessages([...messages, userMessage]);
  setInputValue('');

  try {
    // Call Gemini-powered API
    const response = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage.text,
        conversation_history: messages
      })
    });

    const data = await response.json();

    // Add bot response
    const botMessage = {
      type: 'bot',
      text: data.response,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, botMessage]);
    
  } catch (error) {
    console.error('Chat error:', error);
  }
};
```

### Generate Report Button

```javascript
const generateReport = async (plantAId, plantBId) => {
  try {
    const response = await fetch('http://localhost:5000/api/generate-report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        plant_a_id: plantAId,
        plant_b_id: plantBId
      })
    });

    const data = await response.json();
    console.log('Report:', data.report);
    
    // Display the report in your UI
    setReport(data.report);
    
  } catch (error) {
    console.error('Report generation error:', error);
  }
};
```

## 🎨 Example Prompts to Try

1. **Simple Query:**
   "What plants are suitable for the Northern zone?"

2. **Trait Analysis:**
   "Analyze the drought resistance characteristics in wheat varieties"

3. **Hybridization Prediction:**
   "What would be the result of crossing wheat and barley?"

4. **Improvement Recommendations:**
   "How can I improve the yield of wheat in the High Plateau zone?"

5. **Report Generation:**
   "Generate a detailed breeding report for crossing plant ID 1 with plant ID 2"

## 🛠️ Troubleshooting

### Error: "Gemini service not available"
```bash
# Install the SDK
pip install google-generativeai

# Verify installation
python -c "import google.generativeai as genai; print('OK')"
```

### Error: "API key invalid"
- Check that your API key is correct in `.env` or `ai_service.py`
- Verify at: https://makersuite.google.com/app/apikey

### Rate Limiting
If you hit rate limits, Gemini will return an error. Wait a few seconds and retry.

## 📚 Next Steps

1. **Test the chatbot** with various queries
2. **Generate sample reports** for different plant combinations
3. **Customize the prompt** for your specific use case
4. **Add more tools** for additional functionality
5. **Connect your React frontend** to the API

## 🔐 Security Note

Your API key is currently hardcoded. For production:
1. Move it to environment variables
2. Never commit API keys to version control
3. Use proper secret management

```bash
# Add to .env file
GEMINI_API_KEY=your_key_here

# Load in Python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

## 📞 Support

- Gemini API Documentation: https://ai.google.dev/docs
- Zer3aZ Chatbot Config: [src/config/](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/config/)
- AI Service: [src/services/ai_service.py](file:///Users/mohamedilyeshaddef/zer3a.../zer3ax/src/services/ai_service.py)

---

**Ready to go! 🚀** Your chatbot is now powered by Google Gemini AI with advanced breeding analysis capabilities.
