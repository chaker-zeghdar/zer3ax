import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Loader } from 'lucide-react';
import { searchPlants, comparePlants, getCompatibilityRating } from '../services/api-service';
import './Predict.css';

const Predict = () => {
  const [plantA, setPlantA] = useState('');
  const [plantB, setPlantB] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [allPlants, setAllPlants] = useState([]);
  const [error, setError] = useState(null);

  // Fetch all plants on component mount
  useEffect(() => {
    const fetchPlants = async () => {
      try {
        const plants = await searchPlants('');
        setAllPlants(Array.isArray(plants) ? plants : []);
      } catch (err) {
        console.error('Error fetching plants:', err);
        setError('Failed to load plants. Please ensure the backend is running.');
        setAllPlants([]);
      }
    };
    fetchPlants();
  }, []);

  const handlePredict = async () => {
    if (!plantA || !plantB) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Call backend API
      const result = await comparePlants(plantA, plantB);
      
      // Transform API response to match UI expectations
      const compatibility = getCompatibilityRating(result.distance, result.same_cluster);
      
      const transformedPrediction = {
        successRate: compatibility.percentage,
        confidence: result.distance < 2.0 ? 0.95 : result.distance < 4.0 ? 0.85 : 0.70,
        sharedTraits: [
          result.same_cluster && 'Same Cluster',
          result.plant_a.climate_zone === result.plant_b.climate_zone && 'Same Climate Zone',
          Math.abs(result.plant_a.hybridization_score - result.plant_b.hybridization_score) < 0.5 && 'Similar Hybridization Score'
        ].filter(Boolean),
        featureImpact: [
          {
            trait: 'Cluster Similarity',
            impact: result.same_cluster ? 15 : -10
          },
          {
            trait: 'Euclidean Distance',
            impact: result.distance < 3.0 ? 20 : -15
          },
          {
            trait: 'Climate Zone Match',
            impact: result.plant_a.climate_zone === result.plant_b.climate_zone ? 12 : -8
          },
          {
            trait: 'Hybridization Score Difference',
            impact: Math.abs(result.plant_a.hybridization_score - result.plant_b.hybridization_score) < 0.5 ? 10 : -5
          }
        ],
        recommendation: result.recommendation,
        distance: result.distance,
        plantADetails: result.plant_a,
        plantBDetails: result.plant_b
      };
      
      setPrediction(transformedPrediction);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.message || 'Failed to predict hybridization. Please try again.');
    } finally {
      setLoading(false);
    }
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
        <h1>Hybrid Prediction</h1>
        <p>Predict the likelihood of successful hybridization between two plant species</p>
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
            <select 
              value={plantA || ''} 
              onChange={(e) => setPlantA(e.target.value)}
              className="plant-select"
            >
              <option value="">Select a plant...</option>
              {Array.isArray(allPlants) && allPlants.map((plantName) => (
                <option key={plantName} value={plantName}>
                  {plantName}
                </option>
              ))}
            </select>
          </div>

          {/* Plant B Selection */}
          <div className="plant-selector">
            <label>Plant B</label>
            <select 
              value={plantB || ''} 
              onChange={(e) => setPlantB(e.target.value)}
              className="plant-select"
            >
              <option value="">Select a plant...</option>
              {Array.isArray(allPlants) && allPlants.map((plantName) => (
                <option key={plantName} value={plantName}>
                  {plantName}
                </option>
              ))}
            </select>
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
