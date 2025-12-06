import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Loader, TrendingUp, Award } from 'lucide-react';
import { searchPlants, analyzePlant } from '../services/api-service';
import './Recommendations.css';

const Recommendations = () => {
  const [selectedPlant, setSelectedPlant] = useState('');
  const [allPlants, setAllPlants] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all plants on mount
  useEffect(() => {
    const fetchPlants = async () => {
      try {
        const plants = await searchPlants('');
        setAllPlants(plants);
      } catch (err) {
        console.error('Error fetching plants:', err);
        setError('Failed to load plants. Please ensure the backend is running.');
      }
    };
    fetchPlants();
  }, []);

  // Fetch recommendations when plant is selected
  useEffect(() => {
    const fetchRecommendations = async () => {
      if (selectedPlant) {
        setLoading(true);
        setError(null);
        try {
          const result = await analyzePlant(selectedPlant, 10);
          // Handle both possible response formats
          if (result.closest_plants && !result.nearest_neighbors) {
            result.nearest_neighbors = result.closest_plants;
          }
          setRecommendations(result);
        } catch (err) {
          console.error('Recommendations error:', err);
          setError(err.message || 'Failed to fetch recommendations.');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchRecommendations();
  }, [selectedPlant]);

  // Filter plants based on search query
  const filteredPlants = allPlants.filter(plant => 
    plant.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getCompatibilityBadge = (distance) => {
    if (distance < 2.0) return { label: 'Excellent', color: '#4caf50' };
    if (distance < 3.0) return { label: 'Very Good', color: '#8bc34a' };
    if (distance < 4.0) return { label: 'Good', color: '#cddc39' };
    if (distance < 5.0) return { label: 'Fair', color: '#ffc107' };
    return { label: 'Moderate', color: '#ff9800' };
  };

  return (
    <div className="recommendations-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="recommendations-header"
      >
        <h1>Plant Recommendations</h1>
        <p>Discover the top 10 most compatible plants for hybridization</p>
      </motion.div>

      {error && (
        <motion.div
          className="error-banner"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            background: 'var(--error)',
            color: 'white',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            textAlign: 'center'
          }}
        >
          {error}
        </motion.div>
      )}

      {/* Selection Section */}
      <motion.div
        className="selection-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="search-card">
          <div className="search-header">
            <Search size={24} />
            <h2>Select a Plant</h2>
          </div>
          
          <input
            type="text"
            placeholder="Search for a plant..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          
          <select 
            value={selectedPlant} 
            onChange={(e) => setSelectedPlant(e.target.value)}
            className="plant-select"
          >
            <option value="">Choose a plant to analyze...</option>
            {filteredPlants.map((plantName) => (
              <option key={plantName} value={plantName}>
                {plantName}
              </option>
            ))}
          </select>
          
          {searchQuery && (
            <div className="search-results-count">
              {filteredPlants.length} plant{filteredPlants.length !== 1 ? 's' : ''} found
            </div>
          )}
        </div>

        {selectedPlant && recommendations && !loading && (
          <motion.div
            className="plant-info-card"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <div className="plant-info-header">
              <span className="plant-icon">🌿</span>
              <h3>{recommendations.plant}</h3>
            </div>
            <div className="plant-info-details">
              <div className="info-item">
                <span className="info-label">Cluster:</span>
                <span className="info-value">{recommendations.cluster}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Hybridization Score:</span>
                <span className="info-value">{recommendations.hybridization_score.toFixed(3)}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Climate Zone:</span>
                <span className="info-value">{recommendations.climate_zone}</span>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Loading State */}
      {loading && (
        <div className="loading-container">
          <Loader className="spinner" size={40} />
          <p>Analyzing compatibility...</p>
        </div>
      )}

      {/* Recommendations List */}
      {recommendations && !loading && (recommendations.nearest_neighbors || recommendations.closest_plants) && (
        <motion.div
          className="recommendations-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="recommendations-header-section">
            <TrendingUp size={28} />
            <h2>Top 10 Compatible Plants</h2>
            <p>Ranked by genetic similarity and hybridization potential</p>
          </div>

          <div className="recommendations-grid">
            {(recommendations.nearest_neighbors || recommendations.closest_plants).map((neighbor, index) => {
              const compatibility = getCompatibilityBadge(neighbor.distance);
              return (
                <motion.div
                  key={neighbor.plant}
                  className="recommendation-card"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ scale: 1.02, boxShadow: '0 8px 16px rgba(0,0,0,0.1)' }}
                >
                  <div className="rank-badge">
                    {index === 0 && <Award size={20} fill="#FFD700" color="#FFD700" />}
                    {index === 1 && <Award size={20} fill="#C0C0C0" color="#C0C0C0" />}
                    {index === 2 && <Award size={20} fill="#CD7F32" color="#CD7F32" />}
                    <span className="rank-number">#{index + 1}</span>
                  </div>

                  <div className="card-content">
                    <div className="plant-header">
                      <span className="plant-icon-large">🌱</span>
                      <h3>{neighbor.plant}</h3>
                    </div>

                    <div className="plant-stats">
                      <div className="stat-row">
                        <span className="stat-label">Distance:</span>
                        <span className="stat-value">{neighbor.distance.toFixed(3)}</span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Cluster:</span>
                        <span className="stat-value">{neighbor.cluster}</span>
                      </div>
                      <div className="stat-row">
                        <span className="stat-label">Climate:</span>
                        <span className="stat-value">{neighbor.climate_zone}</span>
                      </div>
                    </div>

                    <div 
                      className="compatibility-badge"
                      style={{ backgroundColor: compatibility.color }}
                    >
                      {compatibility.label} Match
                    </div>

                    {neighbor.cluster === recommendations.cluster && (
                      <div className="same-cluster-badge">
                        ✓ Same Cluster
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Recommendations;
