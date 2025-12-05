# Claude AI Integration Setup

## 🎯 Overview

The chatbot now supports **Claude AI (Anthropic)** as the primary intelligent response system, with automatic fallback to Gemini or rule-based responses.

**Priority Order:**
1. **Claude AI (Sonnet 4)** - Most intelligent, natural responses ✅ Recommended
2. **Gemini AI** - Fast, reliable alternative
3. **Flexible Fallback** - Rule-based system (always works)

---

## 🚀 Quick Setup (3 Steps)

### 1. Install Dependencies

```bash
cd python-chatbot
pip install -r requirements.txt
```

This installs:
- `anthropic>=0.39.0` (Claude AI)
- `google-generativeai>=0.3.0` (Gemini - optional fallback)
- `flask`, `flask-cors`, etc.

### 2. Get Your API Key

**Option A: Claude AI (Recommended)**
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

**Option B: Gemini AI (Alternative)**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Copy the key

### 3. Configure API Key

**Method 1: Interactive Setup (Easiest)**
```bash
cd python-chatbot
python setup_claude.py
```

This will:
- Install dependencies
- Prompt for your API key
- Save to `.env` file
- Test the connection

**Method 2: Manual Setup**

Create a `.env` file in the project root:

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-your-key-here
GEMINI_API_KEY=your-gemini-key-here  # Optional fallback
```

---

## 🏃 Running the Chatbot

```bash
# Start the Flask API (from project root)
python src/api/chatbot_api.py

# In another terminal, start React frontend
npm run dev
```

The API will automatically detect which service is available:
```
✅ Claude AI service initialized successfully
🟢 Using Claude AI (Sonnet 4)
```

Or if Claude isn't configured:
```
⚠️  Claude service initialization failed: API key not found
✅ Gemini AI service initialized successfully
🟢 Using Gemini AI
```

Or if neither is configured:
```
🟡 Using flexible fallback response system
```

---

## 🧪 Testing

### Test in Terminal
```bash
cd python-chatbot
python -c "
from sys import path
path.insert(0, '../src')
from services.claude_service import ClaudeChatbotService

bot = ClaudeChatbotService()
response = bot.chat('What is the best plant for drought?')
print(response)
"
```

### Check API Health
```bash
curl http://localhost:5001/api/health
```

Response:
```json
{
  "status": "healthy",
  "claude_available": true,
  "gemini_available": false,
  "active_service": "Claude AI"
}
```

### Test Chat Endpoint
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Sorghum"}'
```

---

## 💡 Features

### What Claude Brings:

✅ **Natural Language Understanding** - Understands questions in any phrasing
✅ **Context Awareness** - Remembers conversation history
✅ **Data-Driven Responses** - Uses all 6 plant species and 3 zone data
✅ **Intelligent Comparisons** - Deep analysis of plant differences
✅ **Breeding Insights** - Scientific breeding recommendations
✅ **Adaptive Formatting** - Responds in best format for each question

### Example Capabilities:

**Before (Rule-based):**
```
User: "What should I grow in hot dry conditions?"
Bot: "For drought conditions, I recommend: Sorghum - 9/10..."
```

**After (Claude AI):**
```
User: "What should I grow in hot dry conditions?"
Claude: "For hot, dry conditions, I recommend focusing on two exceptional performers:

**Sorghum (Sorghum bicolor)** - Your best choice
- Exceptional heat tolerance: thrives at 25-35°C
- Outstanding drought resistance: 9/10 rating
- Minimal water needs: only 400-600mm rainfall
- Perfectly adapted to Sahara zone conditions
- Small, efficient genome (730 Mbp) maximizes resource use
- Very high stress tolerance overall

**Why Sorghum excels here:**
Its C4 photosynthesis pathway makes it extremely water-efficient, and its deep root system (reaching 1.5-2m) accesses moisture other plants can't. It's specifically evolved for arid conditions.

**Barley as alternative:**
- High drought tolerance (8/10)
- Better for slightly cooler areas (12-22°C)
- Excellent salinity tolerance if soil is salty

Would you like specific cultivation tips for Sorghum in your zone?"
```

---

## 🔧 Customization

### Adjust Response Temperature

In `claude_service.py`:
```python
# More creative (0.8-1.0)
response = bot.chat(message, temperature=0.9)

# More focused (0.3-0.6)
response = bot.chat(message, temperature=0.4)

# Balanced (default: 0.7)
response = bot.chat(message, temperature=0.7)
```

### Add More Data

Edit the system prompt in `claude_service.py`:
```python
# Add more plants
plants_data.append(f"""
New Plant Name
- Genome: X Mbp
- Traits: ...
""")
```

---

## 📊 Cost Estimate

Claude AI Pricing (as of 2024):
- **Sonnet 4**: $3 / 1M input tokens, $15 / 1M output tokens

**Example usage:**
- Average question: ~500 input tokens
- Average response: ~300 output tokens
- **Cost per interaction: ~$0.006** (less than a penny)
- 1000 conversations: ~$6

Very affordable for most applications!

---

## 🐛 Troubleshooting

### "API key not found"
```bash
# Check environment variable
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env | grep ANTHROPIC
```

### "anthropic module not found"
```bash
pip install anthropic>=0.39.0
```

### API still using fallback
```bash
# Check logs when starting API
python src/api/chatbot_api.py

# Should see:
# ✅ Claude AI service initialized successfully
```

### Test Claude directly
```bash
python -c "
import anthropic
client = anthropic.Anthropic(api_key='your-key-here')
msg = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Hi!'}]
)
print(msg.content[0].text)
"
```

---

## 🎓 Learn More

- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/en/api)
- [Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

---

## ✅ Summary

**To use Claude AI:**
1. `pip install anthropic`
2. Get API key from console.anthropic.com
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
4. Start API: `python src/api/chatbot_api.py`
5. Enjoy intelligent responses! 🎉

**The chatbot will automatically:**
- Use Claude if available
- Fall back to Gemini if Claude isn't configured
- Use rule-based responses if neither AI is available
- Always provide helpful, data-driven answers
