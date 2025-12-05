import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Loader, ChevronDown } from 'lucide-react';
import { plants, predictHybrid } from '../data/mockData';
import './Predict.css';

const Predict = () => {
  const [plantA, setPlantA] = useState(null);
  const [plantB, setPlantB] = useState(null);
  const [searchA, setSearchA] = useState('');
  const [searchB, setSearchB] = useState('');
  const [showDropdownA, setShowDropdownA] = useState(false);
  const [showDropdownB, setShowDropdownB] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const filteredPlantsA = plants.filter(p => 
    p.name.toLowerCase().includes(searchA.toLowerCase()) ||
    p.commonName.toLowerCase().includes(searchA.toLowerCase())
  );

  const filteredPlantsB = plants.filter(p => 
    p.name.toLowerCase().includes(searchB.toLowerCase()) ||
    p.commonName.toLowerCase().includes(searchB.toLowerCase())
  );

  const handlePredict = async () => {
    if (!plantA || !plantB) return;
    
    setLoading(true);
    // Simulate AI processing
    setTimeout(() => {
      const result = predictHybrid(plantA.id, plantB.id);
      setPrediction(result);
      setLoading(false);
    }, 1500);
  };

  const getConfidenceLevel = (confidence) => {
    if (confidence >= 0.85) return { label: 'High', color: 'var(--success)' };
    if (confidence >= 0.70) return { label: 'Medium', color: 'var(--warning)' };
    return { label: 'Low', color: 'var(--error)' };
  };

  const getSuccessColor = (rate) => {
    if (rate >= 70) return 'var(--success)';
    if (rate >= 50) return 'var(--warning)';
    return 'var(--error)';
  };

  return (
    <div className="predict-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="predict-header"
      >
        <h1>🧬 Hybrid Prediction</h1>
        <p>Predict the likelihood of successful hybridization between two plant species</p>
      </motion.div>

      <div className="predict-container">
        {/* Selection Form */}
        <motion.div
          className="selection-card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h2>Select Plants for Hybrid Prediction</h2>
          
          {/* Plant A Selection */}
          <div className="plant-selector">
            <label>Plant A</label>
            <div className="dropdown-container">
              <div className="search-input-wrapper" onClick={() => setShowDropdownA(true)}>
                <Search size={18} className="search-icon" />
                <input
                  type="text"
                  placeholder="Search for a plant..."
                  value={plantA ? `${plantA.icon} ${plantA.name} (${plantA.commonName})` : searchA}
                  onChange={(e) => {
                    setSearchA(e.target.value);
                    setPlantA(null);
                    setShowDropdownA(true);
                  }}
                  onFocus={() => setShowDropdownA(true)}
                />
                <ChevronDown size={18} className="dropdown-icon" />
              </div>
              
              {showDropdownA && (
                <div className="dropdown-menu">
                  {filteredPlantsA.map((plant) => (
                    <div
                      key={plant.id}
                      className="dropdown-item"
                      onClick={() => {
                        setPlantA(plant);
                        setSearchA('');
                        setShowDropdownA(false);
                      }}
                    >
                      <span className="plant-icon">{plant.icon}</span>
                      <div className="plant-info">
                        <span className="plant-name">{plant.name}</span>
                        <span className="plant-common">({plant.commonName})</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Plant B Selection */}
          <div className="plant-selector">
            <label>Plant B</label>
            <div className="dropdown-container">
              <div className="search-input-wrapper" onClick={() => setShowDropdownB(true)}>
                <Search size={18} className="search-icon" />
                <input
                  type="text"
                  placeholder="Search for a plant..."
                  value={plantB ? `${plantB.icon} ${plantB.name} (${plantB.commonName})` : searchB}
                  onChange={(e) => {
                    setSearchB(e.target.value);
                    setPlantB(null);
                    setShowDropdownB(true);
                  }}
                  onFocus={() => setShowDropdownB(true)}
                />
                <ChevronDown size={18} className="dropdown-icon" />
              </div>
              
              {showDropdownB && (
                <div className="dropdown-menu">
                  {filteredPlantsB.map((plant) => (
                    <div
                      key={plant.id}
                      className="dropdown-item"
                      onClick={() => {
                        setPlantB(plant);
                        setSearchB('');
                        setShowDropdownB(false);
                      }}
                    >
                      <span className="plant-icon">{plant.icon}</span>
                      <div className="plant-info">
                        <span className="plant-name">{plant.name}</span>
                        <span className="plant-common">({plant.commonName})</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <button 
            className="predict-btn"
            onClick={handlePredict}
            disabled={!plantA || !plantB || loading}
          >
            {loading ? (
              <>
                <Loader className="spinner" size={20} />
                Processing...
              </>
            ) : (
              'Predict Hybrid Success'
            )}
          </button>
        </motion.div>

        {/* Results Panel */}
        {prediction && (
          <motion.div
            className="results-panel"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2>AI Prediction Results</h2>
            
            {/* Success Probability */}
            <div className="result-section">
              <h3>Probability of Hybrid Success</h3>
              <div className="probability-display">
                <div 
                  className="probability-gauge"
                  style={{ 
                    background: `conic-gradient(${getSuccessColor(prediction.successRate)} ${prediction.successRate}%, var(--border-light) ${prediction.successRate}%)`
                  }}
                >
                  <div className="gauge-inner">
                    <span className="probability-value">{prediction.successRate}%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Confidence Level */}
            <div className="result-section">
              <h3>Confidence Level</h3>
              <div className="confidence-badge" style={{ backgroundColor: getConfidenceLevel(prediction.confidence).color }}>
                {getConfidenceLevel(prediction.confidence).label} ({prediction.confidence.toFixed(2)})
              </div>
            </div>

            {/* Shared Traits */}
            {prediction.sharedTraits.length > 0 && (
              <div className="result-section">
                <h3>Key Traits Shared</h3>
                <div className="traits-chips">
                  {prediction.sharedTraits.map((trait, index) => (
                    <span key={index} className="trait-chip">
                      {trait}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Compatibility Notes */}
            <div className="result-section">
              <h3>Compatibility Notes</h3>
              <div className="compatibility-note">
                {prediction.successRate >= 70 ? (
                  <p>✅ These species show high compatibility. Shared traits and similar genetic profiles increase the likelihood of successful hybridization.</p>
                ) : prediction.successRate >= 50 ? (
                  <p>⚠️ Moderate compatibility detected. Some traits align well, but differences in key characteristics may pose challenges.</p>
                ) : (
                  <p>❌ Low compatibility. Significant differences in genetic and environmental factors reduce hybridization success.</p>
                )}
              </div>
            </div>

            {/* Feature Impact (XAI) */}
            <div className="result-section">
              <h3>Feature Impact Analysis (XAI)</h3>
              <div className="feature-impact-chart">
                {prediction.featureImpact.map((feature, index) => (
                  <div key={index} className="impact-bar-container">
                    <span className="impact-label">{feature.trait}</span>
                    <div className="impact-bar">
                      <div
                        className="impact-fill"
                        style={{
                          width: `${Math.abs(feature.impact) * 5}%`,
                          backgroundColor: feature.impact > 0 ? 'var(--success)' : 'var(--error)',
                        }}
                      />
                      <span className="impact-value">
                        {feature.impact > 0 ? '+' : ''}{feature.impact}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Explanation Text */}
            <div className="result-section">
              <h3>AI Explanation</h3>
              <div className="explanation-text">
                <p>
                  The prediction model analyzed {prediction.featureImpact.length} key traits. 
                  {prediction.featureImpact.filter(f => f.impact > 0).length > 0 && 
                    ` Positive factors include ${prediction.featureImpact.filter(f => f.impact > 0).map(f => f.trait.toLowerCase()).join(', ')}.`
                  }
                  {prediction.featureImpact.filter(f => f.impact < 0).length > 0 && 
                    ` Negative factors include ${prediction.featureImpact.filter(f => f.impact < 0).map(f => f.trait.toLowerCase()).join(', ')}.`
                  }
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Predict;
