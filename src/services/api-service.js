/**
 * AgroX Plant Hybridization API Service
 * Connects frontend to backend API running on localhost:5001
 */

const BASE_URL = 'http://localhost:5001';

/**
 * Generic fetch wrapper with error handling
 */
const apiFetch = async (endpoint, options = {}) => {
try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
        'Content-Type': 'application/json',
        ...options.headers,
    },
    ...options,
    });

    if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
} catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
}
};

// ============================================================================
// HEALTH & STATUS
// ============================================================================

/**
 * Check API health and get basic statistics
 * @returns {Promise<{status: string, message: string, total_plants: number, total_clusters: number}>}
 */
export const checkHealth = async () => {
  return apiFetch('/api/health');
};

/**
 * Get global statistics about the dataset
 * @returns {Promise<{total_plants: number, total_clusters: number, cluster_sizes: object, climate_zones: object, avg_hybridization_score: number}>}
 */
export const getGlobalStats = async () => {
  return apiFetch('/api/stats');
};

// ============================================================================
// PLANT SEARCH & DISCOVERY
// ============================================================================

/**
 * Get all plant genus names
 * @returns {Promise<string[]>} Array of plant names
 */
export const getAllPlants = async () => {
  const response = await apiFetch('/api/plants');
  return response.plants || [];
};

/**
 * Search for plants by partial name match
 * @param {string} query - Search query (case-insensitive)
 * @returns {Promise<string[]>} Array of matching plant names
 */
export const searchPlants = async (query) => {
  if (!query || query.trim() === '') {
    return getAllPlants();
  }
  const response = await apiFetch(`/api/plants/search?q=${encodeURIComponent(query)}`);
  return response.plants || [];
};

// ============================================================================
// PLANT ANALYSIS
// ============================================================================

/**
 * Analyze a single plant - get detailed information
 * @param {string} plantName - Name of the plant to analyze
 * @param {number} topK - Number of nearest neighbors to return (default: 3)
 * @returns {Promise<{plant: string, cluster: number, hybridization_score: number, climate_zone: string, features: object, nearest_neighbors: array}>}
 */
export const analyzePlant = async (plantName, topK = 3) => {
  return apiFetch(`/api/analyze/${encodeURIComponent(plantName)}?top_k=${topK}`);
};

/**
 * Analyze multiple plants in batch
 * @param {string[]} plantNames - Array of plant names to analyze
 * @returns {Promise<array>} Array of plant analysis results
 */
export const batchAnalyzePlants = async (plantNames) => {
  return apiFetch('/api/batch/analyze', {
    method: 'POST',
    body: JSON.stringify({ plants: plantNames }),
  });
};

// ============================================================================
// PLANT COMPARISON
// ============================================================================

/**
 * Compare two plants and get compatibility information
 * @param {string} plantA - First plant name
 * @param {string} plantB - Second plant name
 * @returns {Promise<{plant_a: object, plant_b: object, distance: number, compatibility: string, same_cluster: boolean, recommendation: string}>}
 */
export const comparePlants = async (plantA, plantB) => {
  return apiFetch('/api/compare', {
    method: 'POST',
    body: JSON.stringify({
    plant_a: plantA,
    plant_b: plantB,
    }),
  });
};

// ============================================================================
// CLUSTER ANALYSIS
// ============================================================================

/**
 * Get all plants in a specific cluster with statistics
 * @param {number} clusterId - Cluster ID (0-17)
 * @returns {Promise<{cluster_id: number, plant_count: number, plants: array, avg_hybridization_score: number, climate_zones: object}>}
 */
export const getClusterInfo = async (clusterId) => {
  return apiFetch(`/api/cluster/${clusterId}`);
};

/**
 * Get all clusters information
 * @returns {Promise<array>} Array of cluster summaries
 */
export const getAllClusters = async () => {
  const stats = await getGlobalStats();
  const clusterIds = Object.keys(stats.cluster_sizes).map(Number);
  
  // Fetch all clusters in parallel
  const clusterPromises = clusterIds.map(id => getClusterInfo(id));
  return Promise.all(clusterPromises);
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get plant details with recommendations
 * @param {string} plantName - Plant name
 * @returns {Promise<object>} Plant details with nearest neighbors
 */
export const getPlantWithRecommendations = async (plantName) => {
  try {
    const analysis = await analyzePlant(plantName, 5);
    return {
      name: analysis.plant,
      cluster: analysis.cluster,
      hybridizationScore: analysis.hybridization_score,
      climateZone: analysis.climate_zone,
      features: analysis.features,
      recommendations: analysis.nearest_neighbors,
    };
  } catch (error) {
    console.error('Error fetching plant recommendations:', error);
    throw error;
  }
};

/**
 * Get compatibility rating based on distance
 * @param {number} distance - Euclidean distance between plants
 * @param {boolean} sameCluster - Whether plants are in the same cluster
 * @returns {{level: string, percentage: number, color: string}}
 */
export const getCompatibilityRating = (distance, sameCluster) => {
  let level, percentage, color;
  
  if (sameCluster) {
    if (distance < 2.0) {
      level = 'Very High';
      percentage = 95;
      color = '#4caf50';
    } else if (distance < 3.0) {
      level = 'High';
      percentage = 85;
      color = '#8bc34a';
    } else if (distance < 4.0) {
      level = 'Medium';
      percentage = 65;
      color = '#ffc107';
    } else {
      level = 'Low';
      percentage = 35;
      color = '#ff9800';
    }
  } else {
    if (distance < 3.0) {
      level = 'High';
      percentage = 75;
      color = '#8bc34a';
    } else if (distance < 5.0) {
      level = 'Medium';
      percentage = 50;
      color = '#ffc107';
    } else {
      level = 'Low';
      percentage = 25;
      color = '#f44336';
    }
  }
  
  return { level, percentage, color };
};

/**
 * Format plant name for display
 * @param {string} name - Plant genus name
 * @returns {string} Formatted name
 */
export const formatPlantName = (name) => {
  return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
};

/**
 * Get plant icon based on climate zone or name
 * @param {string} climateZone - Climate zone
 * @param {string} name - Plant name
 * @returns {string} Emoji icon
 */
export const getPlantIcon = (climateZone, name = '') => {
  const nameLower = name.toLowerCase();
  
  // Specific plant icons
  if (nameLower.includes('rosa')) return '🌹';
  if (nameLower.includes('quercus')) return '🌳';
  if (nameLower.includes('pinus')) return '🌲';
  if (nameLower.includes('abies')) return '🌲';
  if (nameLower.includes('citrus')) return '🍊';
  if (nameLower.includes('malus')) return '🍎';
  if (nameLower.includes('prunus')) return '🌸';
  if (nameLower.includes('vitis')) return '🍇';
  
  // Climate-based icons
  switch (climateZone) {
    case 'Tropical':
      return '🌴';
    case 'Temperate':
      return '🌳';
    case 'Arid':
      return '🌵';
    case 'Cold':
      return '🌲';
    default:
      return '🌿';
  }
};

export default {
  // Health & Status
  checkHealth,
  getGlobalStats,
  
  // Plant Search
  getAllPlants,
  searchPlants,
  
  // Plant Analysis
  analyzePlant,
  batchAnalyzePlants,
  
  // Plant Comparison
  comparePlants,
  
  // Cluster Analysis
  getClusterInfo,
  getAllClusters,
  
  // Utility
  getPlantWithRecommendations,
  getCompatibilityRating,
  formatPlantName,
  getPlantIcon,
};
