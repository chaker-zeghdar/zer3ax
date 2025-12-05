"""
Chatbot Tools Configuration

This file defines the available tools/functions that the chatbot can use
to provide dynamic responses and interact with the platform's features.
"""

from typing import Dict, List, Optional, Any


# Sample plant data (replace with actual data source)
SAMPLE_PLANTS = [
    {
        "id": 1,
        "name": "Common Wheat",
        "scientific_name": "Triticum aestivum",
        "zone": "Northern",
        "traits": ["drought_resistance", "high_yield", "disease_resistance"]
    },
    {
        "id": 2,
        "name": "Barley",
        "scientific_name": "Hordeum vulgare",
        "zone": "Northern",
        "traits": ["cold_tolerance", "drought_resistance", "adaptability"]
    },
    {
        "id": 3,
        "name": "Durum Wheat",
        "scientific_name": "Triticum durum",
        "zone": "High Plateau",
        "traits": ["high_protein", "drought_resistance", "heat_tolerance"]
    },
    {
        "id": 4,
        "name": "Sorghum",
        "scientific_name": "Sorghum bicolor",
        "zone": "Sahara",
        "traits": ["extreme_drought_resistance", "heat_tolerance", "low_water_needs"]
    }
]


def search_plants(query: str) -> List[Dict[str, Any]]:
    """
    Search for plants by name, scientific name, or zone.
    
    Args:
        query (str): Search term
        
    Returns:
        List[Dict]: List of matching plants
    """
    query_lower = query.lower()
    results = [
        plant for plant in SAMPLE_PLANTS
        if query_lower in plant["name"].lower()
        or query_lower in plant["scientific_name"].lower()
        or query_lower in plant["zone"].lower()
    ]
    return results


def get_plant_details(plant_id: int) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific plant.
    
    Args:
        plant_id (int): Plant ID
        
    Returns:
        Dict: Plant details or None if not found
    """
    for plant in SAMPLE_PLANTS:
        if plant["id"] == plant_id:
            return plant
    return None


def calculate_trait_similarity(plant_a: Dict[str, Any], plant_b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate trait similarity between two plants.
    
    Args:
        plant_a (Dict): First plant
        plant_b (Dict): Second plant
        
    Returns:
        Dict: Similarity analysis with shared traits, unique traits, and similarity percentage
    """
    traits_a = set(plant_a.get("traits", []))
    traits_b = set(plant_b.get("traits", []))
    
    shared_traits = list(traits_a & traits_b)
    unique_to_a = list(traits_a - traits_b)
    unique_to_b = list(traits_b - traits_a)
    union_traits = traits_a | traits_b
    
    similarity = (len(shared_traits) / len(union_traits) * 100) if union_traits else 0
    
    return {
        "shared_traits": shared_traits,
        "similarity": round(similarity, 2),
        "unique_to_a": unique_to_a,
        "unique_to_b": unique_to_b
    }


def get_plants_by_zone(zone: str) -> List[Dict[str, Any]]:
    """
    Get all plants for a specific climate zone.
    
    Args:
        zone (str): Climate zone (Northern, High Plateau, or Sahara)
        
    Returns:
        List[Dict]: List of plants in the zone
    """
    return [
        plant for plant in SAMPLE_PLANTS
        if plant["zone"].lower() == zone.lower()
    ]


def predict_hybridization(plant_a_id: int, plant_b_id: int) -> Optional[Dict[str, Any]]:
    """
    Predict hybridization success between two plants.
    
    Args:
        plant_a_id (int): First plant ID
        plant_b_id (int): Second plant ID
        
    Returns:
        Dict: Prediction results including success rate, confidence, and recommendation
    """
    plant_a = get_plant_details(plant_a_id)
    plant_b = get_plant_details(plant_b_id)
    
    if not plant_a or not plant_b:
        return None
    
    similarity = calculate_trait_similarity(plant_a, plant_b)
    
    # Simulate success rate based on trait similarity and zone compatibility
    zone_bonus = 15 if plant_a["zone"] == plant_b["zone"] else 0
    base_success = similarity["similarity"]
    success_rate = min(95, max(20, base_success + zone_bonus))
    
    # Determine compatibility level
    if success_rate >= 70:
        compatibility = "High"
        recommendation = "These species show high compatibility for hybridization."
    elif success_rate >= 50:
        compatibility = "Moderate"
        recommendation = "Moderate compatibility. Additional testing recommended."
    else:
        compatibility = "Low"
        recommendation = "Low compatibility. Consider alternative combinations."
    
    return {
        "plant_a": plant_a["name"],
        "plant_b": plant_b["name"],
        "success_rate": round(success_rate),
        "confidence": round(0.6 + (similarity["similarity"] / 200), 2),
        "shared_traits": similarity["shared_traits"],
        "compatibility": compatibility,
        "recommendation": recommendation
    }


