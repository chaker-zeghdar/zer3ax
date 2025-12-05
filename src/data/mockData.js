// Mock data for the Plant Breeding Assistant

export const plants = [
  {
    id: 1,
    name: "Triticum aestivum",
    commonName: "Bread Wheat",
    icon: "🌾",
    perenniality: "Annual",
    woodiness: "Herbaceous",
    pollinationType: "Wind",
    genomeSize: 17000,
    environmentalFactor: {
      rainfall: "400-600mm",
      temperature: "15-25°C",
      droughtTolerance: "Moderate"
    },
    growthForm: "Erect",
    rootDepth: "1.5-2m",
    resistance: {
      drought: 6,
      salinity: 4,
      disease: 7
    },
    lifespan: "1 year",
    optimalZone: "Northern",
    soilPreference: "Loamy, well-drained",
    yieldPotential: 8,
    geneticDiversity: 7
  },
  {
    id: 2,
    name: "Hordeum vulgare",
    commonName: "Barley",
    icon: "🌾",
    perenniality: "Annual",
    woodiness: "Herbaceous",
    pollinationType: "Self",
    genomeSize: 5100,
    environmentalFactor: {
      rainfall: "300-500mm",
      temperature: "12-22°C",
      droughtTolerance: "High"
    },
    growthForm: "Erect",
    rootDepth: "1-1.5m",
    resistance: {
      drought: 8,
      salinity: 7,
      disease: 6
    },
    lifespan: "1 year",
    optimalZone: "High Plateau",
    soilPreference: "Well-drained, tolerates alkaline",
    yieldPotential: 7,
    geneticDiversity: 6
  },
  {
    id: 3,
    name: "Zea mays",
    commonName: "Corn/Maize",
    icon: "🌽",
    perenniality: "Annual",
    woodiness: "Herbaceous",
    pollinationType: "Wind",
    genomeSize: 2300,
    environmentalFactor: {
      rainfall: "500-800mm",
      temperature: "20-30°C",
      droughtTolerance: "Low"
    },
    growthForm: "Erect",
    rootDepth: "1-1.8m",
    resistance: {
      drought: 4,
      salinity: 3,
      disease: 5
    },
    lifespan: "1 year",
    optimalZone: "Northern",
    soilPreference: "Deep, fertile loam",
    yieldPotential: 9,
    geneticDiversity: 8
  },
  {
    id: 4,
    name: "Sorghum bicolor",
    commonName: "Sorghum",
    icon: "🌾",
    perenniality: "Annual",
    woodiness: "Herbaceous",
    pollinationType: "Self",
    genomeSize: 730,
    environmentalFactor: {
      rainfall: "400-600mm",
      temperature: "25-35°C",
      droughtTolerance: "Very High"
    },
    growthForm: "Erect",
    rootDepth: "2-2.5m",
    resistance: {
      drought: 9,
      salinity: 6,
      disease: 7
    },
    lifespan: "1 year",
    optimalZone: "Sahara",
    soilPreference: "Wide range, drought tolerant",
    yieldPotential: 7,
    geneticDiversity: 8
  },
  {
    id: 5,
    name: "Triticum durum",
    commonName: "Durum Wheat",
    icon: "🌾",
    perenniality: "Annual",
    woodiness: "Herbaceous",
    pollinationType: "Wind",
    genomeSize: 12000,
    environmentalFactor: {
      rainfall: "350-550mm",
      temperature: "15-25°C",
      droughtTolerance: "Moderate"
    },
    growthForm: "Erect",
    rootDepth: "1.5-2m",
    resistance: {
      drought: 7,
      salinity: 5,
      disease: 6
    },
    lifespan: "1 year",
    optimalZone: "High Plateau",
    soilPreference: "Clay-loam",
    yieldPotential: 7,
    geneticDiversity: 6
  },
  {
    id: 6,
    name: "Medicago sativa",
    commonName: "Alfalfa",
    icon: "🌿",
    perenniality: "Perennial",
    woodiness: "Herbaceous",
    pollinationType: "Insect",
    genomeSize: 900,
    environmentalFactor: {
      rainfall: "450-750mm",
      temperature: "15-28°C",
      droughtTolerance: "Moderate"
    },
    growthForm: "Spreading",
    rootDepth: "2-4m",
    resistance: {
      drought: 7,
      salinity: 6,
      disease: 7
    },
    lifespan: "3-5 years",
    optimalZone: "Northern",
    soilPreference: "Deep, well-drained",
    yieldPotential: 8,
    geneticDiversity: 7
  }
];

