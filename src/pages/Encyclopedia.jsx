import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, X } from 'lucide-react';
import { plants } from '../data/mockData';
import './Encyclopedia.css';

const Encyclopedia = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [filterZone, setFilterZone] = useState('all');
  const [filterPollination, setFilterPollination] = useState('all');

  const filteredPlants = plants.filter(plant => {
    const matchesSearch = plant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         plant.commonName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesZone = filterZone === 'all' || plant.optimalZone === filterZone;
    const matchesPollination = filterPollination === 'all' || plant.pollinationType === filterPollination;
    
    return matchesSearch && matchesZone && matchesPollination;
  });

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
              <option value="Northern">Northern</option>
              <option value="High Plateau">High Plateau</option>
              <option value="Sahara">Sahara</option>
            </select>
          </div>

          <div className="filter-item">
            <Filter size={18} />
            <label>Pollination:</label>
            <select value={filterPollination} onChange={(e) => setFilterPollination(e.target.value)}>
              <option value="all">All</option>
              <option value="Wind">Wind</option>
              <option value="Self">Self</option>
              <option value="Insect">Insect</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-count">
        Showing {filteredPlants.length} of {plants.length} plants
      </div>

      {/* Plants Grid */}
      <div className="plants-grid">
        {filteredPlants.map((plant, index) => (
          <motion.div
            key={plant.id}
            className="plant-encyclopedia-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ y: -5 }}
            onClick={() => setSelectedPlant(plant)}
          >
            <div className="plant-card-icon">{plant.icon}</div>
            <h3 className="plant-card-title">{plant.commonName}</h3>
            <p className="plant-card-scientific">{plant.name}</p>
            
            <div className="plant-card-traits">
              <div className="trait-badge">
                <span className="trait-badge-label">Zone</span>
                <span className="trait-badge-value">{plant.optimalZone}</span>
              </div>
              <div className="trait-badge">
                <span className="trait-badge-label">Pollination</span>
                <span className="trait-badge-value">{plant.pollinationType}</span>
              </div>
            </div>

            <div className="plant-card-stats">
              <div className="stat-item">
                <span className="stat-icon">💧</span>
                <span className="stat-value">{plant.resistance.drought}/10</span>
              </div>
              <div className="stat-item">
                <span className="stat-icon">🌾</span>
                <span className="stat-value">{plant.yieldPotential}/10</span>
              </div>
              <div className="stat-item">
                <span className="stat-icon">🧬</span>
                <span className="stat-value">{plant.geneticDiversity}/10</span>
              </div>
            </div>

            <button className="view-details-btn">View Details</button>
          </motion.div>
        ))}
      </div>

      {filteredPlants.length === 0 && (
        <div className="no-results">
          <p>No plants found matching your criteria</p>
          <button onClick={() => {
            setSearchTerm('');
            setFilterZone('all');
            setFilterPollination('all');
          }}>
            Clear Filters
          </button>
        </div>
      )}

      {/* Plant Details Modal */}
      {selectedPlant && (
        <div className="modal-overlay" onClick={() => setSelectedPlant(null)}>
          <motion.div
            className="modal-content"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={(e) => e.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelectedPlant(null)}>
              <X size={24} />
            </button>

            <div className="modal-header">
              <span className="modal-icon">{selectedPlant.icon}</span>
              <div>
                <h2>{selectedPlant.commonName}</h2>
                <p className="modal-scientific">{selectedPlant.name}</p>
              </div>
            </div>

            <div className="modal-body">
              <div className="detail-section">
                <h3>Basic Information</h3>
                <div className="detail-grid">
                  <DetailRow label="Perenniality" value={selectedPlant.perenniality} />
                  <DetailRow label="Woodiness" value={selectedPlant.woodiness} />
                  <DetailRow label="Pollination Type" value={selectedPlant.pollinationType} />
                  <DetailRow label="Genome Size" value={`${selectedPlant.genomeSize} Mb`} />
                  <DetailRow label="Growth Form" value={selectedPlant.growthForm} />
                  <DetailRow label="Root Depth" value={selectedPlant.rootDepth} />
                  <DetailRow label="Lifespan" value={selectedPlant.lifespan} />
                  <DetailRow label="Optimal Zone" value={selectedPlant.optimalZone} />
                </div>
              </div>

              <div className="detail-section">
                <h3>Environmental Requirements</h3>
                <div className="detail-grid">
                  <DetailRow label="Rainfall" value={selectedPlant.environmentalFactor.rainfall} />
                  <DetailRow label="Temperature" value={selectedPlant.environmentalFactor.temperature} />
                  <DetailRow label="Drought Tolerance" value={selectedPlant.environmentalFactor.droughtTolerance} />
                  <DetailRow label="Soil Preference" value={selectedPlant.soilPreference} />
                </div>
              </div>

              <div className="detail-section">
                <h3>Resistance & Performance</h3>
                <div className="resistance-bars">
                  <ResistanceBar label="Drought Resistance" value={selectedPlant.resistance.drought} />
                  <ResistanceBar label="Salinity Resistance" value={selectedPlant.resistance.salinity} />
                  <ResistanceBar label="Disease Resistance" value={selectedPlant.resistance.disease} />
                  <ResistanceBar label="Yield Potential" value={selectedPlant.yieldPotential} />
                  <ResistanceBar label="Genetic Diversity" value={selectedPlant.geneticDiversity} />
                </div>
              </div>
            </div>
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
