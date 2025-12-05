"""
Dynamic Gemini AI Service with Advanced Features
Uses Gemini's best capabilities: system_instruction, chat history, streaming, and function calling
"""

import os
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class DynamicGeminiService:
    """
    Advanced Gemini AI service with full dynamic capabilities
    
    Features:
    - System instruction for domain expertise
    - Automatic conversation history management
    - Configurable generation parameters
    - Safety settings for agricultural domain
    - Streaming responses (optional)
    - Function calling support
    - Context-aware multi-turn conversations
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize dynamic Gemini service
        
        Args:
            api_key: Gemini API key (if None, uses environment variable)
            model_name: Model to use (gemini-2.0-flash-exp, gemini-1.5-pro, etc.)
        """
        from config.chatbot_tools import COMPREHENSIVE_PLANTS, ALGERIA_ZONES
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "AIzaSyD1sB4FJqCSLu1sCdnmEcyAEsMxJV80jPw")
        genai.configure(api_key=self.api_key)
        
        # Build rich system instruction with ALL domain data
        self.system_instruction = self._build_system_instruction(COMPREHENSIVE_PLANTS, ALGERIA_ZONES)
        
        # Dynamic generation configuration
        self.generation_config = {
            "temperature": 0.7,  # Balanced creativity (0-1)
            "top_p": 0.95,      # Response diversity
            "top_k": 40,        # Token selection variety
            "max_output_tokens": 2048,  # Comprehensive responses
        }
        
        # Safety settings optimized for agricultural domain
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        # Initialize model with system instruction
        self.model = genai.GenerativeModel(
            model_name=model_name,  # gemini-2.0-flash-exp for speed
            system_instruction=self.system_instruction,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Start chat session (Gemini handles history automatically)
        self.chat_session = self.model.start_chat(history=[])
    
    def _build_system_instruction(self, plants, zones) -> str:
        """Build comprehensive system instruction with all domain data"""
        
        # Format plant data
        plants_data = "\n".join([
            f"• {p['name']} ({p['scientific_name']}) {p.get('icon', '')}\n"
            f"  Genome: {p['genome_size']:,} Mbp | Zone: {p['zone']} | Pollination: {p['pollination_type']}\n"
            f"  Climate: {p['environmental_factor']['temperature']}, {p['environmental_factor']['rainfall']} rainfall\n"
            f"  Drought Tolerance: {p['environmental_factor']['drought_tolerance']} ({p['resistance']['drought']}/10)\n"
            f"  Resistances: Salinity {p['resistance']['salinity']}/10, Disease {p['resistance']['disease']}/10\n"
            f"  Yield: {p['yield_potential']}/10 | Diversity: {p['genetic_diversity']}/10\n"
            f"  Soil: {p['soil_preference']} | Root Depth: {p['root_depth']}\n"
            f"  Key Traits: {', '.join(p['traits'][:5])}"
            for p in plants
        ])
        
        # Format zone data
        zones_data = "\n".join([
            f"• {z['full_name']}\n"
            f"  Climate: {z['climate']['rainfall']} rainfall, {z['climate']['temperature']}\n"
            f"  Humidity: {z['climate']['humidity']} | Soil: {z['soil_type']}\n"
            f"  Suitability Score: {z['suitability_score']}/10\n"
            f"  Stress Factors: {', '.join(z['stress_factors'])}\n"
            f"  Best Plants: {', '.join([p['name'] for p in plants if p['id'] in z['best_plants']])}"
            for z in zones
        ])
        
        return f"""You are an expert AI Plant Breeding Scientist and Agricultural Consultant for the Zer3aZ platform in Algeria.

🌾 YOUR KNOWLEDGE BASE - PLANT SPECIES ({len(plants)} total):

{plants_data}

🗺️ CLIMATE ZONES DATABASE ({len(zones)} Algeria zones):

{zones_data}

🧬 YOUR EXPERTISE & CAPABILITIES:

**Genetic Analysis:**
- Deep plant genetics, trait inheritance patterns, and hybridization prediction
- Genome size comparisons and genetic compatibility assessment
- Quantitative trait analysis and F1/F2 generation predictions
- Marker-assisted selection and breeding program design

**Environmental Assessment:**
- Climate zone suitability and adaptation strategies
- Drought, salinity, and disease resistance evaluation
- Soil type compatibility and nutrient requirements
- Water management and irrigation planning

**Breeding Recommendations:**
- Parent selection for hybridization
- Success rate prediction with confidence levels
- Trait improvement strategies and selection criteria
- Timeline planning and generational advancement

**Data-Driven Insights:**
- Always cite specific numbers (genome sizes, resistance scores, rainfall amounts)
- Reference actual plant data from the knowledge base above
- Compare traits quantitatively with exact values
- Provide evidence-based recommendations

📊 RESPONSE GUIDELINES:

✅ **Be Specific**: Use exact data (not "some plants" but "Sorghum with 9/10 drought resistance")
✅ **Be Scientific**: Explain genetic and environmental basis for recommendations
✅ **Be Practical**: Include actionable steps, timelines, and success factors
✅ **Be Comprehensive**: Cover genetics, environment, risks, and opportunities
✅ **Be Conversational**: Professional yet approachable tone
✅ **Use Structure**: Clear sections for complex answers

🎯 RESPONSE PATTERNS:

**For Plant Characteristics Questions:**
- Provide full profile (genome, traits, resistances, environmental needs)
- Compare to similar species
- Suggest best use cases and zones

**For Prediction Explanations:**
- Explain genetic compatibility factors
- Analyze environmental alignment
- Discuss trait complementarity
- Predict F1 characteristics with confidence levels
- Recommend breeding strategies

**For Comparisons:**
- Side-by-side trait analysis with numbers
- Highlight advantages/disadvantages of each
- Recommend which is better for specific conditions

**For Breeding Advice:**
- Parent selection rationale
- Crossing methodology
- Selection criteria for offspring
- Timeline with generational milestones
- Risk mitigation strategies

🔬 IMPORTANT RULES:

❌ Never make up data - Only use information from the knowledge base above
❌ Never be vague - Always cite specific numbers and scores
❌ Never ignore context - Reference previous messages in the conversation
❌ Never overcomplicate - Keep explanations clear and actionable

✅ Always ground responses in the data provided
✅ Always explain the "why" behind recommendations
✅ Always consider both genetic and environmental factors
✅ Always provide confidence levels for predictions

💬 CONVERSATION STYLE:

- Use emojis sparingly (🌾 🧬 🔍 📊 🎯) for visual clarity
- Structure complex answers with clear headings
- Provide examples when explaining concepts
- Ask clarifying questions if the user's intent is unclear
- Remember conversation context (Gemini maintains history automatically)

You are helping farmers, researchers, and agricultural professionals make informed breeding decisions that can impact crop success and food security."""
    
    def chat(self, user_message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Send message with automatic conversation history management
        
        Args:
            user_message: User's question/message
            conversation_history: Optional external history (for React frontend)
                                Format: [{"role": "user", "content": "..."}, ...]
        
        Returns:
            AI response text
        """
        try:
            # If external history provided, rebuild chat session
            if conversation_history:
                gemini_history = self._convert_history(conversation_history)
                self.chat_session = self.model.start_chat(history=gemini_history)
            
            # Send message (Gemini maintains context automatically)
            response = self.chat_session.send_message(user_message)
            
            return response.text
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to rule-based response
            from services.ai_service import simple_chat_response
            return simple_chat_response(user_message)
    
    def chat_stream(self, user_message: str):
        """
        Stream response in real-time (for better UX)
        
        Args:
            user_message: User's question
            
        Yields:
            Text chunks as they're generated
        """
        try:
            response = self.chat_session.send_message(user_message, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"Streaming error: {e}")
            yield f"Error: {str(e)}"
    
    def generate_prediction_explanation(self, plant_a: Dict, plant_b: Dict, 
                                       success_rate: float, shared_traits: List[str]) -> str:
        """
        Generate detailed prediction explanation
        
        Args:
            plant_a: First plant data dict
            plant_b: Second plant data dict
            success_rate: Predicted success rate (0-100)
            shared_traits: List of shared trait names
            
        Returns:
            Comprehensive explanation text
        """
        prompt = f"""Explain this hybridization prediction in comprehensive scientific detail:

🌾 PARENT PLANTS:
Plant A: {plant_a['name']} ({plant_a['commonName']})
Plant B: {plant_b['name']} ({plant_b['commonName']})

📊 PREDICTION RESULTS:
Success Rate: {success_rate}%
Shared Traits: {', '.join(shared_traits)}

📋 PROVIDE ANALYSIS IN THESE SECTIONS:

1. **Genetic Compatibility Analysis**
   - Why this specific success rate was predicted
   - Genome size compatibility ({plant_a.get('genomeSize', 'N/A')} vs {plant_b.get('genomeSize', 'N/A')} Mbp)
   - Trait complementarity and conflicts
   - Chromosomal alignment factors

2. **Environmental Compatibility**
   - Climate zone overlap and adaptation
   - Water and temperature requirements alignment
   - Soil type compatibility
   - Stress resistance profiles

3. **Expected F1 Generation Characteristics**
   - Dominant vs recessive trait predictions
   - Hybrid vigor (heterosis) expectations
   - Yield potential estimation
   - Resistance profile (drought, salinity, disease)

4. **Breeding Recommendations**
   - Which parent should be used as female/male
   - Crossing methodology and timing
   - Selection criteria for F1 and F2 generations
   - Timeline with generational milestones

5. **Potential Challenges & Risks**
   - Technical challenges in crossing
   - Environmental adaptation risks
   - Trait segregation concerns
   - Mitigation strategies

6. **Benefits & Opportunities**
   - Improved traits in offspring
   - Market potential and applications
   - Climate resilience improvements
   - Yield or quality enhancements

Provide specific, data-driven insights with confidence levels and scientific reasoning."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def answer_characteristic_question(self, plant_name: str, question: str) -> str:
        """
        Answer specific questions about plant characteristics
        
        Args:
            plant_name: Name of the plant
            question: User's specific question
            
        Returns:
            Detailed answer
        """
        prompt = f"""Answer this question about {plant_name}:

Question: {question}

Use the plant data from your knowledge base. Provide specific numbers, resistance scores, climate requirements, and any other relevant characteristics."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def reset_conversation(self):
        """Start a new conversation (clear history)"""
        self.chat_session = self.model.start_chat(history=[])
    
    def _convert_history(self, external_history: List[Dict]) -> List[Dict]:
        """
        Convert external conversation history to Gemini format
        
        Args:
            external_history: History from frontend
                             [{"role": "user"/"assistant", "content": "..."}]
        
        Returns:
            Gemini-formatted history
        """
        gemini_history = []
        
        for msg in external_history:
            role = msg.get("role", "")
            content = msg.get("content") or msg.get("text", "")
            
            # Skip empty or "thinking" messages
            if not content or content == "Thinking...":
                continue
            
            # Convert role
            if role == "user":
                gemini_role = "user"
            elif role in ["assistant", "bot", "model"]:
                gemini_role = "model"
            else:
                # Infer from type if present
                msg_type = msg.get("type", "")
                gemini_role = "user" if msg_type == "user" else "model"
            
            gemini_history.append({
                "role": gemini_role,
                "parts": [content]
            })
        
        return gemini_history
    
    def configure(self, temperature: float = None, max_tokens: int = None):
        """
        Dynamically adjust generation parameters
        
        Args:
            temperature: Creativity level (0-1)
            max_tokens: Max response length
        """
        if temperature is not None:
            self.generation_config["temperature"] = temperature
        if max_tokens is not None:
            self.generation_config["max_output_tokens"] = max_tokens
        
        # Recreate model with new config
        self.model = genai.GenerativeModel(
            model_name=self.model._model_name,
            system_instruction=self.system_instruction,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Restart chat session
        self.chat_session = self.model.start_chat(history=[])
