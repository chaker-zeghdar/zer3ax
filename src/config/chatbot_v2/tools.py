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
    """Extract keywords from question - works with ANY language and even single words"""
    q = question.lower()
    
    # Extract plant names (more flexible matching - works with partial names)
    plants = []
    for p in PLANTS_DATA:
        common_lower = p["commonName"].lower()
        name_lower = p["name"].lower()
        
        # Match full names or partial words
        if (common_lower in q or name_lower in q or
            any(word in q for word in common_lower.split()) or
            any(word in q for word in name_lower.split())):
            plants.append(p["commonName"])
            continue
            
        # Single word matching for each plant
        if "wheat" in q or "blé" in q or "قمح" in q:
            if "wheat" in common_lower:
                plants.append(p["commonName"])
        elif "barley" in q or "orge" in q or "شعير" in q:
            if "barley" in common_lower:
                plants.append(p["commonName"])
        elif "corn" in q or "maïs" in q or "ذرة" in q:
            if "corn" in common_lower:
                plants.append(p["commonName"])
        elif "sorghum" in q or "sorgo" in q or "ذرة رفيعة" in q:
            if "sorghum" in common_lower:
                plants.append(p["commonName"])
        elif "alfalfa" in q or "luzerne" in q or "فصة" in q:
            if "alfalfa" in common_lower:
                plants.append(p["commonName"])
    
    # Remove duplicates
    plants = list(dict.fromkeys(plants))
    
    # Extract zones (multi-language)
    zones = []
    if any(w in q for w in ["northern", "north", "coastal", "nord", "côtier", "شمال"]):
        zones.append("Northern")
    if any(w in q for w in ["plateau", "high plateau", "hauts plateaux", "الهضاب"]):
        zones.append("High Plateau")
    if any(w in q for w in ["sahara", "southern", "south", "desert", "sud", "صحراء", "جنوب"]):
        zones.append("Sahara")
    
    # Extract traits (multi-language)
    traits = []
    trait_keywords = {
        "drought": ["drought", "dry", "sécheresse", "sec", "جفاف"],
        "salinity": ["salinity", "salt", "salinité", "sel", "ملوحة"],
        "disease": ["disease", "resistance", "maladie", "résistance", "مرض", "مقاومة"],
        "yield": ["yield", "production", "rendement", "إنتاج"],
        "genome": ["genome", "génome", "جينوم"],
        "rainfall": ["rain", "rainfall", "pluie", "précipitation", "أمطار"],
        "temperature": ["temperature", "temp", "température", "حرارة"]
    }
    
    for trait, keywords in trait_keywords.items():
        if any(kw in q for kw in keywords):
            traits.append(trait)
    
    # Detect question type (multi-language intent detection)
    qtype = "general"
    
    # Recommendation
    if any(w in q for w in ["best", "recommend", "meilleur", "recommand", "أفضل", "نصح"]):
        qtype = "recommendation"
    
    # Ranking
    elif any(w in q for w in ["rank", "ranking", "position", "classement", "ترتيب"]):
        qtype = "ranking"
    
    # Comparison
    elif any(w in q for w in ["compare", "vs", "versus", "comparer", "مقارنة"]):
        qtype = "comparison"
    
    # What/Tell/Info questions
    elif any(w in q for w in ["what", "tell", "about", "info", "describe", "qu'est", "quoi", "ماذا", "ما هو"]):
        qtype = "what"
    
    # Characteristics
    elif any(w in q for w in ["characteristic", "trait", "property", "caractéristique", "propriété", "خصائص"]):
        qtype = "characteristics"
    
    # Single word handling - if just a plant name or trait
    if len(q.split()) <= 2 and (plants or traits or zones):
        if plants:
            qtype = "what"  # Single word plant = tell me about it
        elif traits:
            qtype = "ranking"  # Single word trait = show rankings
    
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
    
    # SINGLE WORD OR FRAGMENT (just "wheat", "drought", "g", etc.)
    if len(question.strip().split()) <= 2:
        # Single plant name
        if kw["plants"] and not kw["traits"]:
            plant = next((p for p in PLANTS_DATA if p["commonName"] == kw["plants"][0]), None)
            if plant:
                resp.append(f"**{plant['commonName']} {plant['icon']}**\n")
                resp.append(f"• Drought: {plant['resistance']['drought']}/10\n")
                resp.append(f"• Yield: {plant['yieldPotential']}/10\n")
                resp.append(f"• Zone: {plant['optimalZone']}\n")
                resp.append(f"• Genome: {plant['genomeSize']:,} Mbp\n")
                return "".join(resp)
        
        # Single trait word
        elif kw["traits"] and not kw["plants"]:
            trait = kw["traits"][0]
            if trait == "drought":
                sorted_p = sorted(PLANTS_DATA, key=lambda p: p["resistance"]["drought"], reverse=True)
                resp.append("**Drought Resistance:**\n")
                for i, p in enumerate(sorted_p, 1):
                    resp.append(f"{i}. {p['commonName']}: {p['resistance']['drought']}/10\n")
                return "".join(resp)
            elif trait == "yield":
                sorted_p = sorted(PLANTS_DATA, key=lambda p: p["yieldPotential"], reverse=True)
                resp.append("**Yield Potential:**\n")
                for i, p in enumerate(sorted_p, 1):
                    resp.append(f"{i}. {p['commonName']}: {p['yieldPotential']}/10\n")
                return "".join(resp)
        
        # Random letters like "g" - show help
        elif not kw["plants"] and not kw["traits"] and not kw["zones"]:
            resp.append("I can help with:\n")
            resp.append("• Just say plant name: 'wheat', 'sorghum'\n")
            resp.append("• Or trait: 'drought', 'yield'\n")
            resp.append("• Or ask: 'ranking of sorghum', 'compare wheat barley'\n")
            resp.append("\nPlants: Wheat, Barley, Corn, Sorghum, Alfalfa")
            return "".join(resp)
    
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
