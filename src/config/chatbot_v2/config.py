"""
Chatbot Configuration
Clean, modular configuration for AI chatbot
"""

import os
from typing import Dict, Any

# ========================================
# API CONFIGURATION
# ========================================

# Your API Key - Replace with your actual key
API_KEY = os.getenv("CHATBOT_API_KEY", "AIzaSyD1sB4FJqCSLu1sCdnmEcyAEsMxJV80jPw")

# Which AI service to use: "claude", "gemini", "openai"
AI_SERVICE = "gemini"  # Using Google Gemini

# Model configuration
MODELS = {
    "claude": {
        "model_name": "claude-3-5-sonnet-20241022",
        "max_tokens": 2048,
        "temperature": 0.7,
    },
    "gemini": {
        "model_name": "gemini-1.5-pro",
        "max_tokens": 2048,
        "temperature": 0.7,
    },
    "openai": {
        "model_name": "gpt-4-turbo-preview",
        "max_tokens": 2048,
        "temperature": 0.7,
    }
}

# ========================================
# SYSTEM PROMPT
# ========================================

SYSTEM_PROMPT = """You are an intelligent Plant Breeding AI Assistant with access to comprehensive plant data.

Your approach:
1. Extract keywords from user questions (plant names, zones, traits)
2. Use the answer_question tool to find relevant data
3. Provide clear, data-driven answers

You have data on:
- 6 plant species (Bread Wheat, Barley, Corn, Sorghum, Durum Wheat, Alfalfa)
- 3 Algeria zones (Northern, High Plateau, Sahara)
- Traits: drought resistance, salinity, disease, yield, genome size, rainfall, temperature

ANSWER ANY QUESTION by:
- Identifying keywords in the question
- Matching keywords to available data
- Providing specific numbers and details from the database

EXAMPLES:
"What is the drought resistance of wheat?" → Extract 'wheat' and 'drought', return data
"Best plants for Sahara?" → Extract 'Sahara', return recommended plants
"Which plant has highest yield?" → Rank by yield, return top plant

ALWAYS use specific data, numbers, and details from the database.
"""

# ========================================
# TOOL DEFINITIONS
# ========================================

# Define your custom tools/functions here
TOOLS = []

# Example tool structure (uncomment and customize):
"""
TOOLS = [
    {
        "name": "search_database",
        "description": "Search for information in the database",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    }
]
"""

# ========================================
# CHATBOT SETTINGS
# ========================================

SETTINGS = {
    "chat_history_limit": 10,  # Max messages to keep in history
    "streaming": False,  # Enable streaming responses
    "enable_tools": True,  # Enable tool/function calling (ENABLED FOR KEYWORD-BASED Q&A)
    "debug_mode": True,  # Print debug information
}

# ========================================
# GREETING MESSAGE
# ========================================

GREETING = """👋 Hello! I'm your AI assistant. How can I help you today?"""

# ========================================
# ERROR MESSAGES
# ========================================

ERROR_MESSAGES = {
    "api_error": "I encountered an error processing your request. Please try again.",
    "tool_error": "I had trouble executing that action. Please try again.",
    "rate_limit": "I'm receiving too many requests. Please wait a moment and try again.",
    "invalid_input": "I didn't quite understand that. Could you rephrase your question?",
}
