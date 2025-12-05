"""
AI Service Integration

This module provides integration with various AI services like OpenAI GPT and Anthropic Claude.
It uses the chatbot configuration and tools to provide intelligent responses.

SETUP INSTRUCTIONS:
1. Install required packages:
   - For OpenAI: pip install openai
   - For Anthropic: pip install anthropic
   
2. Set environment variables:
   - OPENAI_API_KEY for OpenAI
   - ANTHROPIC_API_KEY for Anthropic
   
3. Uncomment the desired integration below and configure it
"""

import os
import json
from typing import List, Dict, Any, Optional

# Import configuration
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.chatbot_prompt import chatbot_config
from config.chatbot_tools import chatbot_tools

# Google Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")

# Google Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")


class ChatbotAIService:
    """Base class for AI service integrations."""
    
    def __init__(self):
        self.system_prompt = chatbot_config["system_prompt"]
        self.tools = chatbot_tools
    
    def format_messages(self, conversation_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format conversation history for AI service.
        
        Args:
            conversation_history: List of message dicts with 'type' and 'text'
            
        Returns:
            List of formatted messages
        """
        formatted = []
        for msg in conversation_history:
            role = "user" if msg["type"] == "user" else "assistant"
            formatted.append({"role": role, "content": msg["text"]})
        return formatted
    
    def format_tools_for_openai(self) -> List[Dict[str, Any]]:
        """Format tools for OpenAI function calling."""
        formatted_tools = []
        for tool_name, tool_data in self.tools.items():
            formatted_tools.append({
                "type": "function",
                "function": {
                    "name": tool_data["name"],
                    "description": tool_data["description"],
                    "parameters": {
                        "type": "object",
                        "properties": tool_data["parameters"],
                        "required": list(tool_data["parameters"].keys())
                    }
                }
            })
        return formatted_tools
    
    def format_tools_for_anthropic(self) -> List[Dict[str, Any]]:
        """Format tools for Anthropic Claude."""
        formatted_tools = []
        for tool_name, tool_data in self.tools.items():
            formatted_tools.append({
                "name": tool_data["name"],
                "description": tool_data["description"],
                "input_schema": {
                    "type": "object",
                    "properties": tool_data["parameters"],
                    "required": list(tool_data["parameters"].keys())
                }
            })
        return formatted_tools


class OpenAIService(ChatbotAIService):
    """OpenAI GPT integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Uncomment to use OpenAI
        # from openai import OpenAI
        # self.client = OpenAI(api_key=self.api_key)
    
    async def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Send a message to OpenAI and get a response.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            
        Returns:
            AI response text
        """
        # Uncomment to use OpenAI
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if conversation_history:
                messages.extend(self.format_messages(conversation_history))
            
            messages.append({"role": "user", "content": user_message})
            
            # Prepare tools
            tools = self.format_tools_for_openai()
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls
            if assistant_message.tool_calls:
                tool_results = []
                
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    if tool_name in self.tools:
                        result = self.tools[tool_name]["execute"](**tool_args)
                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(result)
                        })
                
                # Get final response with tool results
                messages.append(assistant_message)
                messages.extend(tool_results)
                
                final_response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages
                )
                
                return final_response.choices[0].message.content
            
            return assistant_message.content
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return chatbot_config["response_templates"]["fallback"]
        """
        
        # Placeholder return
        return "OpenAI integration not yet configured. Please uncomment the code above."


class AnthropicService(ChatbotAIService):
    """Anthropic Claude integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        
        # Uncomment to use Anthropic
        # from anthropic import Anthropic
        # self.client = Anthropic(api_key=self.api_key)
    
    async def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Send a message to Claude and get a response.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            
        Returns:
            AI response text
        """
        # Uncomment to use Anthropic
        """
        try:
            messages = []
            
            if conversation_history:
                messages = self.format_messages(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            # Prepare tools
            tools = self.format_tools_for_anthropic()
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=self.system_prompt,
                messages=messages,
                tools=tools
            )
            
            # Handle tool use
            if any(block.type == "tool_use" for block in response.content):
                tool_results = []
                
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        
                        # Execute the tool
                        if tool_name in self.tools:
                            result = self.tools[tool_name]["execute"](**tool_input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result)
                            })
                
                # Get final response with tool results
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
                
                final_response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=self.system_prompt,
                    messages=messages
                )
                
                return final_response.content[0].text
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API Error: {e}")
            return chatbot_config["response_templates"]["fallback"]
        """
        
        # Placeholder return
        return "Anthropic integration not yet configured. Please uncomment the code above."


class GeminiService(ChatbotAIService):
    """Google Gemini AI integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        # Use provided API key or from environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or "AIzaSyD1sB4FJqCSLu1sCdnmEcyAEsMxJV80jPw"
        
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            },
            system_instruction=self.system_prompt
        )
        
        # Initialize chat session
        self.chat_session = None
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Send a message to Gemini and get a response.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages (optional)
            
        Returns:
            AI response text
        """
        try:
            # Start or continue chat session
            if self.chat_session is None or not conversation_history:
                self.chat_session = self.model.start_chat(history=[])
            else:
                # Convert conversation history to Gemini format
                history = []
                for msg in conversation_history:
                    role = "user" if msg["type"] == "user" else "model"
                    history.append({
                        "role": role,
                        "parts": [msg["text"]]
                    })
                self.chat_session = self.model.start_chat(history=history)
            
            # Send message and get response
            response = self.chat_session.send_message(user_message)
            return response.text
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            import traceback
            traceback.print_exc()
            return chatbot_config["response_templates"]["fallback"]
    
    def generate_report(self, plant_a_id: int, plant_b_id: int) -> str:
        """
        Generate a detailed breeding report using Gemini.
        
        Args:
            plant_a_id: First plant ID
            plant_b_id: Second plant ID
            
        Returns:
            Formatted report text
        """
        try:
            # Get report data from tool
            from config.chatbot_tools import execute_tool
            report_data = execute_tool("generate_detailed_report", plant_a_id=plant_a_id, plant_b_id=plant_b_id)
            
            if not report_data:
                return "Unable to generate report. Please check plant IDs."
            
            # Create prompt for Gemini to format the report
            prompt = f"""Generate a comprehensive, professional plant breeding analysis report based on the following data:

{json.dumps(report_data, indent=2)}

Format the report with:
- Clear section headings
- Detailed scientific explanations
- Actionable recommendations
- Professional tone suitable for agricultural researchers and farmers
- Include all sections: Executive Summary, Parent Analysis, Trait Compatibility, Predictions, Recommendations, Environmental Assessment, and Risk Analysis
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Report generation error: {e}")
            return f"Error generating report: {str(e)}"


# Default service instance (configure as needed)
def get_ai_service(service_type: str = "gemini") -> ChatbotAIService:
    """
    Get an AI service instance.
    
    Args:
        service_type: Type of service ("gemini", "openai", or "anthropic")
        
    Returns:
        ChatbotAIService instance
    """
    if service_type.lower() == "gemini":
        try:
            return GeminiService()
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            return None
    elif service_type.lower() == "openai":
        try:
            return OpenAIService()
        except ValueError as e:
            print(f"Failed to initialize OpenAI: {e}")
            return None
    elif service_type.lower() == "anthropic":
        try:
            return AnthropicService()
        except ValueError as e:
            print(f"Failed to initialize Anthropic: {e}")
            return None
    else:
        raise ValueError(f"Unknown service type: {service_type}")


# Simple fallback function for testing without API
def simple_chat_response(user_message: str) -> str:
    """
    Simple rule-based response system (no AI API required).
    Use this for testing or as a fallback.
    
    Args:
        user_message: User's message
        
    Returns:
        Response text
    """
    from config.chatbot_tools import execute_tool
    
    message_lower = user_message.lower()
    
    # Handle plant search
    if "search" in message_lower or "find plant" in message_lower:
        import re
        search_term = re.sub(r'search|find plant|for', '', user_message, flags=re.IGNORECASE).strip()
        results = execute_tool("search_plants", query=search_term)
        
        if results:
            plant_list = "\n".join([
                f"• {p['name']} ({p['scientific_name']}) - {p['zone']} zone"
                for p in results[:3]
            ])
            return f"I found {len(results)} plant(s) matching '{search_term}':\n\n{plant_list}"
        return f"I couldn't find any plants matching '{search_term}'."
    
    # Handle zone queries
    if any(zone in message_lower for zone in ["zone", "northern", "plateau", "sahara"]):
        zone = "Northern"
        if "plateau" in message_lower:
            zone = "High Plateau"
        elif "sahara" in message_lower:
            zone = "Sahara"
        
        stats = execute_tool("get_zone_statistics", zone=zone)
        traits = ", ".join([t["trait"] for t in stats["common_traits"][:3]])
        return f"{zone} zone has {stats['plant_count']} plants. Common traits: {traits}."
    
    # Handle help
    if "help" in message_lower or "what can you do" in message_lower:
        return chatbot_config["response_templates"]["general_help"]
    
    # Default fallback
    return chatbot_config["response_templates"]["fallback"]
