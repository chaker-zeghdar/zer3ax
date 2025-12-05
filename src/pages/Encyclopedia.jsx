import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, X } from 'lucide-react';
import { searchPlants, analyzePlant, getPlantIcon } from '../services/api-service';
import './Encyclopedia.css';

const Encyclopedia = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [selectedPlantDetails, setSelectedPlantDetails] = useState(null);
  const [filterZone, setFilterZone] = useState('all');
  const [allPlants, setAllPlants] = useState([]);
  const [displayedPlants, setDisplayedPlants] = useState([]);
  const [plantDetailsCache, setPlantDetailsCache] = useState({});
  const [loading, setLoading] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all plants on mount
  useEffect(() => {
    const fetchPlants = async () => {
      try {
        setLoading(true);
        const plants = await searchPlants('');
        
        // Fetch details for first batch of plants to get climate zones
        const detailsPromises = plants.slice(0, 20).map(async (plantName) => {
          try {
            const details = await analyzePlant(plantName, 1);
            return { name: plantName, details };
          } catch (err) {
            console.error(`Error fetching ${plantName}:`, err);
            return { name: plantName, details: null };
          }
        });
        
        const detailsResults = await Promise.all(detailsPromises);
        const cache = {};
        detailsResults.forEach(({ name, details }) => {
          if (details) cache[name] = details;
        });
        
        setPlantDetailsCache(cache);
        setAllPlants(plants);
        setDisplayedPlants(plants);
      } catch (err) {
        console.error('Error fetching plants:', err);
        setError('Failed to load plants. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchPlants();
  }, []);

  // Filter plants based on search and filters
  useEffect(() => {
    let filtered = allPlants;
    
    if (searchTerm) {
      const lowerSearch = searchTerm.toLowerCase();
      filtered = filtered.filter(plant => 
        plant.toLowerCase().includes(lowerSearch)
      );
    }
    
    if (filterZone !== 'all') {
      filtered = filtered.filter(plantName => {
        const details = plantDetailsCache[plantName];
        return details && details.climate_zone === filterZone;
      });
    }
    
    setDisplayedPlants(filtered);
  }, [searchTerm, filterZone, allPlants, plantDetailsCache]);

  // Fetch selected plant details
  const handlePlantClick = async (plantName) => {
    setSelectedPlant(plantName);
    setLoadingDetails(true);
    
    try {
      // Check cache first
      if (plantDetailsCache[plantName]) {
        setSelectedPlantDetails(plantDetailsCache[plantName]);
      } else {
        const details = await analyzePlant(plantName, 5);
        setSelectedPlantDetails(details);
        setPlantDetailsCache(prev => ({ ...prev, [plantName]: details }));
      }
    } catch (err) {
      console.error('Error fetching plant details:', err);
      setError('Failed to load plant details.');
    } finally {
      setLoadingDetails(false);
    }
  };

  return (
    <div className="encyclopedia-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="encyclopedia-header"
      >
        <h1>📚 Plant Encyclopedia</h1>
        <p>Comprehensive database of plant traits and characteristics</p>
      </motion.div>

      {error && (
        <div style={{
          background: 'var(--error)',
          color: 'white',
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '1rem',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      {/* Search and Filters */}
      <div className="search-filter-section">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search by name or species..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <X 
              size={20} 
              className="clear-btn" 
              onClick={() => setSearchTerm('')}
            />
          )}
        </div>

        <div className="filters">
          <div className="filter-item">
            <Filter size={18} />
            <label>Zone:</label>
            <select value={filterZone} onChange={(e) => setFilterZone(e.target.value)}>
              <option value="all">All</option>
              <option value="Tropical">Tropical</option>
              <option value="Temperate">Temperate</option>
              <option value="Arid">Arid</option>
              <option value="Cold">Cold</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-count">
        {loading ? 'Loading plants...' : `Showing ${displayedPlants.length} of ${allPlants.length} plants`}
      </div>

      {/* Plants Grid */}
      <div className="plants-grid">
        {displayedPlants.slice(0, 50).map((plantName, index) => {
          const details = plantDetailsCache[plantName];
          return (
            <motion.div
              key={plantName}
              className="plant-encyclopedia-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.02 }}
              whileHover={{ y: -5 }}
              onClick={() => handlePlantClick(plantName)}
            >
              <div className="plant-card-icon">{getPlantIcon(details?.climate_zone, plantName)}</div>
              <h3 className="plant-card-title">{plantName}</h3>
              
              {details && (
                <>
                  <div className="plant-card-traits">
                    <div className="trait-badge">
                      <span className="trait-badge-label">Zone</span>
                      <span className="trait-badge-value">{details.climate_zone}</span>
                    </div>
                    <div className="trait-badge">
                      <span className="trait-badge-label">Cluster</span>
                      <span className="trait-badge-value">{details.cluster}</span>
                    </div>
                  </div>

                  <div className="plant-card-stats">
                    <div className="stat-item">
                      <span className="stat-icon">🧬</span>
                      <span className="stat-value">{details.hybridization_score.toFixed(1)}</span>
                    </div>
                  </div>
                </>
              )}

              <button className="view-details-btn">View Details</button>
            </motion.div>
          );
        })}
      </div>

      {displayedPlants.length === 0 && !loading && (
        <div className="no-results">
          <p>No plants found matching your criteria</p>
          <button onClick={() => {
            setSearchTerm('');
            setFilterZone('all');
          }}>
            Clear Filters
          </button>
        </div>
      )}

      {/* Plant Details Modal */}
      {selectedPlant && (
        <div className="modal-overlay" onClick={() => {
          setSelectedPlant(null);
          setSelectedPlantDetails(null);
        }}>
          <motion.div
            className="modal-content"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={(e) => e.stopPropagation()}
          >
            <button className="modal-close" onClick={() => {
              setSelectedPlant(null);
              setSelectedPlantDetails(null);
            }}>
              <X size={24} />
            </button>

            {loadingDetails ? (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>Loading plant details...</p>
              </div>
            ) : selectedPlantDetails ? (
              <>
                <div className="modal-header">
                  <span className="modal-icon">{getPlantIcon(selectedPlantDetails.climate_zone, selectedPlant)}</span>
                  <div>
                    <h2>{selectedPlant}</h2>
                    <p className="modal-scientific">Cluster {selectedPlantDetails.cluster}</p>
                  </div>
                </div>

                <div className="modal-body">
                  <div className="detail-section">
                    <h3>Basic Information</h3>
                    <div className="detail-grid">
                      <DetailRow label="Hybridization Score" value={selectedPlantDetails.hybridization_score.toFixed(2)} />
                      <DetailRow label="Climate Zone" value={selectedPlantDetails.climate_zone} />
                      <DetailRow label="Cluster" value={selectedPlantDetails.cluster} />
                    </div>
                  </div>

                  {selectedPlantDetails.nearest_neighbors && selectedPlantDetails.nearest_neighbors.length > 0 && (
                    <div className="detail-section">
                      <h3>Similar Plants (Nearest Neighbors)</h3>
                      <div className="neighbors-list">
                        {selectedPlantDetails.nearest_neighbors.map((neighbor, idx) => (
                          <div key={idx} className="neighbor-item">
                            <span>{getPlantIcon(selectedPlantDetails.climate_zone, neighbor.plant)}</span>
                            <span>{neighbor.plant}</span>
                            <span className="neighbor-distance">Distance: {neighbor.distance.toFixed(2)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="detail-section">
                    <h3>Feature Values</h3>
                    <div className="resistance-bars">
                      {Object.entries(selectedPlantDetails.features || {}).slice(0, 8).map(([key, value]) => (
                        <ResistanceBar key={key} label={key.replace(/_/g, ' ')} value={value * 10} />
                      ))}
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>No details available</p>
              </div>
            )}
          </motion.div>
        </div>
      )}
    </div>
  );
};

const DetailRow = ({ label, value }) => (
  <div className="detail-row">
    <span className="detail-label">{label}:</span>
    <span className="detail-value">{value}</span>
  </div>
);

const ResistanceBar = ({ label, value }) => (
  <div className="resistance-bar-container">
    <div className="resistance-label-row">
      <span className="resistance-label">{label}</span>
      <span className="resistance-value">{value}/10</span>
    </div>
    <div className="resistance-bar">
      <div 
        className="resistance-fill"
        style={{ width: `${(value / 10) * 100}%` }}
      />
    </div>
  </div>
);

export default Encyclopedia;