export const algeriaZones = [
  {
    id: 1,
    name: "Northern / Coastal Zone",
    color: "#4CAF50",
    climate: {
      rainfall: "400-800mm",
      temperature: "10-30°C",
      humidity: "High"
    },
    soilType: "Clay-loam, fertile",
    stressFactors: ["Occasional drought", "High humidity diseases"],
    bestPlants: [1, 3, 6], // Wheat, Corn, Alfalfa
    suitabilityScore: 8.5,
    coordinates: { lat: 36.7, lng: 3.2 }
  },
  {
    id: 2,
    name: "High Plateau Zone",
    color: "#8B4513",
    climate: {
      rainfall: "200-400mm",
      temperature: "5-35°C",
      humidity: "Moderate"
    },
    soilType: "Sandy-loam, alkaline",
    stressFactors: ["Cold winters", "Water scarcity", "Salinity"],
    bestPlants: [2, 5, 4], // Barley, Durum Wheat, Sorghum
    suitabilityScore: 7.2,
    coordinates: { lat: 34.8, lng: 1.5 }
  },
  {
    id: 3,
    name: "Southern / Sahara Zone",
    color: "#D2691E",
    climate: {
      rainfall: "50-200mm",
      temperature: "15-45°C",
      humidity: "Very Low"
    },
    soilType: "Sandy, poor organic matter",
    stressFactors: ["Extreme heat", "Severe drought", "Sand storms"],
    bestPlants: [4], // Sorghum
    suitabilityScore: 4.8,
    coordinates: { lat: 28.5, lng: 2.8 }
  }
];

export const recentPredictions = [
  {
    id: 1,
    plantA: "Triticum aestivum",
    plantB: "Hordeum vulgare",
    successRate: 78,
    confidence: 0.89,
    date: "2025-12-04",
    zone: "Northern"
  },
  {
    id: 2,
    plantA: "Zea mays",
    plantB: "Sorghum bicolor",
    successRate: 45,
    confidence: 0.72,
    date: "2025-12-04",
    zone: "High Plateau"
  },
  {
    id: 3,
    plantA: "Triticum durum",
    plantB: "Triticum aestivum",
    successRate: 92,
    confidence: 0.95,
    date: "2025-12-03",
    zone: "Northern"
  },
  {
    id: 4,
    plantA: "Medicago sativa",
    plantB: "Triticum aestivum",
    successRate: 35,
    confidence: 0.65,
    date: "2025-12-03",
    zone: "High Plateau"
  },
  {
    id: 5,
    plantA: "Hordeum vulgare",
    plantB: "Sorghum bicolor",
    successRate: 68,
    confidence: 0.81,
    date: "2025-12-02",
    zone: "Sahara"
  }
];

export const kpiData = {
  totalPlants: plants.length,
  totalTraits: 15,
  avgSuccessRate: 72,
  predictionsToday: 12,
  topZoneToday: "Northern"
};

export const trendingSpecies = [
  { name: "Triticum aestivum", uses: 45 },
  { name: "Hordeum vulgare", uses: 38 },
  { name: "Sorghum bicolor", uses: 32 },
  { name: "Zea mays", uses: 28 },
  { name: "Triticum durum", uses: 25 }
];

// Function to simulate AI prediction
export const predictHybrid = (plantAId, plantBId) => {
  const plantA = plants.find(p => p.id === plantAId);
  const plantB = plants.find(p => p.id === plantBId);
  
  if (!plantA || !plantB) return null;

  // Calculate success based on trait compatibility
  let successScore = 50; // Base score
  
  // Same pollination type increases success
  if (plantA.pollinationType === plantB.pollinationType) successScore += 15;
  
  // Similar genome size (within 5000) increases success
  const genomeDiff = Math.abs(plantA.genomeSize - plantB.genomeSize);
  if (genomeDiff < 5000) successScore += 10;
  else if (genomeDiff > 10000) successScore -= 15;
  
  // Same perenniality increases success
  if (plantA.perenniality === plantB.perenniality) successScore += 10;
  
  // Similar drought tolerance
  const droughtDiff = Math.abs(plantA.resistance.drought - plantB.resistance.drought);
  if (droughtDiff <= 2) successScore += 8;
  else successScore -= 5;
  
  // Same zone compatibility
  if (plantA.optimalZone === plantB.optimalZone) successScore += 7;
  
  // Clamp between 0-100
  successScore = Math.max(0, Math.min(100, successScore));
  
  const confidence = successScore > 70 ? 0.9 : successScore > 50 ? 0.75 : 0.6;
  
  return {
    successRate: Math.round(successScore),
    confidence: confidence,
    sharedTraits: [
      plantA.pollinationType === plantB.pollinationType && "Same pollination type",
      Math.abs(plantA.genomeSize - plantB.genomeSize) < 5000 && "Compatible genome size",
      plantA.perenniality === plantB.perenniality && "Same perenniality",
      droughtDiff <= 2 && "Similar drought tolerance"
    ].filter(Boolean),
    featureImpact: [
      { trait: "Genome compatibility", impact: genomeDiff < 5000 ? 15 : -15 },
      { trait: "Pollination match", impact: plantA.pollinationType === plantB.pollinationType ? 15 : -5 },
      { trait: "Drought tolerance", impact: droughtDiff <= 2 ? 8 : -5 },
      { trait: "Perenniality match", impact: plantA.perenniality === plantB.perenniality ? 10 : -3 },
      { trait: "Zone compatibility", impact: plantA.optimalZone === plantB.optimalZone ? 7 : 0 }
    ]
  };
};

export const rankedPlants = plants.map(plant => ({
  ...plant,
  hybridPotentialScore: (plant.resistance.drought + plant.yieldPotential + plant.geneticDiversity) / 3,
  environmentalAdaptability: (plant.resistance.drought + plant.resistance.salinity + plant.resistance.disease) / 3,
  overallRating: Math.round(((plant.resistance.drought + plant.yieldPotential + plant.geneticDiversity) / 3) / 2)
})).sort((a, b) => b.hybridPotentialScore - a.hybridPotentialScore);
