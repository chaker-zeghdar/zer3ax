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
    
    # RANKING QUESTIONS
    elif kw["type"] == "ranking":
        if "drought" in kw["traits"]:
            sorted_p = sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True)
            resp.append("**Top 3 for Drought Resistance:**\n")
            for i, p in enumerate(sorted_p[:3], 1):
                resp.append(f"{i}. {p['commonName']}: {p['resistance']['drought']}/10\n")
        elif "yield" in kw["traits"]:
            sorted_p = sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True)
            resp.append("**Top 3 for Yield:**\n")
            for i, p in enumerate(sorted_p[:3], 1):
                resp.append(f"{i}. {p['commonName']}: {p['yieldPotential']}/10\n")
    
    # RECOMMENDATION QUESTIONS
    elif kw["type"] == "recommendation":
        if "drought" in q or "dry" in q:
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
            resp.append("**Drought Resistance Rankings:**\n")
            for p in sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True):
                resp.append(f"- {p['commonName']}: {p['resistance']['drought']}/10\n")
        elif trait == "yield":
            resp.append("**Yield Potential Rankings:**\n")
            for p in sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True):
                resp.append(f"- {p['commonName']}: {p['yieldPotential']}/10\n")
    
    # FALLBACK
    if not resp:
        resp.append("**Available Plants:**\n")
        for p in PLANTS_DATA:
            resp.append(f"- {p['commonName']} ({p['optimalZone']})\n")
        resp.append("\nAsk me about any plant, zone, or trait!")
    
    return "".join(resp)
