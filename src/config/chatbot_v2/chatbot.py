"""
Clean Chatbot Implementation
Supports Claude, Gemini, and OpenAI with easy configuration
"""

import os
import json
from typing import List, Dict, Optional, Any
from config import (
    API_KEY, AI_SERVICE, MODELS, SYSTEM_PROMPT, 
    SETTINGS, ERROR_MESSAGES
)
from tools import tool_registry


class Chatbot:
    """Universal AI Chatbot with multiple service support"""
    
    def __init__(self, api_key: Optional[str] = None, service: Optional[str] = None):
        """
        Initialize chatbot
        
        Args:
            api_key: API key (uses config if not provided)
            service: AI service to use (uses config if not provided)
        """
        self.api_key = api_key or API_KEY
        self.service = service or AI_SERVICE
        self.config = MODELS.get(self.service, {})
        self.conversation_history: List[Dict] = []
        self.client = None
        
        # Initialize the AI service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the selected AI service"""
        if self.service == "claude":
            self._init_claude()
        elif self.service == "gemini":
            self._init_gemini()
        elif self.service == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unsupported AI service: {self.service}")
    
    def _init_claude(self):
        """Initialize Anthropic Claude"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            if SETTINGS["debug_mode"]:
                print(f"✅ Claude initialized: {self.config['model_name']}")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(
                model_name=self.config["model_name"],
                system_instruction=SYSTEM_PROMPT,
                generation_config={
                    "temperature": self.config["temperature"],
                    "max_output_tokens": self.config["max_tokens"],
                }
            )
            self.chat_session = self.client.start_chat(history=[])
            if SETTINGS["debug_mode"]:
                print(f"✅ Gemini initialized: {self.config['model_name']}")
        except ImportError:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
    
    def _init_openai(self):
        """Initialize OpenAI"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            if SETTINGS["debug_mode"]:
                print(f"✅ OpenAI initialized: {self.config['model_name']}")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def chat(self, message: str) -> str:
        """
        Send a message and get response
        
        Args:
            message: User's message
            
        Returns:
            AI response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Get response from AI service
            if self.service == "claude":
                response = self._chat_claude(message)
            elif self.service == "gemini":
                response = self._chat_gemini(message)
            elif self.service == "openai":
                response = self._chat_openai(message)
            else:
                response = ERROR_MESSAGES["api_error"]
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Limit history size
            max_history = SETTINGS["chat_history_limit"] * 2  # user + assistant pairs
            if len(self.conversation_history) > max_history:
                self.conversation_history = self.conversation_history[-max_history:]
            
            return response
            
        except Exception as e:
            if SETTINGS["debug_mode"]:
                print(f"Error: {e}")
            return ERROR_MESSAGES["api_error"]
    
    def _chat_claude(self, message: str) -> str:
        """Chat with Claude"""
        # Prepare messages with history
        messages = self.conversation_history.copy()
        
        # Handle tools if enabled
        tools = None
        if SETTINGS["enable_tools"] and tool_registry.get_definitions():
            tools = self._format_tools_for_claude()
        
        # Call Claude API
        response = self.client.messages.create(
            model=self.config["model_name"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools if tools else None
        )
        
        # Handle tool calls if present
        if response.stop_reason == "tool_use":
            return self._handle_claude_tools(response, messages)
        
        return response.content[0].text
    
    def _chat_gemini(self, message: str) -> str:
        """Chat with Gemini"""
        response = self.chat_session.send_message(message)
        return response.text
    
    def _chat_openai(self, message: str) -> str:
        """Chat with OpenAI"""
        # Prepare messages with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.conversation_history)
        
        # Handle tools if enabled
        tools = None
        if SETTINGS["enable_tools"] and tool_registry.get_definitions():
            tools = self._format_tools_for_openai()
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.config["model_name"],
            messages=messages,
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"],
            tools=tools if tools else None
        )
        
        # Handle tool calls if present
        assistant_message = response.choices[0].message
        if assistant_message.tool_calls:
            return self._handle_openai_tools(assistant_message, messages)
        
        return assistant_message.content
    
    def _format_tools_for_claude(self) -> List[Dict]:
        """Format tools for Claude API"""
        tools = []
        for tool_def in tool_registry.get_definitions():
            tools.append({
                "name": tool_def["name"],
                "description": tool_def["description"],
                "input_schema": tool_def["parameters"]
            })
        return tools
    
    def _format_tools_for_openai(self) -> List[Dict]:
        """Format tools for OpenAI API"""
        tools = []
        for tool_def in tool_registry.get_definitions():
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_def["name"],
                    "description": tool_def["description"],
                    "parameters": tool_def["parameters"]
                }
            })
        return tools
    
    def _handle_claude_tools(self, response, messages) -> str:
        """Handle Claude tool calls"""
        tool_results = []
        
        for block in response.content:
            if block.type == "tool_use":
                # Execute the tool
                result = tool_registry.execute(block.name, **block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
        
        # Get final response with tool results
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
        
        final_response = self.client.messages.create(
            model=self.config["model_name"],
            max_tokens=self.config["max_tokens"],
            system=SYSTEM_PROMPT,
            messages=messages
        )
        
        return final_response.content[0].text
    
    def _handle_openai_tools(self, assistant_message, messages) -> str:
        """Handle OpenAI tool calls"""
        messages.append(assistant_message)
        
        # Execute tools
        for tool_call in assistant_message.tool_calls:
            result = tool_registry.execute(
                tool_call.function.name,
                **json.loads(tool_call.function.arguments)
            )
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": str(result)
            })
        
        # Get final response
        final_response = self.client.chat.completions.create(
            model=self.config["model_name"],
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.service == "gemini":
            self.chat_session = self.client.start_chat(history=[])
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history.copy()


# ========================================
# SIMPLE USAGE EXAMPLE
# ========================================

if __name__ == "__main__":
    from config import GREETING
    
    # Create chatbot
    bot = Chatbot()
    
    print(GREETING)
    print("\nType 'exit' to quit, 'reset' to clear history\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        if user_input.lower() == "reset":
            bot.reset()
            print("Conversation history cleared!")
            continue
        
        response = bot.chat(user_input)
        print(f"\nBot: {response}\n")
