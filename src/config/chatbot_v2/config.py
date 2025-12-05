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

SYSTEM_PROMPT = """You are a helpful AI assistant.

YOUR ROLE:
- Answer questions clearly and concisely
- Provide accurate, helpful information
- Be professional and friendly

YOUR CAPABILITIES:
- General knowledge and conversation
- Problem-solving and analysis
- Information retrieval and explanation

RESPONSE STYLE:
- Clear and well-structured
- Use examples when helpful
- Be concise but thorough
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
    "enable_tools": False,  # Enable tool/function calling
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
