/**
 * Chatbot Tools Configuration
 * 
 * This file defines the available tools/functions that the chatbot can use
 * to provide dynamic responses and interact with the platform's features.
 */

import { plants } from '../data/mockData';

/**
 * Tool: Search Plants
 * Searches for plants by name or characteristics
 */
export const searchPlants = (query) => {
  const lowerQuery = query.toLowerCase();
  return plants.filter(plant => 
    plant.name.toLowerCase().includes(lowerQuery) ||
    plant.scientificName.toLowerCase().includes(lowerQuery) ||
    plant.zone.toLowerCase().includes(lowerQuery)
  );
};

/**
 * Tool: Get Plant Details
 * Retrieves detailed information about a specific plant
 */
export const getPlantDetails = (plantId) => {
  return plants.find(plant => plant.id === plantId);
};

/**
 * Tool: Calculate Trait Similarity
 * Calculates similarity between two plants based on traits
 */
export const calculateTraitSimilarity = (plantA, plantB) => {
  const traitsA = new Set(plantA.traits || []);
  const traitsB = new Set(plantB.traits || []);
  
  const intersection = [...traitsA].filter(trait => traitsB.has(trait));
  const union = new Set([...traitsA, ...traitsB]);
  
  return {
    sharedTraits: intersection,
    similarity: union.size > 0 ? (intersection.length / union.size) * 100 : 0,
    uniqueToA: [...traitsA].filter(trait => !traitsB.has(trait)),
    uniqueToB: [...traitsB].filter(trait => !traitsA.has(trait))
  };
};

/**
 * Tool: Get Plants By Zone
 * Returns all plants suitable for a specific climate zone
 */
export const getPlantsByZone = (zone) => {
  return plants.filter(plant => 
    plant.zone.toLowerCase() === zone.toLowerCase()
  );
};

/**
 * Tool: Predict Hybridization Success
 * Simulates a hybridization prediction between two plants
 */
export const predictHybridization = (plantAId, plantBId) => {
  const plantA = plants.find(p => p.id === plantAId);
  const plantB = plants.find(p => p.id === plantBId);
  
  if (!plantA || !plantB) {
    return null;
  }

  const similarity = calculateTraitSimilarity(plantA, plantB);
  
  // Simulate success rate based on trait similarity and zone compatibility
  const zoneBonus = plantA.zone === plantB.zone ? 15 : 0;
  const baseSuccess = similarity.similarity;
  const successRate = Math.min(95, Math.max(20, baseSuccess + zoneBonus));
  
  return {
    plantA: plantA.name,
    plantB: plantB.name,
    successRate: Math.round(successRate),
    confidence: (0.6 + (similarity.similarity / 200)).toFixed(2),
    sharedTraits: similarity.sharedTraits,
    compatibility: successRate >= 70 ? 'High' : successRate >= 50 ? 'Moderate' : 'Low',
    recommendation: successRate >= 70 
      ? 'These species show high compatibility for hybridization.'
      : successRate >= 50
      ? 'Moderate compatibility. Additional testing recommended.'
      : 'Low compatibility. Consider alternative combinations.'
  };
};

/**
 * Tool: Get Zone Statistics
 * Returns statistics about plants in a specific zone
 */
export const getZoneStatistics = (zone) => {
  const zonePlants = getPlantsByZone(zone);
  
  return {
    zone,
    plantCount: zonePlants.length,
    plants: zonePlants.map(p => ({
      name: p.name,
      scientificName: p.scientificName
    })),
    commonTraits: extractCommonTraits(zonePlants)
  };
};

/**
 * Helper: Extract Common Traits
 * Finds traits that appear in multiple plants
 */
const extractCommonTraits = (plantsList) => {
  const traitCounts = {};
  
  plantsList.forEach(plant => {
    (plant.traits || []).forEach(trait => {
      traitCounts[trait] = (traitCounts[trait] || 0) + 1;
    });
  });
  
  return Object.entries(traitCounts)
    .filter(([_, count]) => count >= 2)
    .map(([trait, count]) => ({ trait, count }))
    .sort((a, b) => b.count - a.count);
};

/**
 * Tool: Get Recommendations
 * Provides plant recommendations based on criteria
 */
export const getRecommendations = (criteria) => {
  const { zone, targetTrait, minSuccessRate = 50 } = criteria;
  
  let filteredPlants = [...plants];
  
  if (zone) {
    filteredPlants = filteredPlants.filter(p => 
      p.zone.toLowerCase() === zone.toLowerCase()
    );
  }
  
  if (targetTrait) {
    filteredPlants = filteredPlants.filter(p => 
      (p.traits || []).some(trait => 
        trait.toLowerCase().includes(targetTrait.toLowerCase())
      )
    );
  }
  
  return filteredPlants.slice(0, 5); // Return top 5 recommendations
};

/**
 * Chatbot Tools Registry
 * Maps tool names to their implementations
 */
export const chatbotTools = {
  searchPlants: {
    name: "searchPlants",
    description: "Search for plants by name, scientific name, or zone",
    parameters: {
      query: "string - search term"
    },
    execute: searchPlants
  },
  
  getPlantDetails: {
    name: "getPlantDetails",
    description: "Get detailed information about a specific plant",
    parameters: {
      plantId: "number - plant ID"
    },
    execute: getPlantDetails
  },
  
  calculateTraitSimilarity: {
    name: "calculateTraitSimilarity",
    description: "Calculate trait similarity between two plants",
    parameters: {
      plantA: "object - first plant",
      plantB: "object - second plant"
    },
    execute: calculateTraitSimilarity
  },
  
  getPlantsByZone: {
    name: "getPlantsByZone",
    description: "Get all plants for a specific climate zone",
    parameters: {
      zone: "string - climate zone (Northern, High Plateau, or Sahara)"
    },
    execute: getPlantsByZone
  },
  
  predictHybridization: {
    name: "predictHybridization",
    description: "Predict hybridization success between two plants",
    parameters: {
      plantAId: "number - first plant ID",
      plantBId: "number - second plant ID"
    },
    execute: predictHybridization
  },
  
  getZoneStatistics: {
    name: "getZoneStatistics",
    description: "Get statistics about a climate zone",
    parameters: {
      zone: "string - climate zone"
    },
    execute: getZoneStatistics
  },
  
  getRecommendations: {
    name: "getRecommendations",
    description: "Get plant recommendations based on criteria",
    parameters: {
      criteria: "object - { zone?, targetTrait?, minSuccessRate? }"
    },
    execute: getRecommendations
  }
};

export default chatbotTools;
