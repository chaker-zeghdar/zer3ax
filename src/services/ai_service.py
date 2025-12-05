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
    Intelligent, adaptive chatbot that can answer ANY question about plant data.
    Uses semantic understanding and context to provide relevant answers.
    
    Args:
        user_message: User's message
        
    Returns:
        Context-aware response based on available data
    """
    from config.chatbot_tools import execute_tool, COMPREHENSIVE_PLANTS, ALGERIA_ZONES
    
    message_lower = user_message.lower()
    
    # Extract entities from the message
    def extract_plant_entity():
        """Find any plant mentioned in the message"""
        plant_keywords = {
            "wheat": ["wheat", "triticum", "bread wheat"],
            "barley": ["barley", "hordeum"],
            "corn": ["corn", "maize", "zea"],
            "sorghum": ["sorghum", "bicolor"],
            "durum": ["durum", "durum wheat"],
            "alfalfa": ["alfalfa", "medicago"]
        }
        
        for plant_type, keywords in plant_keywords.items():
            if any(kw in message_lower for kw in keywords):
                results = execute_tool("search_plants", query=plant_type)
                if results:
                    return results[0]
        return None
    
    def extract_zone_entity():
        """Find any zone mentioned in the message"""
        zone_map = {
            "northern": "Northern", "coastal": "Northern", "north": "Northern",
            "plateau": "High Plateau", "high plateau": "High Plateau", "middle": "High Plateau",
            "sahara": "Sahara", "desert": "Sahara", "south": "Sahara", "southern": "Sahara"
        }
        
        for keyword, zone in zone_map.items():
            if keyword in message_lower:
                return zone
        return None
    
    def extract_trait_intent():
        """Determine what trait/attribute the user is asking about"""
        trait_patterns = {
            "drought": ["drought", "dry", "water", "arid", "rainfall"],
            "yield": ["yield", "production", "harvest", "productive", "output"],
            "disease": ["disease", "resistant", "immunity", "infection"],
            "salinity": ["salt", "salinity", "saline"],
            "temperature": ["temperature", "temp", "hot", "cold", "climate"],
            "soil": ["soil", "ground", "earth"],
            "genome": ["genome", "genetic", "dna", "gene"],
            "pollination": ["pollination", "pollinate", "cross", "fertilize"]
        }
        
        for trait, keywords in trait_patterns.items():
            if any(kw in message_lower for kw in keywords):
                return trait
        return None
    
    def extract_comparison_intent():
        """Check if user wants to compare things"""
        comparison_words = ["compare", "difference", "vs", "versus", "better", "which is", "or"]
        return any(word in message_lower for word in comparison_words)
    
    def extract_recommendation_intent():
        """Check if user wants recommendations"""
        rec_words = ["best", "recommend", "suggest", "should", "good", "top", "ideal", "suitable"]
        return any(word in message_lower for word in rec_words)
    
    def extract_question_type():
        """Determine the type of question"""
        question_types = {
            "what": ["what", "what's", "what is"],
            "how": ["how", "how to", "how does"],
            "why": ["why", "why is"],
            "when": ["when", "when to"],
            "where": ["where", "which zone", "which area"],
            "which": ["which", "which one"]
        }
        
        for q_type, keywords in question_types.items():
            if any(kw in message_lower for kw in keywords):
                return q_type
        return "statement"
    
    # Extract context
    plant = extract_plant_entity()
    zone = extract_zone_entity()
    trait = extract_trait_intent()
    is_comparison = extract_comparison_intent()
    wants_recommendation = extract_recommendation_intent()
    question_type = extract_question_type()
    
    # Build intelligent response based on context
    
    # 1. SPECIFIC PLANT QUESTIONS
    if plant:
        # General info about the plant
        if any(word in message_lower for word in ["about", "tell me", "what is", "describe", "info", "information"]):
            p = plant
            response = f"🌾 **{p['name']}** ({p['scientific_name']})\n\n"
            response += f"**Zone:** {p['zone']} | **Genome:** {p['genome_size']:,} Mbp\n"
            response += f"**Climate:** {p['environmental_factor']['temperature']}, {p['environmental_factor']['rainfall']} rainfall\n"
            response += f"**Resistance:** Drought {p['resistance']['drought']}/10, Salinity {p['resistance']['salinity']}/10, Disease {p['resistance']['disease']}/10\n"
            response += f"**Yield Potential:** {p['yield_potential']}/10 | **Diversity:** {p['genetic_diversity']}/10\n"
            response += f"**Soil:** {p['soil_preference']} | **Pollination:** {p['pollination_type']}"
            return response
        
        # Specific trait about the plant
        if trait:
            p = plant
            if trait == "drought":
                return f"{p['name']} has a drought resistance of {p['resistance']['drought']}/10 with {p['environmental_factor']['drought_tolerance']} tolerance. It needs {p['environmental_factor']['rainfall']} rainfall and has roots reaching {p['root_depth']}."
            elif trait == "yield":
                return f"{p['name']} has a yield potential of {p['yield_potential']}/10 and genetic diversity of {p['genetic_diversity']}/10, making it {'excellent' if p['yield_potential'] >= 8 else 'good' if p['yield_potential'] >= 6 else 'moderate'} for production."
            elif trait == "disease":
                return f"{p['name']} has disease resistance of {p['resistance']['disease']}/10."
            elif trait == "salinity":
                return f"{p['name']} has salinity resistance of {p['resistance']['salinity']}/10."
            elif trait == "temperature":
                return f"{p['name']} thrives in {p['environmental_factor']['temperature']} with {p['environmental_factor']['rainfall']} annual rainfall."
            elif trait == "soil":
                return f"{p['name']} prefers {p['soil_preference']} soil."
            elif trait == "genome":
                return f"{p['name']} has a genome size of {p['genome_size']:,} Mbp with genetic diversity of {p['genetic_diversity']}/10."
        
        # Where can it grow?
        if question_type in ["where", "which"] or "grow" in message_lower or "zone" in message_lower:
            p = plant
            return f"{p['name']} is best suited for the {p['zone']} zone. It requires {p['environmental_factor']['temperature']} and {p['environmental_factor']['rainfall']} rainfall."
        
        # Default plant response
        p = plant
        return f"{p['name']} is a {p['perenniality'].lower()} plant grown in the {p['zone']} zone with {p['resistance']['drought']}/10 drought resistance and {p['yield_potential']}/10 yield potential."
    
    # 2. ZONE QUESTIONS
    if zone or any(word in message_lower for word in ["zone", "region", "area", "climate"]):
        zone_name = zone or "Northern"  # Default
        
        # What grows in this zone?
        if any(word in message_lower for word in ["grow", "plant", "suitable", "cultivate", "farm"]):
            zone_info = execute_tool("get_zone_details", zone_name=zone_name)
            plants = execute_tool("get_plants_by_zone", zone=zone_name)
            plant_list = ', '.join([p['name'] for p in plants])
            return f"In the {zone_name} zone, you can grow: {plant_list}. Climate: {zone_info['climate']['rainfall']} rainfall, {zone_info['climate']['temperature']}."
        
        # Zone details
        if zone:
            zone_info = execute_tool("get_zone_details", zone_name=zone_name)
            response = f"**{zone_info['full_name']}**\n\n"
            response += f"Climate: {zone_info['climate']['rainfall']} rainfall, {zone_info['climate']['temperature']}\n"
            response += f"Soil: {zone_info['soil_type']}\n"
            response += f"Suitability Score: {zone_info['suitability_score']}/10\n"
            response += f"Stress Factors: {', '.join(zone_info['stress_factors'])}"
            return response
    
    # 3. RECOMMENDATION QUESTIONS
    if wants_recommendation or any(word in message_lower for word in ["looking for", "need", "want", "suitable"]):
        # Best for specific trait
        if trait == "drought":
            best_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['drought'], reverse=True)[:3]
            response = "For drought resistance:\n"
            for i, p in enumerate(best_plants, 1):
                response += f"{i}. {p['name']} - {p['resistance']['drought']}/10 ({p['environmental_factor']['drought_tolerance']})\n"
            return response
        
        elif trait == "yield":
            best_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['yield_potential'], reverse=True)[:3]
            response = "For highest yield:\n"
            for i, p in enumerate(best_plants, 1):
                response += f"{i}. {p['name']} - {p['yield_potential']}/10 yield potential\n"
            return response
        
        elif trait == "disease":
            best_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['disease'], reverse=True)[:3]
            response = "For disease resistance:\n"
            for i, p in enumerate(best_plants, 1):
                response += f"{i}. {p['name']} - {p['resistance']['disease']}/10\n"
            return response
        
        elif trait == "salinity":
            best_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['salinity'], reverse=True)[:3]
            response = "For saline/salty soil:\n"
            for i, p in enumerate(best_plants, 1):
                response += f"{i}. {p['name']} - Salinity resistance: {p['resistance']['salinity']}/10\n"
            return response
        
        elif trait == "genome":
            # Check if they want small or large
            if any(word in message_lower for word in ["small", "smallest", "compact", "tiny"]):
                sorted_by_genome = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['genome_size'])
                smallest = sorted_by_genome[:3]
                response = "Plants with smallest genomes:\n"
                for i, p in enumerate(smallest, 1):
                    response += f"{i}. {p['name']} - {p['genome_size']:,} Mbp\n"
                return response
            else:
                sorted_by_genome = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['genome_size'], reverse=True)
                largest = sorted_by_genome[:3]
                response = "Plants with largest genomes:\n"
                for i, p in enumerate(largest, 1):
                    response += f"{i}. {p['name']} - {p['genome_size']:,} Mbp\n"
                return response
        
        elif trait == "temperature":
            # Check if asking for hot/heat tolerance
            if any(word in message_lower for word in ["hot", "heat", "extreme", "high temp"]):
                # Find plants that tolerate high temps
                hot_climate_plants = [p for p in COMPREHENSIVE_PLANTS if "35" in p['environmental_factor']['temperature'] or "40" in p['environmental_factor']['temperature'] or "45" in p['environmental_factor']['temperature']]
                if hot_climate_plants:
                    response = "Plants for hot/extreme heat:\n"
                    for p in hot_climate_plants:
                        response += f"• {p['name']} - Tolerates up to {p['environmental_factor']['temperature']}\n"
                    return response
                else:
                    # Fallback: Sahara zone plants are heat-tolerant
                    sahara_plants = execute_tool("get_plants_by_zone", zone="Sahara")
                    return f"For extreme heat, try Sahara zone plants: {', '.join([p['name'] for p in sahara_plants])}. Sorghum tolerates 25-35°C."
        
        # Recommendation for zone
        if zone:
            plants = execute_tool("get_plants_by_zone", zone=zone)
            plant_list = ', '.join([p['name'] for p in plants])
            return f"For {zone} zone, I recommend: {plant_list}"
        
        # General recommendation
        return "What's most important to you? I can recommend based on: drought resistance, high yield, disease resistance, salinity tolerance, genome size, or specific climate zones."
    
    # 4. COMPARISON QUESTIONS
    if is_comparison:
        # Find two plants mentioned
        plants_found = []
        for p in COMPREHENSIVE_PLANTS:
            if p['name'].lower() in message_lower or p['scientific_name'].lower() in message_lower:
                plants_found.append(p)
        
        if len(plants_found) >= 2:
            p1, p2 = plants_found[0], plants_found[1]
            response = f"**{p1['name']} vs {p2['name']}**\n\n"
            response += f"Drought: {p1['resistance']['drought']}/10 vs {p2['resistance']['drought']}/10\n"
            response += f"Yield: {p1['yield_potential']}/10 vs {p2['yield_potential']}/10\n"
            response += f"Zone: {p1['zone']} vs {p2['zone']}\n"
            response += f"Genome: {p1['genome_size']:,} Mbp vs {p2['genome_size']:,} Mbp\n"
            response += f"Disease Resistance: {p1['resistance']['disease']}/10 vs {p2['resistance']['disease']}/10"
            return response
        elif len(plants_found) == 1:
            # Only one plant found, show its comparison to similar plants
            p = plants_found[0]
            return f"{p['name']}: Drought {p['resistance']['drought']}/10, Yield {p['yield_potential']}/10, Zone: {p['zone']}, Genome: {p['genome_size']:,} Mbp. Ask me to compare it with another specific plant!"
        
        # Compare zones
        if any(word in message_lower for word in ["zone", "region"]):
            return f"We have {len(ALGERIA_ZONES)} zones: {', '.join([z['name'] for z in ALGERIA_ZONES])}. Northern has the most rainfall, Sahara is driest, High Plateau is in between."
    
    # 5. STATISTICAL/DATA QUESTIONS
    if any(word in message_lower for word in ["how many", "total", "count", "number", "statistics", "stats"]):
        if "plant" in message_lower:
            return f"We have {len(COMPREHENSIVE_PLANTS)} plant species in the database: {', '.join([p['name'] for p in COMPREHENSIVE_PLANTS])}"
        if "zone" in message_lower:
            return f"We have {len(ALGERIA_ZONES)} climate zones: {', '.join([z['name'] for z in ALGERIA_ZONES])}"
        
        # General stats
        kpis = execute_tool("get_dashboard_kpis")
        return f"Platform Statistics:\n• Plants: {kpis['total_plants']}\n• Avg Success Rate: {kpis['avg_success_rate']}%\n• Predictions Today: {kpis['predictions_today']}\n• Top Zone: {kpis['top_zone_today']}"
    
    # 6. TRENDING/POPULAR QUESTIONS
    if any(word in message_lower for word in ["trending", "popular", "most used", "common"]):
        trending = execute_tool("get_trending_species")
        response = "Most popular species:\n"
        for i, s in enumerate(trending[:3], 1):
            response += f"{i}. {s['name']} - {s['uses']} uses\n"
        return response
    
    # 7. HYBRIDIZATION/PREDICTION QUESTIONS
    if any(word in message_lower for word in ["hybrid", "cross", "breed", "predict", "combine", "mix"]):
        if "history" in message_lower or "recent" in message_lower or "past" in message_lower:
            predictions = execute_tool("get_historical_predictions")
            response = "Recent hybridizations:\n"
            for p in predictions[:3]:
                response += f"• {p['plant_a']} × {p['plant_b']} = {p['success_rate']}% success\n"
            return response
        return "I can help with hybridization predictions! Tell me which two plants you want to cross, or ask about recent predictions."
    
    # 8. HOW/WHY QUESTIONS - Provide explanations
    if question_type == "how":
        if "work" in message_lower or "predict" in message_lower:
            return "Hybridization prediction works by analyzing genetic compatibility, climate zone overlap, trait complementarity, and historical success rates to estimate the likelihood of successful crosses."
        if "choose" in message_lower or "select" in message_lower:
            return "Choose plants based on: 1) Your climate zone, 2) Desired traits (drought resistance, yield), 3) Soil type, 4) Water availability. I can help you find the best match!"
    
    if question_type == "why":
        return "Plant characteristics are determined by genetics, environment, and breeding history. Different traits make plants suitable for different conditions and uses."
    
    # 9. LIST/SHOW QUESTIONS
    if any(word in message_lower for word in ["list", "show me", "all", "available"]):
        if "plant" in message_lower:
            # Check if asking for specific attribute
            if "diversity" in message_lower or "genetic" in message_lower:
                sorted_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['genetic_diversity'], reverse=True)
                plant_list = '\n'.join([f"• {p['name']} - Genetic Diversity: {p['genetic_diversity']}/10, Genome: {p['genome_size']:,} Mbp" for p in sorted_plants])
                return f"Plants by genetic diversity:\n{plant_list}"
            elif "genome" in message_lower or "largest" in message_lower or "biggest" in message_lower:
                sorted_plants = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['genome_size'], reverse=True)
                plant_list = '\n'.join([f"• {p['name']} - {p['genome_size']:,} Mbp" for p in sorted_plants])
                return f"Plants by genome size:\n{plant_list}"
            else:
                plant_list = '\n'.join([f"• {p['name']} ({p['zone']}) - Drought: {p['resistance']['drought']}/10, Yield: {p['yield_potential']}/10" for p in COMPREHENSIVE_PLANTS])
                return f"Available plants:\n{plant_list}"
        if "zone" in message_lower:
            zone_list = '\n'.join([f"• {z['full_name']} - {z['climate']['rainfall']}, {z['climate']['temperature']}" for z in ALGERIA_ZONES])
            return f"Climate zones:\n{zone_list}"
    
    # 10. HELP/CAPABILITY QUESTIONS
    if any(word in message_lower for word in ["help", "can you", "what can", "how to use", "capabilities", "features"]):
        return f"""🌾 **AI Plant Breeding Assistant - Capabilities**