def get_zone_statistics(zone: str) -> Dict[str, Any]:
    """
    Get statistics about a specific climate zone.
    
    Args:
        zone (str): Climate zone name
        
    Returns:
        Dict: Zone statistics including plant count and common traits
    """
    zone_plants = get_plants_by_zone(zone)
    
    # Extract common traits
    trait_counts = {}
    for plant in zone_plants:
        for trait in plant.get("traits", []):
            trait_counts[trait] = trait_counts.get(trait, 0) + 1
    
    common_traits = [
        {"trait": trait, "count": count}
        for trait, count in trait_counts.items()
        if count >= 2
    ]
    common_traits.sort(key=lambda x: x["count"], reverse=True)
    
    return {
        "zone": zone,
        "plant_count": len(zone_plants),
        "plants": [
            {"name": p["name"], "scientific_name": p["scientific_name"]}
            for p in zone_plants
        ],
        "common_traits": common_traits
    }


def get_recommendations(criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get plant recommendations based on criteria.
    
    Args:
        criteria (Dict): Search criteria with optional keys:
            - zone (str): Climate zone
            - target_trait (str): Desired trait
            - min_success_rate (int): Minimum success rate (default: 50)
            
    Returns:
        List[Dict]: List of recommended plants (top 5)
    """
    zone = criteria.get("zone")
    target_trait = criteria.get("target_trait")
    
    filtered_plants = SAMPLE_PLANTS.copy()
    
    if zone:
        filtered_plants = [
            p for p in filtered_plants
            if p["zone"].lower() == zone.lower()
        ]
    
    if target_trait:
        filtered_plants = [
            p for p in filtered_plants
            if any(target_trait.lower() in trait.lower() for trait in p.get("traits", []))
        ]
    
    return filtered_plants[:5]


def generate_detailed_report(plant_a_id: int, plant_b_id: int) -> Optional[Dict[str, Any]]:
    """
    Generate a comprehensive breeding analysis report for two plants.
    
    Args:
        plant_a_id (int): First plant ID
        plant_b_id (int): Second plant ID
        
    Returns:
        Dict: Detailed report with multiple sections
    """
    plant_a = get_plant_details(plant_a_id)
    plant_b = get_plant_details(plant_b_id)
    
    if not plant_a or not plant_b:
        return None
    
    # Get prediction data
    prediction = predict_hybridization(plant_a_id, plant_b_id)
    similarity = calculate_trait_similarity(plant_a, plant_b)
    
    # Generate comprehensive report
    report = {
        "title": f"Plant Breeding Analysis Report: {plant_a['name']} × {plant_b['name']}",
        
        "executive_summary": {
            "parent_species": [plant_a["name"], plant_b["name"]],
            "scientific_names": [plant_a["scientific_name"], plant_b["scientific_name"]],
            "success_probability": prediction["success_rate"],
            "confidence_level": prediction["confidence"],
            "compatibility_rating": prediction["compatibility"],
            "key_finding": f"The cross between {plant_a['name']} and {plant_b['name']} shows {prediction['compatibility'].lower()} compatibility with a {prediction['success_rate']}% predicted success rate."
        },
        
        "parent_analysis": {
            "plant_a": {
                "name": plant_a["name"],
                "scientific_name": plant_a["scientific_name"],
                "zone": plant_a["zone"],
                "traits": plant_a.get("traits", []),
                "strengths": _analyze_strengths(plant_a),
                "limitations": _analyze_limitations(plant_a)
            },
            "plant_b": {
                "name": plant_b["name"],
                "scientific_name": plant_b["scientific_name"],
                "zone": plant_b["zone"],
                "traits": plant_b.get("traits", []),
                "strengths": _analyze_strengths(plant_b),
                "limitations": _analyze_limitations(plant_b)
            }
        },
        
        "trait_compatibility": {
            "shared_traits": similarity["shared_traits"],
            "similarity_percentage": similarity["similarity"],
            "complementary_traits": _identify_complementary_traits(plant_a, plant_b),
            "potential_conflicts": _identify_conflicts(plant_a, plant_b),
            "trait_interactions": _analyze_trait_interactions(similarity)
        },
        
        "hybridization_prediction": {
            "success_rate": prediction["success_rate"],
            "confidence": prediction["confidence"],
            "genetic_basis": _explain_genetic_basis(plant_a, plant_b, similarity),
            "expected_vigor": _predict_hybrid_vigor(similarity),
            "segregation_pattern": "Expected Mendelian inheritance in F2 generation"
        },
        
        "expected_f1_characteristics": {
            "dominant_traits": _predict_f1_traits(plant_a, plant_b, similarity),
            "yield_prediction": _predict_yield_improvement(similarity),
            "quality_metrics": _predict_quality_traits(plant_a, plant_b),
            "stress_tolerance": _predict_stress_tolerance(plant_a, plant_b)
        },
        
        "improvement_recommendations": {
            "short_term": _generate_short_term_recommendations(plant_a, plant_b, prediction),
            "long_term": _generate_long_term_strategy(plant_a, plant_b, similarity),
            "selection_criteria": _define_selection_criteria(plant_a, plant_b),
            "breeding_timeline": _create_breeding_timeline(prediction["success_rate"])
        },
        
        "environmental_adaptability": {
            "optimal_zones": _determine_optimal_zones(plant_a, plant_b),
            "climate_requirements": _analyze_climate_needs(plant_a, plant_b),
            "soil_preferences": _analyze_soil_requirements(plant_a, plant_b),
            "water_management": _analyze_water_needs(plant_a, plant_b)
        },
        
        "risk_assessment": {
            "technical_risks": _assess_technical_risks(prediction["success_rate"]),
            "environmental_risks": _assess_environmental_risks(plant_a, plant_b),
            "market_risks": _assess_market_risks(plant_a, plant_b),
            "mitigation_strategies": _generate_mitigation_strategies(prediction)
        },
        
        "conclusion": {
            "overall_recommendation": prediction["recommendation"],
            "confidence_level": prediction["compatibility"],
            "next_steps": _generate_next_steps(prediction),
            "expected_timeline": _estimate_timeline(prediction["success_rate"]),
            "investment_priority": _assess_investment_priority(prediction["success_rate"])
        }
    }
    
    return report


# Helper functions for detailed report generation

def _analyze_strengths(plant: Dict[str, Any]) -> List[str]:
    """Analyze and list plant strengths."""
    strengths = []
    traits = plant.get("traits", [])
    
    if "drought_resistance" in traits:
        strengths.append("Excellent drought tolerance for water-scarce conditions")
    if "high_yield" in traits:
        strengths.append("Superior yield potential for commercial production")
    if "disease_resistance" in traits:
        strengths.append("Strong disease resistance reduces chemical inputs")
    if "cold_tolerance" in traits:
        strengths.append("Cold hardiness extends growing season")
    if "heat_tolerance" in traits:
        strengths.append("Heat tolerance suitable for warm climates")
    
    if not strengths:
        strengths.append("Well-adapted to " + plant["zone"] + " climate zone")
    
    return strengths


def _analyze_limitations(plant: Dict[str, Any]) -> List[str]:
    """Analyze potential limitations."""
    limitations = []
    traits = plant.get("traits", [])
    
    if "drought_resistance" not in traits:
        limitations.append("May require consistent irrigation")
    if "disease_resistance" not in traits:
        limitations.append("Susceptibility to common diseases may require monitoring")
    if plant["zone"] == "Northern":
        limitations.append("Limited adaptability to extreme heat conditions")
    
    if not limitations:
        limitations.append("Zone-specific adaptation may limit geographic range")
    
    return limitations


def _identify_complementary_traits(plant_a: Dict, plant_b: Dict) -> List[str]:
    """Identify traits that complement each other."""
    traits_a = set(plant_a.get("traits", []))
    traits_b = set(plant_b.get("traits", []))
    
    complementary = []
    
    # Check for complementary combinations
    if "high_yield" in traits_a and "disease_resistance" in traits_b:
        complementary.append("High yield from parent A + disease resistance from parent B = robust production")
    if "drought_resistance" in traits_a and "heat_tolerance" in traits_b:
        complementary.append("Combined stress tolerance for challenging environments")
    if "cold_tolerance" in traits_a and "adaptability" in traits_b:
        complementary.append("Extended geographic range potential")
    
    if not complementary:
        complementary.append("Shared traits may reinforce beneficial characteristics in offspring")
    
    return complementary


def _identify_conflicts(plant_a: Dict, plant_b: Dict) -> List[str]:
    """Identify potential trait conflicts."""
    conflicts = []
    
    if plant_a["zone"] != plant_b["zone"]:
        conflicts.append(f"Different climate adaptations ({plant_a['zone']} vs {plant_b['zone']}) may require careful F2 selection")
    
    traits_a = set(plant_a.get("traits", []))
    traits_b = set(plant_b.get("traits", []))
    
    if not (traits_a & traits_b):
        conflicts.append("Limited trait overlap may result in variable F1 expression")
    
    if not conflicts:
        conflicts.append("No major conflicts detected - favorable for hybridization")
    
    return conflicts


def _analyze_trait_interactions(similarity: Dict) -> str:
    """Analyze how traits interact genetically."""
    if similarity["similarity"] > 60:
        return "High genetic similarity suggests stable trait inheritance with predictable outcomes."
    elif similarity["similarity"] > 30:
        return "Moderate similarity allows for trait recombination and potential heterosis effects."
    else:
        return "Low similarity may lead to wide segregation in F2; careful selection required."


def _explain_genetic_basis(plant_a: Dict, plant_b: Dict, similarity: Dict) -> str:
    """Explain the genetic basis for prediction."""
    shared = len(similarity["shared_traits"])
    zone_match = plant_a["zone"] == plant_b["zone"]
    
    explanation = f"The prediction is based on {shared} shared genetic traits. "
    
    if zone_match:
        explanation += "Both parents are adapted to the same climate zone, indicating compatible environmental gene networks. "
    
    if shared >= 2:
        explanation += "Multiple shared traits suggest recent common ancestry and high crossability."
    else:
        explanation += "Limited trait overlap suggests genetic distance; F1 may show hybrid vigor but F2 segregation expected."
    
    return explanation


def _predict_hybrid_vigor(similarity: Dict) -> str:
    """Predict heterosis (hybrid vigor) potential."""
    if 30 <= similarity["similarity"] <= 70:
        return "High - Optimal genetic distance for heterosis expression"
    elif similarity["similarity"] > 70:
        return "Moderate - Close relatives may show less heterosis"
    else:
        return "Variable - Wide genetic distance may produce unpredictable results"


def _predict_f1_traits(plant_a: Dict, plant_b: Dict, similarity: Dict) -> List[str]:
    """Predict dominant traits in F1."""
    shared = similarity["shared_traits"]
    predicted_traits = []
    
    for trait in shared:
        predicted_traits.append(f"{trait.replace('_', ' ').title()} (inherited from both parents)")
    
    # Add unique dominant traits
    for trait in similarity["unique_to_a"][:2]:
        predicted_traits.append(f"{trait.replace('_', ' ').title()} (likely from {plant_a['name']})")
    
    return predicted_traits if predicted_traits else ["Variable trait expression expected"]


def _predict_yield_improvement(similarity: Dict) -> str:
    """Predict yield improvements."""
    sim_score = similarity["similarity"]
    
    if sim_score > 60:
        return "Expected 10-20% yield improvement through hybrid vigor"
    elif sim_score > 30:
        return "Expected 15-30% yield improvement with optimal heterosis"
    else:
        return "Variable yield response; selection required in F2"


def _predict_quality_traits(plant_a: Dict, plant_b: Dict) -> Dict[str, str]:
    """Predict quality trait improvements."""
    return {
        "protein_content": "Expected stable or improved based on parent mid-range",
        "grain_quality": "F1 typically shows intermediate to superior quality",
        "nutritional_value": "Combination of parent nutritional profiles"
    }


def _predict_stress_tolerance(plant_a: Dict, plant_b: Dict) -> Dict[str, str]:
    """Predict stress tolerance characteristics."""
    traits_combined = set(plant_a.get("traits", []) + plant_b.get("traits", []))
    
    return {
        "drought": "High" if "drought_resistance" in traits_combined else "Moderate",
        "heat": "High" if "heat_tolerance" in traits_combined else "Moderate",
        "cold": "High" if "cold_tolerance" in traits_combined else "Moderate",
        "disease": "High" if "disease_resistance" in traits_combined else "Requires monitoring"
    }


def _generate_short_term_recommendations(plant_a: Dict, plant_b: Dict, prediction: Dict) -> List[str]:
    """Generate short-term breeding recommendations."""
    recommendations = [
        "Conduct initial test crosses with 20-50 plants",
        f"Monitor F1 for hybrid vigor and {', '.join(prediction['shared_traits'][:2])}",
        "Document phenotypic observations throughout growth cycle",
        "Assess F1 uniformity and performance metrics"
    ]
    
    if prediction["success_rate"] < 60:
        recommendations.append("Consider multiple crossing attempts to ensure success")
    
    return recommendations


def _generate_long_term_strategy(plant_a: Dict, plant_b: Dict, similarity: Dict) -> List[str]:
    """Generate long-term breeding strategy."""
    return [
        "Develop F2 population of 500+ plants for selection",
        "Implement marker-assisted selection for target traits",
        "Conduct multi-location trials across target zones",
        "Establish pure line selection program by F4-F5",
        "Initiate variety registration process after F6 stabilization"
    ]


def _define_selection_criteria(plant_a: Dict, plant_b: Dict) -> Dict[str, str]:
    """Define selection criteria for offspring."""
    return {
        "primary_traits": "Yield, disease resistance, climate adaptation",
        "secondary_traits": "Quality metrics, stress tolerance, maturity period",
        "elimination_criteria": "Severe disease susceptibility, poor vigor, off-types",
        "advancement_threshold": "Top 10% based on multi-trait index"
    }


def _create_breeding_timeline(success_rate: int) -> Dict[str, str]:
    """Create a breeding timeline."""
    base_years = 6 if success_rate > 70 else 7
    
    return {
        "F1_generation": "Year 1 - Initial cross and F1 production",
        "F2_generation": "Year 2 - Population development and initial selection",
        "F3_F4": "Years 3-4 - Line advancement and trait fixation",
        "F5_F6": "Years 5-6 - Yield trials and variety testing",
        "release": f"Year {base_years} - Variety release (subject to trials)"
    }


def _determine_optimal_zones(plant_a: Dict, plant_b: Dict) -> List[str]:
    """Determine optimal climate zones."""
    zones = [plant_a["zone"], plant_b["zone"]]
    
    if plant_a["zone"] == plant_b["zone"]:
        return [plant_a["zone"], "Adjacent transitional zones"]
    else:
        return [f"{plant_a['zone']}", f"{plant_b['zone']}", "Intermediate climate zones"]


def _analyze_climate_needs(plant_a: Dict, plant_b: Dict) -> str:
    """Analyze climate requirements."""
    if "Northern" in [plant_a["zone"], plant_b["zone"]]:
        return "Cool to moderate temperatures (15-25°C), adequate rainfall"
    elif "Sahara" in [plant_a["zone"], plant_b["zone"]]:
        return "High heat tolerance (25-40°C), minimal rainfall, drought-adapted"
    else:
        return "Moderate temperatures (18-28°C), seasonal rainfall patterns"


def _analyze_soil_requirements(plant_a: Dict, plant_b: Dict) -> str:
    """Analyze soil requirements."""
    return "Well-drained loamy soil, pH 6.0-7.5, moderate to high fertility"


def _analyze_water_needs(plant_a: Dict, plant_b: Dict) -> str:
    """Analyze water requirements."""
    traits = set(plant_a.get("traits", []) + plant_b.get("traits", []))
    
    if "drought_resistance" in traits:
        return "Moderate water needs; 300-500mm annual rainfall or supplemental irrigation"
    else:
        return "Regular irrigation required; 500-800mm annual rainfall equivalent"


def _assess_technical_risks(success_rate: int) -> List[Dict[str, str]]:
    """Assess technical risks."""
    risks = []
    
    if success_rate < 60:
        risks.append({
            "risk": "Lower success probability",
            "mitigation": "Increase crossing attempts, use experienced technicians"
        })
    
    risks.append({
        "risk": "F2 segregation variability",
        "mitigation": "Large F2 population (500+ plants) for adequate selection"
    })
    
    return risks


def _assess_environmental_risks(plant_a: Dict, plant_b: Dict) -> List[Dict[str, str]]:
    """Assess environmental risks."""
    return [{
        "risk": "Climate variability",
        "mitigation": "Multi-location testing and adaptive trait selection"
    }, {
        "risk": "Pest and disease pressure",
        "mitigation": "Integrate resistance screening in early generations"
    }]


def _assess_market_risks(plant_a: Dict, plant_b: Dict) -> List[Dict[str, str]]:
    """Assess market risks."""
    return [{
        "risk": "Market acceptance of new variety",
        "mitigation": "Farmer participatory trials and early stakeholder engagement"
    }, {
        "risk": "Competing varieties",
        "mitigation": "Focus on unique trait combinations and performance advantages"
    }]


def _generate_mitigation_strategies(prediction: Dict) -> List[str]:
    """Generate overall mitigation strategies."""
    return [
        "Implement rigorous quality control throughout breeding process",
        "Maintain genetic diversity in breeding populations",
        "Use molecular markers for trait validation",
        "Conduct regular performance evaluations",
        "Establish backup crosses for genetic security"
    ]


def _generate_next_steps(prediction: Dict) -> List[str]:
    """Generate actionable next steps."""
    steps = [
        "Review parent materials and confirm trait characterization",
        "Plan crossing schedule and resource allocation",
        "Prepare field plots and experimental design"
    ]
    
    if prediction["success_rate"] > 70:
        steps.append("Proceed with confidence to large-scale crossing program")
    else:
        steps.append("Consider pilot crosses before full-scale program")
    
    return steps


def _estimate_timeline(success_rate: int) -> str:
    """Estimate breeding timeline."""
    years = 6 if success_rate > 70 else 7
    return f"{years}-{years+2} years from initial cross to variety release"


def _assess_investment_priority(success_rate: int) -> str:
    """Assess investment priority."""
    if success_rate >= 80:
        return "High Priority - Excellent success probability justifies immediate investment"
    elif success_rate >= 60:
        return "Medium-High Priority - Good success probability with managed risk"
    elif success_rate >= 40:
        return "Medium Priority - Consider as part of diversified breeding portfolio"
    else:
        return "Low Priority - High risk; recommend alternative crosses"


# Chatbot Tools Registry
# Maps tool names to their implementations and metadata
chatbot_tools = {
    "search_plants": {
        "name": "search_plants",
        "description": "Search for plants by name, scientific name, or zone",
        "parameters": {
            "query": {"type": "string", "description": "Search term"}
        },
        "execute": search_plants
    },
    
    "get_plant_details": {
        "name": "get_plant_details",
        "description": "Get detailed information about a specific plant",
        "parameters": {
            "plant_id": {"type": "integer", "description": "Plant ID"}
        },
        "execute": get_plant_details
    },
    
    "calculate_trait_similarity": {
        "name": "calculate_trait_similarity",
        "description": "Calculate trait similarity between two plants",
        "parameters": {
            "plant_a": {"type": "object", "description": "First plant"},
            "plant_b": {"type": "object", "description": "Second plant"}
        },
        "execute": calculate_trait_similarity
    },
    
    "get_plants_by_zone": {
        "name": "get_plants_by_zone",
        "description": "Get all plants for a specific climate zone",
        "parameters": {
            "zone": {"type": "string", "description": "Climate zone (Northern, High Plateau, or Sahara)"}
        },
        "execute": get_plants_by_zone
    },
    
    "predict_hybridization": {
        "name": "predict_hybridization",
        "description": "Predict hybridization success between two plants",
        "parameters": {
            "plant_a_id": {"type": "integer", "description": "First plant ID"},
            "plant_b_id": {"type": "integer", "description": "Second plant ID"}
        },
        "execute": predict_hybridization
    },
    
    "get_zone_statistics": {
        "name": "get_zone_statistics",
        "description": "Get statistics about a climate zone",
        "parameters": {
            "zone": {"type": "string", "description": "Climate zone"}
        },
        "execute": get_zone_statistics
    },
    
    "get_recommendations": {
        "name": "get_recommendations",
        "description": "Get plant recommendations based on criteria",
        "parameters": {
            "criteria": {
                "type": "object",
                "description": "Search criteria (zone, target_trait, min_success_rate)"
            }
        },
        "execute": get_recommendations
    },
    
    "generate_detailed_report": {
        "name": "generate_detailed_report",
        "description": "Generate comprehensive breeding analysis report with characteristics analysis and improvement recommendations",
        "parameters": {
            "plant_a_id": {"type": "integer", "description": "First plant ID"},
            "plant_b_id": {"type": "integer", "description": "Second plant ID"}
        },
        "execute": generate_detailed_report
    }
}


def get_tool(tool_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a tool by name.
    
    Args:
        tool_name (str): Name of the tool
        
    Returns:
        Dict: Tool information or None if not found
    """
    return chatbot_tools.get(tool_name)


def execute_tool(tool_name: str, **kwargs) -> Any:
    """
    Execute a tool by name with the given parameters.
    
    Args:
        tool_name (str): Name of the tool to execute
        **kwargs: Tool parameters
        
    Returns:
        Any: Tool execution result
        
    Raises:
        ValueError: If tool not found
    """
    tool = get_tool(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found")
    
    return tool["execute"](**kwargs)
