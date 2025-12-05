"""
Intelligent Keyword-Based Tools for Plant Breeding Chatbot
Answers ANY question using mock data with smart keyword extraction
"""

from typing import Dict, Any, List, Callable


class ToolRegistry:
    """Registry for chatbot tools/functions"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_definitions: List[Dict] = []
    
    def register(self, name: str, description: str, parameters: Dict):
        """Register a new tool"""
        def decorator(func: Callable):
            self.tools[name] = func
            self.tool_definitions.append({
                "name": name,
                "description": description,
                "parameters": parameters
            })
            return func
        return decorator
    
    def execute(self, name: str, **kwargs) -> Any:
        """Execute a tool by name"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        return self.tools[name](**kwargs)
    
    def get_definitions(self) -> List[Dict]:
        """Get all tool definitions for AI"""
        return self.tool_definitions


# Initialize tool registry
tool_registry = ToolRegistry()


# ========================================
# MOCK DATA FROM DASHBOARD
# ========================================

PLANTS_DATA = [
    {
        "id": 1, "name": "Triticum aestivum", "commonName": "Bread Wheat", "icon": "🌾",
        "genomeSize": 17000, "rainfall": "400-600mm", "temperature": "15-25°C",
        "droughtTolerance": "Moderate", "resistance": {"drought": 6, "salinity": 4, "disease": 7},
        "optimalZone": "Northern", "yieldPotential": 8, "geneticDiversity": 7
    },
    {
        "id": 2, "name": "Hordeum vulgare", "commonName": "Barley", "icon": "🌾",
        "genomeSize": 5100, "rainfall": "300-500mm", "temperature": "12-22°C",
        "droughtTolerance": "High", "resistance": {"drought": 8, "salinity": 7, "disease": 6},
        "optimalZone": "High Plateau", "yieldPotential": 7, "geneticDiversity": 6
    },
    {
        "id": 3, "name": "Zea mays", "commonName": "Corn", "icon": "🌽",
        "genomeSize": 2300, "rainfall": "500-800mm", "temperature": "20-30°C",
        "droughtTolerance": "Low", "resistance": {"drought": 4, "salinity": 3, "disease": 5},
        "optimalZone": "Northern", "yieldPotential": 9, "geneticDiversity": 8
    },
    {
        "id": 4, "name": "Sorghum bicolor", "commonName": "Sorghum", "icon": "🌾",
        "genomeSize": 730, "rainfall": "400-600mm", "temperature": "25-35°C",
        "droughtTolerance": "Very High", "resistance": {"drought": 9, "salinity": 6, "disease": 7},
        "optimalZone": "Sahara", "yieldPotential": 7, "geneticDiversity": 8
    },
    {
        "id": 5, "name": "Triticum durum", "commonName": "Durum Wheat", "icon": "🌾",
        "genomeSize": 12000, "rainfall": "350-550mm", "temperature": "15-25°C",
        "droughtTolerance": "Moderate", "resistance": {"drought": 7, "salinity": 5, "disease": 6},
        "optimalZone": "High Plateau", "yieldPotential": 7, "geneticDiversity": 6
    },
    {
        "id": 6, "name": "Medicago sativa", "commonName": "Alfalfa", "icon": "🌿",
        "genomeSize": 900, "rainfall": "450-750mm", "temperature": "15-28°C",
        "droughtTolerance": "Moderate", "resistance": {"drought": 7, "salinity": 6, "disease": 7},
        "optimalZone": "Northern", "yieldPotential": 8, "geneticDiversity": 7
    }
]

ZONES_DATA = [
    {
        "name": "Northern", "rainfall": "400-800mm", "temperature": "10-30°C",
        "soil": "Clay-loam, fertile", "bestPlants": ["Bread Wheat", "Corn", "Alfalfa"], "suitability": 8.5
    },
    {
        "name": "High Plateau", "rainfall": "200-400mm", "temperature": "5-35°C",
        "soil": "Sandy-loam, alkaline", "bestPlants": ["Barley", "Durum Wheat", "Sorghum"], "suitability": 7.2
    },
    {
        "name": "Sahara", "rainfall": "50-200mm", "temperature": "15-45°C",
        "soil": "Sandy, poor organic matter", "bestPlants": ["Sorghum"], "suitability": 4.8
    }
]


# ========================================
# KEYWORD EXTRACTION
# ========================================

