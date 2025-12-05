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
    Flexible, intelligent response system that dynamically queries data based on user intent.
    Uses natural language understanding to provide contextual, relevant answers.
    
    Args:
        user_message: User's message
        
    Returns:
        Dynamic response based on available data
    """
    from config.chatbot_tools import execute_tool, COMPREHENSIVE_PLANTS, ALGERIA_ZONES
    
    message_lower = user_message.lower()
    
    # Dynamically extract what the user is asking about
    
    # Check if asking about specific plant
    plant_keywords = ["wheat", "barley", "corn", "maize", "sorghum", "alfalfa", "triticum", "hordeum", "zea", "medicago"]
    mentioned_plant = None
    for keyword in plant_keywords:
        if keyword in message_lower:
            results = execute_tool("search_plants", query=keyword)
            if results:
                mentioned_plant = results[0]
                break
    
    # Check if asking about specific zone
    zone_keywords = {"northern": "Northern", "coastal": "Northern", "plateau": "High Plateau", 
                     "high plateau": "High Plateau", "sahara": "Sahara", "desert": "Sahara", "south": "Sahara"}
    mentioned_zone = None
    for keyword, zone_name in zone_keywords.items():
        if keyword in message_lower:
            mentioned_zone = zone_name
            break
    
    # Flexible query handling
    
    # 1. Asking about specific trait or condition
    if any(word in message_lower for word in ["drought", "dry", "water", "arid"]):
        if mentioned_plant:
            return f"{mentioned_plant['name']} has a drought resistance of {mentioned_plant['resistance']['drought']}/10 and requires {mentioned_plant['environmental_factor']['rainfall']} of rainfall annually. It's classified as having {mentioned_plant['environmental_factor']['drought_tolerance']} drought tolerance with roots reaching {mentioned_plant['root_depth']} deep to access water."
        else:
            # Dynamically find best drought-resistant plants
            drought_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p["resistance"]["drought"], reverse=True)
            response = "For drought conditions, I recommend:\n\n"
            for i, plant in enumerate(drought_plants[:3], 1):
                response += f"{i}. {plant['name']} - {plant['resistance']['drought']}/10 drought resistance ({plant['environmental_factor']['drought_tolerance']} tolerance)\n"
            return response
    
    # 2. Asking about yield or production
    if any(word in message_lower for word in ["yield", "production", "harvest", "productive"]):
        if mentioned_plant:
            return f"{mentioned_plant['name']} has a yield potential of {mentioned_plant['yield_potential']}/10, making it {'excellent' if mentioned_plant['yield_potential'] >= 8 else 'good' if mentioned_plant['yield_potential'] >= 6 else 'moderate'} for production. Its genetic diversity score is {mentioned_plant['genetic_diversity']}/10."
        else:
            high_yield = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p["yield_potential"], reverse=True)
            plants_str = ', '.join([f"{p['name']} ({p['yield_potential']}/10)" for p in high_yield[:3]])
            return f"Highest yielding plants: {plants_str}"
    
    # 3. Asking about resistance (disease, salinity, etc.)
    if "resistance" in message_lower or "disease" in message_lower:
        if mentioned_plant:
            r = mentioned_plant['resistance']
            return f"{mentioned_plant['name']} resistance profile: Drought {r['drought']}/10, Salinity {r['salinity']}/10, Disease {r['disease']}/10"
        else:
            return "Ask me about a specific plant's resistance, or tell me which type of resistance matters most (drought, salinity, or disease)."
    
    # 4. Asking about zone/climate
    if any(word in message_lower for word in ["zone", "climate", "region", "area", "grow", "suitable"]):
        if mentioned_zone:
            zone_info = execute_tool("get_zone_details", zone_name=mentioned_zone)
            plants = execute_tool("get_plants_by_zone", zone=mentioned_zone)
            plant_names = ', '.join([p['name'] for p in plants])
            return f"{zone_info['full_name']}: {zone_info['climate']['rainfall']} rainfall, {zone_info['climate']['temperature']} temperature. Suitable plants: {plant_names}"
        elif mentioned_plant:
            return f"{mentioned_plant['name']} thrives in the {mentioned_plant['zone']} zone with {mentioned_plant['environmental_factor']['rainfall']} rainfall and {mentioned_plant['environmental_factor']['temperature']} temperatures."
        else:
            zone_names = ', '.join([z['name'] for z in ALGERIA_ZONES])
            return f"I have data on {len(ALGERIA_ZONES)} climate zones: {zone_names}. Which one interests you?"
    
    # 5. Asking about specific plant details
    if mentioned_plant and any(word in message_lower for word in ["about", "tell", "info", "detail", "what is", "describe"]):
        p = mentioned_plant
        return f"{p['icon']} **{p['name']}** ({p['scientific_name']})\n\nZone: {p['zone']} | Genome: {p['genome_size']:,} Mbp | Pollination: {p['pollination_type']}\nRainfall: {p['environmental_factor']['rainfall']} | Temp: {p['environmental_factor']['temperature']}\nDrought: {p['resistance']['drought']}/10 | Yield: {p['yield_potential']}/10 | Diversity: {p['genetic_diversity']}/10\nSoil: {p['soil_preference']}"
    
    # 6. Asking about hybridization/crossing
    if any(word in message_lower for word in ["hybrid", "cross", "breed", "combine"]):
        if "history" in message_lower or "recent" in message_lower or "past" in message_lower:
            predictions = execute_tool("get_historical_predictions")
            return f"Recent crosses: {predictions[0]['plant_a']} × {predictions[0]['plant_b']} = {predictions[0]['success_rate']}% success | {predictions[1]['plant_a']} × {predictions[1]['plant_b']} = {predictions[1]['success_rate']}% | {predictions[2]['plant_a']} × {predictions[2]['plant_b']} = {predictions[2]['success_rate']}%"
        else:
            return "To predict a hybrid, tell me which two plants you want to cross, or ask about recent hybridization results."
    
    # 7. Asking about statistics/trending
    if any(word in message_lower for word in ["popular", "trending", "most used", "common", "statistics", "stats"]):
        if "plant" in message_lower:
            trending = execute_tool("get_trending_species")
            trending_str = ', '.join([f"{s['name']} ({s['uses']} uses)" for s in trending[:3]])
            return f"Most used species: {trending_str}"
        else:
            kpis = execute_tool("get_dashboard_kpis")
            return f"Platform stats: {kpis['total_plants']} plants, {kpis['avg_success_rate']}% avg success, {kpis['predictions_today']} predictions today, top zone: {kpis['top_zone_today']}"
    
    # 8. Asking comparison questions
    if any(word in message_lower for word in ["compare", "difference", "better", "vs", "versus"]):
        plants_found = [p for p in COMPREHENSIVE_PLANTS if p['name'].lower() in message_lower or p['scientific_name'].lower() in message_lower]
        if len(plants_found) >= 2:
            p1, p2 = plants_found[0], plants_found[1]
            return f"{p1['name']} vs {p2['name']}: Drought ({p1['resistance']['drought']} vs {p2['resistance']['drought']}), Yield ({p1['yield_potential']} vs {p2['yield_potential']}), Zone ({p1['zone']} vs {p2['zone']})"
        return "Tell me which two plants you want to compare."
    
    # 9. Asking "best" or "recommend"
    if any(word in message_lower for word in ["best", "recommend", "suggest", "should", "good"]):
        # Try to infer criteria from context
        if mentioned_zone:
            plants = execute_tool("get_plants_by_zone", zone=mentioned_zone)
            plant_names = ', '.join([p['name'] for p in plants])
            return f"For {mentioned_zone} zone: {plant_names}"
        elif "yield" in message_lower:
            best = max(COMPREHENSIVE_PLANTS, key=lambda p: p['yield_potential'])
            return f"For highest yield: {best['name']} ({best['yield_potential']}/10)"
        elif "drought" in message_lower or "dry" in message_lower:
            best = max(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['drought'])
            return f"For drought resistance: {best['name']} ({best['resistance']['drought']}/10)"
        else:
            return "What's most important to you? Drought resistance, high yield, specific climate zone, or disease resistance?"
    
    # 10. General help or unclear intent
    if any(word in message_lower for word in ["help", "can you", "how", "what can"]):
        return f"I can help you with:\n• Details about {len(COMPREHENSIVE_PLANTS)} plant species\n• Climate zones and suitability\n• Drought, yield, and resistance comparisons\n• Hybridization predictions\n• Platform statistics\n\nJust ask naturally!"
    
    # Default: Show what's available and ask for clarification
    available_plants = ", ".join([p['name'] for p in COMPREHENSIVE_PLANTS])
    return f"I have data on: {available_plants}. I can also tell you about climate zones, drought resistance, yield potential, or hybridization. What would you like to know?"

