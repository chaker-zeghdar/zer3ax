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
    Enhanced rule-based response system using comprehensive data.
    Provides detailed answers using all available plant, zone, and historical data.
    
    Args:
        user_message: User's message
        
    Returns:
        Response text with specific data from the database
    """
    from config.chatbot_tools import execute_tool, COMPREHENSIVE_PLANTS, ALGERIA_ZONES
    
    message_lower = user_message.lower()
    
    # Handle drought/resistance queries with detailed data
    if "drought" in message_lower or "dry" in message_lower or "water" in message_lower:
        # Get plants sorted by drought resistance
        drought_plants = sorted(
            COMPREHENSIVE_PLANTS,
            key=lambda p: p["resistance"]["drought"],
            reverse=True
        )[:3]
        
        response = "**Best Plants for Drought Conditions:**\n\n"
        for i, plant in enumerate(drought_plants, 1):
            response += f"{i}. **{plant['name']} ({plant['scientific_name']})**\n"
            response += f"   - Drought Resistance: {plant['resistance']['drought']}/10\n"
            response += f"   - Drought Tolerance: {plant['environmental_factor']['drought_tolerance']}\n"
            response += f"   - Rainfall Needs: {plant['environmental_factor']['rainfall']}\n"
            response += f"   - Root Depth: {plant['root_depth']} (deeper roots access more water)\n"
            response += f"   - Zone: {plant['zone']}\n"
            response += f"   - Key Traits: {', '.join(plant['traits'][:3])}\n\n"
        
        return response
    
    # Handle plant search with comprehensive data
    if "search" in message_lower or "find plant" in message_lower or "tell me about" in message_lower:
        import re
        search_term = re.sub(r'search|find plant|tell me about|for', '', user_message, flags=re.IGNORECASE).strip()
        results = execute_tool("search_plants", query=search_term)
        
        if results:
            plant = results[0]  # Get first result
            response = f"# {plant['name']} ({plant['scientific_name']}) {plant.get('icon', '')}\n\n"
            response += f"**Basic Information:**\n"
            response += f"- Zone: {plant['zone']}\n"
            response += f"- Perenniality: {plant['perenniality']}\n"
            response += f"- Pollination: {plant['pollination_type']}\n"
            response += f"- Genome Size: {plant['genome_size']:,} Mbp\n\n"
            
            response += f"**Environmental Requirements:**\n"
            response += f"- Rainfall: {plant['environmental_factor']['rainfall']}\n"
            response += f"- Temperature: {plant['environmental_factor']['temperature']}\n"
            response += f"- Drought Tolerance: {plant['environmental_factor']['drought_tolerance']}\n\n"
            
            response += f"**Resistance Scores:**\n"
            response += f"- Drought: {plant['resistance']['drought']}/10\n"
            response += f"- Salinity: {plant['resistance']['salinity']}/10\n"
            response += f"- Disease: {plant['resistance']['disease']}/10\n\n"
            
            response += f"**Growth Characteristics:**\n"
            response += f"- Form: {plant['growth_form']}\n"
            response += f"- Root Depth: {plant['root_depth']}\n"
            response += f"- Lifespan: {plant['lifespan']}\n"
            response += f"- Soil Preference: {plant['soil_preference']}\n\n"
            
            response += f"**Agronomic Potential:**\n"
            response += f"- Yield Potential: {plant['yield_potential']}/10\n"
            response += f"- Genetic Diversity: {plant['genetic_diversity']}/10\n"
            
            if len(results) > 1:
                response += f"\n*Found {len(results)} total matches. Use search to explore others.*"
            
            return response
        return f"I couldn't find any plants matching '{search_term}'. Available plants: {', '.join([p['name'] for p in COMPREHENSIVE_PLANTS])}"
    
    # Handle zone queries with detailed climate data
    if any(zone in message_lower for zone in ["zone", "northern", "plateau", "sahara", "climate"]):
        zone = "Northern"
        if "plateau" in message_lower or "high plateau" in message_lower:
            zone = "High Plateau"
        elif "sahara" in message_lower or "southern" in message_lower or "desert" in message_lower:
            zone = "Sahara"
        
        zone_info = execute_tool("get_zone_details", zone_name=zone)
        stats = execute_tool("get_zone_statistics", zone=zone)
        
        if zone_info:
            response = f"# {zone_info['full_name']}\n\n"
            response += f"**Climate Conditions:**\n"
            response += f"- Rainfall: {zone_info['climate']['rainfall']} annually\n"
            response += f"- Temperature Range: {zone_info['climate']['temperature']}\n"
            response += f"- Humidity: {zone_info['climate']['humidity']}\n\n"
            
            response += f"**Soil Characteristics:**\n"
            response += f"- Type: {zone_info['soil_type']}\n\n"
            
            response += f"**Stress Factors:**\n"
            for factor in zone_info['stress_factors']:
                response += f"- {factor}\n"
            
            response += f"\n**Suitable Plants ({stats['plant_count']} species):**\n"
            for plant_info in stats['plants']:
                response += f"- {plant_info['name']} ({plant_info['scientific_name']})\n"
            
            response += f"\n**Suitability Score: {zone_info['suitability_score']}/10**\n"
            
            if stats['common_traits']:
                response += f"\n**Common Traits in this Zone:**\n"
                for trait_info in stats['common_traits'][:3]:
                    response += f"- {trait_info['trait'].replace('_', ' ').title()} ({trait_info['count']} plants)\n"
            
            return response
    
    # Handle prediction/hybridization queries
    if "predict" in message_lower or "hybrid" in message_lower or "cross" in message_lower:
        predictions = execute_tool("get_historical_predictions")
        response = "**Recent Hybridization Predictions:**\n\n"
        
        for pred in predictions[:3]:
            response += f"• {pred['plant_a']} × {pred['plant_b']}\n"
            response += f"  Success Rate: {pred['success_rate']}%\n"
            response += f"  Confidence: {pred['confidence']:.0%}\n"
            response += f"  Zone: {pred['zone']}\n"
            response += f"  Date: {pred['date']}\n\n"
        
        response += "\nTo predict a specific cross, use our Predict feature or ask about two specific plants!"
        return response
    
    # Handle trait queries
    if "trait" in message_lower:
        response = "**Plant Traits in Our Database:**\n\n"
        all_traits = set()
        for plant in COMPREHENSIVE_PLANTS:
            all_traits.update(plant['traits'])
        
        response += "Key genetic traits tracked:\n"
        for trait in sorted(all_traits):
            response += f"- {trait.replace('_', ' ').title()}\n"
        
        response += "\nThese traits influence hybridization success, yield potential, and environmental adaptation."
        return response
    
    # Handle statistics/KPI queries
    if "statistics" in message_lower or "stats" in message_lower or "kpi" in message_lower or "dashboard" in message_lower:
        kpis = execute_tool("get_dashboard_kpis")
        trending = execute_tool("get_trending_species")
        
        response = "**Zer3aZ Platform Statistics:**\n\n"
        response += f"- Total Plant Species: {kpis['total_plants']}\n"
        response += f"- Tracked Traits: {kpis['total_traits']}\n"
        response += f"- Average Success Rate: {kpis['avg_success_rate']}%\n"
        response += f"- Predictions Today: {kpis['predictions_today']}\n"
        response += f"- Top Zone Today: {kpis['top_zone_today']}\n\n"
        
        response += "**Trending Species (by usage):**\n"
        for species in trending[:5]:
            response += f"- {species['name']}: {species['uses']} uses\n"
        
        return response
    
    # Handle help
    if "help" in message_lower or "what can you do" in message_lower:
        response = chatbot_config["response_templates"]["general_help"]
        response += "\n\n**Available Data:**\n"
        response += f"- {len(COMPREHENSIVE_PLANTS)} plant species with complete genetic profiles\n"
        response += f"- {len(ALGERIA_ZONES)} climate zones across Algeria\n"
        response += "- Historical prediction data\n"
        response += "- Trending species statistics\n"
        response += "\n**Ask me about:**\n"
        response += "- Specific plants (e.g., 'Tell me about wheat')\n"
        response += "- Climate zones (e.g., 'What grows in the Sahara?')\n"
        response += "- Drought resistance (e.g., 'Best plants for dry conditions')\n"
        response += "- Predictions (e.g., 'What are recent hybridization results?')\n"
        response += "- Statistics (e.g., 'Show me platform statistics')\n"
        return response
    
    # Default: Show available plants
    response = "I have comprehensive data on **6 plant species**:\n\n"
    for plant in COMPREHENSIVE_PLANTS:
        response += f"{plant['icon']} **{plant['name']}** ({plant['scientific_name']}) - {plant['zone']} zone\n"
    
    response += "\nAsk me about any plant, climate zone, drought tolerance, or hybridization predictions!"
    return response