**🔍 Search & Information:**
• Get detailed info about any plant: "Tell me about [plant name]"
• Search by trait: "drought resistant plants", "high yield crops"
• Zone information: "What grows in the Sahara?"
• Environmental needs: "Can wheat handle heat?"

**🔄 Comparisons:**
• Compare any two plants: "Compare wheat and barley"
• Show differences: "What's better for drought, corn or sorghum?"
• Zone comparisons: "Northern vs Sahara climate"

**🎯 Recommendations:**
• Best for traits: "Best plant for drought/yield/disease"
• Zone-specific: "What should I grow in High Plateau?"
• Soil-specific: "Plants for saline soil"
• Climate-specific: "What handles extreme heat?"

**📋 Lists & Rankings:**
• "Show all plants"
• "List by genetic diversity"
• "Which has the largest/smallest genome?"
• "Show trending species"

**🧬 Breeding & Predictions:**
• "Predict wheat x barley hybrid"
• "Recent hybridization results"
• "Success rate for [plant A] x [plant B]"

**📊 Statistics:**
• "How many plants in database?"
• "Show platform statistics"
• "Most popular species"

**Available Data:**
• {len(COMPREHENSIVE_PLANTS)} plant species with complete profiles
• {len(ALGERIA_ZONES)} climate zones (Northern, High Plateau, Sahara)
• Genome sizes, resistance scores, yield potential
• Historical predictions & trending data