def extract_keywords(question: str) -> Dict:
    """Extract keywords from question"""
    q = question.lower()
    
    # Extract plant names (more flexible matching)
    plants = []
    for p in PLANTS_DATA:
        # Check common name and scientific name
        if (p["commonName"].lower() in q or 
            p["name"].lower() in q or
            any(word in q for word in p["commonName"].lower().split()) or
            "wheat" in q and "wheat" in p["commonName"].lower() or
            "barley" in q and p["commonName"] == "Barley" or
            "corn" in q and p["commonName"] == "Corn" or
            "sorghum" in q and p["commonName"] == "Sorghum" or
            "alfalfa" in q and p["commonName"] == "Alfalfa"):
            plants.append(p["commonName"])
    
    # Extract zones
    zones = []
    if "northern" in q or "coastal" in q or "north" in q: zones.append("Northern")
    if "plateau" in q or "high plateau" in q: zones.append("High Plateau")
    if "sahara" in q or "southern" in q or "desert" in q or "south" in q: zones.append("Sahara")
    
    # Extract traits
    traits = []
    for trait in ["drought", "salinity", "disease", "yield", "genome", "rainfall", "temperature"]:
        if trait in q:
            traits.append(trait)
    
    # Question type
    qtype = "general"
    if any(w in q for w in ["best", "recommend"]): qtype = "recommendation"
    elif any(w in q for w in ["highest", "most", "rank"]): qtype = "ranking"
    elif any(w in q for w in ["compare", "vs", "difference"]): qtype = "comparison"
    elif any(w in q for w in ["what", "tell", "about", "info"]): qtype = "what"
    
    return {"plants": plants, "zones": zones, "traits": traits, "type": qtype, "original": question}


# ========================================
# INTELLIGENT ANSWER TOOL
# ========================================

