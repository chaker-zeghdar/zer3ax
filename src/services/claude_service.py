"""
Claude AI Service for Zer3aZ Chatbot
Provides intelligent responses using Anthropic's Claude API with domain-specific knowledge
"""

import anthropic
import os
from typing import List, Dict, Optional


class ClaudeChatbotService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude chatbot service
        
        Args:
            api_key: Anthropic API key (if None, tries to get from environment)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not provided and not found in environment")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.conversation_history = []
        
    def get_system_prompt(self) -> str:
        """Generate comprehensive system prompt with domain knowledge"""
        
        from config.chatbot_tools import COMPREHENSIVE_PLANTS, ALGERIA_ZONES
        
        # Build plant database description
        plants_data = []
        for plant in COMPREHENSIVE_PLANTS:
            plant_info = f"""
{plant['name']} ({plant['scientific_name']}) {plant.get('icon', '')}
- Genome Size: {plant['genome_size']:,} Mbp
- Climate Zone: {plant['zone']}
- Environmental Needs: {plant['environmental_factor']['temperature']}, {plant['environmental_factor']['rainfall']} rainfall
- Drought Tolerance: {plant['environmental_factor']['drought_tolerance']} ({plant['resistance']['drought']}/10)
- Salinity Resistance: {plant['resistance']['salinity']}/10
- Disease Resistance: {plant['resistance']['disease']}/10
- Yield Potential: {plant['yield_potential']}/10
- Genetic Diversity: {plant['genetic_diversity']}/10
- Soil Preference: {plant['soil_preference']}
- Pollination: {plant['pollination_type']}
- Growth Form: {plant['growth_form']}, {plant['perenniality']}
- Root Depth: {plant['root_depth']}
- Key Traits: {', '.join(plant['traits'][:5])}
"""
            plants_data.append(plant_info.strip())
        
        # Build zone database description
        zones_data = []
        for zone in ALGERIA_ZONES:
            zone_info = f"""
{zone['full_name']}
- Climate: {zone['climate']['rainfall']} rainfall, {zone['climate']['temperature']}, {zone['climate']['humidity']} humidity
- Soil Type: {zone['soil_type']}
- Suitability Score: {zone['suitability_score']}/10
- Stress Factors: {', '.join(zone['stress_factors'])}
- Best Plants: {', '.join([p['name'] for p in COMPREHENSIVE_PLANTS if p['id'] in zone['best_plants']])}
"""
            zones_data.append(zone_info.strip())
        
        system_prompt = f"""You are an expert AI Plant Breeding Scientist and Agricultural Consultant specialized in the Zer3aZ platform.

YOUR KNOWLEDGE BASE - PLANT DATABASE ({len(COMPREHENSIVE_PLANTS)} species):

{chr(10).join(plants_data)}

CLIMATE ZONES DATABASE ({len(ALGERIA_ZONES)} Algeria zones):

{chr(10).join(zones_data)}

YOUR CAPABILITIES:
🔍 **Search & Information**
- Provide detailed profiles for any plant (genome, traits, resistance, environmental needs)
- Explain growth requirements and climate suitability
- Compare disease, drought, and salinity resistance across species

🔄 **Comparisons**
- Compare any two plants side-by-side (traits, genome size, resistance, zones)
- Explain differences and trade-offs between species
- Recommend which is better for specific conditions

🎯 **Recommendations**
- Suggest best plants based on climate zone, soil type, stress conditions
- Rank plants by drought resistance, yield potential, salinity tolerance, etc.
- Provide zone-specific cultivation advice

📋 **Data Analysis**
- List plants by any criteria (genome size, genetic diversity, resistance scores)
- Show rankings and statistics
- Identify trends and patterns in the database

🧬 **Breeding & Predictions**
- Predict hybridization success rates based on genetic compatibility
- Analyze trait inheritance and F1 generation characteristics
- Provide breeding recommendations and timelines

📊 **Statistics & Trends**
- Share platform usage statistics
- Identify most popular species
- Report on prediction success rates

YOUR RESPONSE STYLE:
✅ **Always reference actual data** - Use specific numbers from the database (genome sizes, resistance scores, climate ranges)
✅ **Be precise** - "Sorghum has 9/10 drought resistance" not "Sorghum is drought tolerant"
✅ **Provide context** - Explain WHY a plant is suitable, not just that it is
✅ **Use clear formatting** - Bullet points, sections, comparisons tables when helpful
✅ **Be conversational** - Friendly and professional, use emojis (🌾 🔍 🎯 📊) sparingly
✅ **Cite zone data** - Reference rainfall amounts, temperature ranges, soil types
✅ **Compare intelligently** - When asked about "best", explain trade-offs
✅ **Admit limitations** - If data isn't available, say so and offer alternatives

EXAMPLES OF GOOD RESPONSES:

Question: "What's best for drought?"
Good Answer: "For drought conditions, I recommend:

1. **Sorghum** - 9/10 drought resistance (Very High tolerance)
   - Requires only 400-600mm rainfall
   - Thrives in Sahara zone (50-200mm rainfall)
   - Small genome (730 Mbp) makes it efficient

2. **Barley** - 8/10 drought resistance (High tolerance)
   - Needs 300-500mm rainfall
   - Suited for High Plateau zone
   - Also has excellent salinity tolerance (7/10)

3. **Durum Wheat** - 7/10 drought resistance (Moderate)
   - Requires 300-450mm rainfall
   - Good for High Plateau
   - Higher yield potential than Sorghum (7/10 vs 7/10)"

Question: "Compare wheat and barley"
Good Answer: "**Bread Wheat vs Barley Comparison:**

**Genome & Genetics**
- Wheat: 17,000 Mbp (large genome)
- Barley: 5,100 Mbp (medium genome)

**Climate Adaptation**
- Wheat: Northern zone, 400-600mm rainfall, 15-25°C
- Barley: High Plateau, 300-500mm rainfall, 12-22°C

**Stress Resistance**
- Drought: Barley wins (8/10 vs 6/10)
- Salinity: Barley wins (7/10 vs 4/10)
- Disease: Wheat wins (7/10 vs 6/10)

**Yield & Production**
- Wheat: 8/10 yield potential
- Barley: 7/10 yield potential

**Best Use Cases**
- Choose Wheat for: Higher yields in favorable conditions, Northern coastal areas
- Choose Barley for: Stress tolerance, marginal lands, High Plateau, saline soils"

IMPORTANT RULES:
❌ Don't make up data - Only use the plant and zone information provided above
❌ Don't be vague - Always include specific numbers and scores
❌ Don't ignore the question - Answer what was actually asked
❌ Don't overcomplicate - Keep explanations clear and actionable
✅ Always prioritize accuracy and helpfulness
✅ If unsure, ask clarifying questions
✅ When multiple interpretations exist, address the most likely one

You are helping farmers, researchers, and agricultural professionals make informed decisions. Your answers can directly impact crop selection and breeding programs."""

        return system_prompt
    
    def chat(self, user_message: str, conversation_history: Optional[List[Dict]] = None,
             temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Send a message and get a response
        
        Args:
            user_message: User's question
            conversation_history: Previous messages (optional)
            temperature: Response creativity (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Assistant's response
        """
        # Use provided history or internal history
        if conversation_history:
            # Convert from frontend format to Claude format
            messages = []
            for msg in conversation_history:
                role = "user" if msg.get("role") == "user" or msg.get("type") == "user" else "assistant"
                content = msg.get("content") or msg.get("text", "")
                if content and content != "Thinking...":  # Skip typing indicators
                    messages.append({"role": role, "content": content})
        else:
            messages = self.conversation_history.copy()
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            system=self.get_system_prompt(),
            messages=messages
        )
        
        # Extract response text
        assistant_message = response.content[0].text
        
        # Update internal history
        self.conversation_history = messages
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history