**Just ask naturally!** I understand questions like:
- "I need something for dry conditions"
- "What's the difference between X and Y?"
- "Looking for high yield in northern zone"
- "Can you recommend something productive?"
"""
    
    # 11. GENERAL TRAIT QUESTIONS (no specific plant)
    if trait and not plant:
        if trait == "drought":
            best = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['drought'], reverse=True)[:3]
            names = ', '.join([f"{p['name']} ({p['resistance']['drought']}/10)" for p in best])
            return f"Best drought-resistant plants: {names}"
        elif trait == "yield":
            best = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['yield_potential'], reverse=True)[:3]
            names = ', '.join([f"{p['name']} ({p['yield_potential']}/10)" for p in best])
            return f"Highest yielding plants: {names}"
        elif trait == "salinity":
            best = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['resistance']['salinity'], reverse=True)[:3]
            response = "Plants suitable for saline soil:\n"
            for p in best:
                response += f"• {p['name']} - Salinity resistance: {p['resistance']['salinity']}/10\n"
            return response
        elif trait == "genome":
            sorted_by_genome = sorted(COMPREHENSIVE_PLANTS, key=lambda p: p['genome_size'], reverse=True)
            largest = sorted_by_genome[0]
            response = f"Largest genome: {largest['name']} with {largest['genome_size']:,} Mbp\n\nAll plants by genome size:\n"
            for p in sorted_by_genome:
                response += f"• {p['name']}: {p['genome_size']:,} Mbp\n"
            return response
    
    # 12. FALLBACK - Intelligent context-aware response
    # Try to understand what data they might be looking for
    context_clues = []
    
    if any(word in message_lower for word in ["resistant", "resistance"]):
        context_clues.append("resistance traits (drought, salinity, disease)")
    if any(word in message_lower for word in ["genetic", "genome", "dna"]):
        context_clues.append("genetic information")
    if any(word in message_lower for word in ["climate", "weather", "temperature"]):
        context_clues.append("climate and environmental data")
    
    if context_clues:
        return f"I have data on {', '.join(context_clues)}. Could you be more specific? For example, ask about a specific plant, zone, or trait you're interested in."
    
    # Ultimate fallback
    return f"I have comprehensive data on {len(COMPREHENSIVE_PLANTS)} plants ({', '.join([p['name'] for p in COMPREHENSIVE_PLANTS[:3]])}, etc.) and {len(ALGERIA_ZONES)} climate zones. Ask me about specific plants, traits, zones, or recommendations!"