@tool_registry.register(
    name="answer_question",
    description="Answer ANY question about plants, zones, traits using keyword extraction",
    parameters={
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "User's question"}
        },
        "required": ["question"]
    }
)
def answer_question(question: str) -> str:
    """Intelligently answer questions using keyword-based matching"""
    kw = extract_keywords(question)
    q = question.lower()
    resp = []
    
    # COMPARISON QUESTIONS (compare X with Y / compare it with X)
    if "compare" in q or "vs" in q or "versus" in q or kw["type"] == "comparison":
        if len(kw["plants"]) >= 2:
            # Compare two plants
            p1 = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][0]), None)
            p2 = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][1]), None)
            if p1 and p2:
                resp.append(f"**{p1['commonName']} vs {p2['commonName']}**\n\n")
                resp.append(f"{p1['icon']} **{p1['commonName']}:**\n")
                resp.append(f"  • Drought: {p1['resistance']['drought']}/10\n")
                resp.append(f"  • Yield: {p1['yieldPotential']}/10\n")
                resp.append(f"  • Zone: {p1['optimalZone']}\n\n")
                resp.append(f"{p2['icon']} **{p2['commonName']}:**\n")
                resp.append(f"  • Drought: {p2['resistance']['drought']}/10\n")
                resp.append(f"  • Yield: {p2['yieldPotential']}/10\n")
                resp.append(f"  • Zone: {p2['optimalZone']}\n\n")
                
                # Winner
                if p1['resistance']['drought'] > p2['resistance']['drought']:
                    resp.append(f"✅ {p1['commonName']} is better for drought\n")
                else:
                    resp.append(f"✅ {p2['commonName']} is better for drought\n")
                if p1['yieldPotential'] > p2['yieldPotential']:
                    resp.append(f"✅ {p1['commonName']} has higher yield\n")
                else:
                    resp.append(f"✅ {p2['commonName']} has higher yield\n")
                return "".join(resp)
    
    # BETTER/WHICH QUESTIONS
    if "better" in q or ("which" in q and ("one" in q or "is" in q)):
        # Extract target trait or plant
        if kw["plants"]:
            # "which one is better for corn" - means compare FOR corn (corn production/crossing)
            target_plant = kw["plants"][0]
            plant = next((p for p in PLANTS_DATA if p["commonName"] == target_plant), None)
            if plant:
                resp.append(f"**For crossing/breeding with {plant['commonName']}:**\n\n")
                resp.append(f"Best compatibility partners would be plants from similar zones:\n")
                similar_zone = [p for p in PLANTS_DATA if p["optimalZone"] == plant["optimalZone"] and p["commonName"] != plant["commonName"]]
                for p in similar_zone[:3]:
                    resp.append(f"• {p['commonName']} (same {p['optimalZone']} zone, yield: {p['yieldPotential']}/10)\n")
                return "".join(resp)
        elif "drought" in q:
            best = max(PLANTS_DATA, key=lambda p: p["resistance"]["drought"])
            resp.append(f"✅ **Best for drought:** {best['commonName']} ({best['resistance']['drought']}/10)\n")
            return "".join(resp)
        elif "yield" in q:
            best = max(PLANTS_DATA, key=lambda p: p["yieldPotential"])
            resp.append(f"✅ **Best for yield:** {best['commonName']} ({best['yieldPotential']}/10)\n")
            return "".join(resp)
    
    # CHARACTERISTIC/TRAIT QUESTIONS
    if "characteristic" in q or "traits" in q or "properties" in q:
        if kw["plants"]:
            plant = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][0]), None)
            if plant:
                resp.append(f"**{plant['commonName']} Characteristics:**\n")
                resp.append(f"• Genome: {plant['genomeSize']:,} Mbp\n")
                resp.append(f"• Climate: {plant['temperature']}, {plant['rainfall']}\n")
                resp.append(f"• Drought Resistance: {plant['resistance']['drought']}/10\n")
                resp.append(f"• Salinity Resistance: {plant['resistance']['salinity']}/10\n")
                resp.append(f"• Disease Resistance: {plant['resistance']['disease']}/10\n")
                resp.append(f"• Yield Potential: {plant['yieldPotential']}/10\n")
                resp.append(f"• Optimal Zone: {plant['optimalZone']}\n")
                return "".join(resp)
        else:
            # Generic characteristics question
            resp.append("Available plant characteristics:\n")
            resp.append("• Genome size, Climate needs, Drought/Salinity/Disease resistance\n")
            resp.append("• Yield potential, Optimal zone\n\n")
            resp.append("Ask: 'What are the characteristics of [plant name]?'")
            return "".join(resp)
    
    # RANKING QUESTIONS ("what is the ranking of X")
    if "ranking" in q:
        if kw["plants"]:
            plant = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][0]), None)
            if plant:
                sorted_drought = sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True)
                sorted_yield = sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True)
                drought_rank = sorted_drought.index(plant) + 1
                yield_rank = sorted_yield.index(plant) + 1
                
                resp.append(f"**{plant['commonName']} Rankings:**\n")
                resp.append(f"• Drought: #{drought_rank}/{len(PLANTS_DATA)} ({plant['resistance']['drought']}/10)\n")
                resp.append(f"• Yield: #{yield_rank}/{len(PLANTS_DATA)} ({plant['yieldPotential']}/10)\n")
                resp.append(f"• Salinity: {plant['resistance']['salinity']}/10\n")
                resp.append(f"• Disease: {plant['resistance']['disease']}/10\n")
                return "".join(resp)
    
    # PLANT-SPECIFIC QUESTIONS
    if kw["plants"]:
        plant = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][0]), None)
        if plant:
            resp.append(f"**{plant['commonName']} ({plant['name']}) {plant['icon']}**\n")
            resp.append(f"- Genome: {plant['genomeSize']:,} Mbp\n")
            resp.append(f"- Climate: {plant['temperature']}, {plant['rainfall']} rainfall\n")
            resp.append(f"- Drought: {plant['resistance']['drought']}/10 ({plant['droughtTolerance']})\n")
            resp.append(f"- Salinity: {plant['resistance']['salinity']}/10\n")
            resp.append(f"- Yield: {plant['yieldPotential']}/10\n")
            resp.append(f"- Zone: {plant['optimalZone']}\n")
    
    # ZONE-SPECIFIC QUESTIONS
    elif kw["zones"]:
        zone = next((z for z in ZONES_DATA if z["name"] == kw["zones"][0]), None)
        if zone:
            resp.append(f"**{zone['name']} Zone**\n")
            resp.append(f"- Rainfall: {zone['rainfall']}\n")
            resp.append(f"- Temperature: {zone['temperature']}\n")
            resp.append(f"- Best Plants: {', '.join(zone['bestPlants'])}\n")
            resp.append(f"- Suitability: {zone['suitability']}/10\n")
    
    # RANKING BY TRAIT
    elif kw["type"] == "ranking":
        if "drought" in kw["traits"]:
            sorted_p = sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True)
            resp.append("**Drought Resistance Rankings:**\n")
            for i, p in enumerate(sorted_p, 1):
                resp.append(f"{i}. {p['commonName']}: {p['resistance']['drought']}/10\n")
        elif "yield" in kw["traits"]:
            sorted_p = sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True)
            resp.append("**Yield Rankings:**\n")
            for i, p in enumerate(sorted_p, 1):
                resp.append(f"{i}. {p['commonName']}: {p['yieldPotential']}/10\n")
    
    # RECOMMENDATION QUESTIONS
    elif kw["type"] == "recommendation":
        if "drought" in q:
            best = max(PLANTS_DATA, key=lambda p: p["resistance"]["drought"])
            resp.append(f"**Best for Drought:** {best['commonName']} ({best['resistance']['drought']}/10)\n")
        elif kw["zones"]:
            zone = next((z for z in ZONES_DATA if z["name"] == kw["zones"][0]), None)
            if zone:
                resp.append(f"**Recommended for {zone['name']}:** {', '.join(zone['bestPlants'])}\n")
    
    # TRAIT QUESTIONS
    elif kw["traits"]:
        trait = kw["traits"][0]
        if trait == "drought":
            resp.append("**Drought Resistance:**\n")
            for p in sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True):
                resp.append(f"- {p['commonName']}: {p['resistance']['drought']}/10\n")
        elif trait == "yield":
            resp.append("**Yield Potential:**\n")
            for p in sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True):
                resp.append(f"- {p['commonName']}: {p['yieldPotential']}/10\n")
    
    # FALLBACK
    if not resp:
        resp.append("I can help with:\n")
        resp.append("• Plant info: 'What is wheat?'\n")
        resp.append("• Rankings: 'What is the ranking of sorghum?'\n")
        resp.append("• Characteristics: 'What are the characteristics?'\n")
        resp.append("• Comparisons: 'Compare wheat with barley'\n")
        resp.append("• Best plants: 'Which is better for drought?'\n")
        resp.append("\nAvailable: Bread Wheat, Barley, Corn, Sorghum, Durum Wheat, Alfalfa")
    
    return "".join(resp)
