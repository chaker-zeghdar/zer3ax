import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';
import { searchPlants, comparePlants, analyzePlant, getCompatibilityRating } from '../services/api-service';
import './Compare.css';

const Compare = () => {
  const [plantA, setPlantA] = useState('');
  const [plantB, setPlantB] = useState('');
  const [allPlants, setAllPlants] = useState([]);
  const [searchQueryA, setSearchQueryA] = useState('');
  const [searchQueryB, setSearchQueryB] = useState('');
  const [plantADetails, setPlantADetails] = useState(null);
  const [plantBDetails, setPlantBDetails] = useState(null);
  const [comparison, setComparison] = useState(null);
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

  // Fetch plant details and compare when both plants are selected
  useEffect(() => {
    const fetchComparison = async () => {
      if (plantA && plantB) {
        setLoading(true);
        setError(null);
        try {
          const [detailsA, detailsB, comparisonResult] = await Promise.all([
            analyzePlant(plantA, 3),
            analyzePlant(plantB, 3),
            comparePlants(plantA, plantB)
          ]);
          setPlantADetails(detailsA);
          setPlantBDetails(detailsB);
          setComparison(comparisonResult);
        } catch (err) {
          console.error('Comparison error:', err);
          setError(err.message || 'Failed to compare plants.');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchComparison();
  }, [plantA, plantB]);

  const generateFakeReasoning = () => {
    if (!comparison || !plantADetails || !plantBDetails) return [];
    
    const reasons = [];
    const cA = plantADetails.cluster;
    const cB = plantBDetails.cluster;
    const distance = comparison.distance;
    
    // Cluster comparison
    if (cA === cB) {
      reasons.push("Both plants belong to the same cluster, indicating overall structural and biological similarity.");
    } else {
      reasons.push("The two plants belong to different clusters, indicating biological structural differences.");
    }
    
    // Climate zone
    if (plantADetails.climate_zone === plantBDetails.climate_zone) {
      reasons.push("Both plants are adapted to the same climatic zone, which increases the likelihood of hybridization.");
    } else {
      reasons.push("Different climatic zones reduce the likelihood of natural hybridization.");
    }
    
    // Hybridization potential
    if (plantADetails.hybridization_score > 0.3 && plantBDetails.hybridization_score > 0.3) {
      reasons.push("Both plants have a high genetic hybridization potential.");
    } else if (plantADetails.hybridization_score < 0.1 && plantBDetails.hybridization_score < 0.1) {
      reasons.push("Both plants have a very low hybridization potential.");
    } else {
      reasons.push("Only one of the plants has a high hybridization potential.");
    }
    
    // Distance analysis
    if (distance < 1.5) {
      reasons.push("The biological distance is very small, indicating strong genetic similarity.");
    } else if (distance < 3) {
      reasons.push("There is moderate genetic similarity between the two plants.");
    } else {
      reasons.push("The biological distance is large, indicating clear genetic differences.");
    }
    
    // Conclusion
    if (distance < 1.5 && cA === cB && plantADetails.climate_zone === plantBDetails.climate_zone) {
      reasons.push("✅ Conclusion: Conditions are ideal for successful natural hybridization.");
    } else if (distance < 3) {
      reasons.push("⚠️ Conclusion: Hybridization is possible but moderately stable.");
    } else {
      reasons.push("❌ Conclusion: Hybridization is weak and genetically unstable.");
    }
    
    return reasons;
  };

  const compareTraits = () => {
    if (!comparison || !plantADetails || !plantBDetails) return null;

    const compatibility = getCompatibilityRating(comparison.distance, comparison.same_cluster);
    
    let summary = `These plants show ${compatibility.level.toLowerCase()} compatibility with a distance of ${comparison.distance.toFixed(2)}. `;
    
    if (comparison.same_cluster) {
      summary += 'They belong to the same cluster, which increases hybridization potential. ';
    } else {
      summary += 'They are in different clusters. ';
    }
    
    if (plantADetails.climate_zone === plantBDetails.climate_zone) {
      summary += `Both thrive in ${plantADetails.climate_zone} climate zones.`;
    } else {
      summary += `${plantA} prefers ${plantADetails.climate_zone} while ${plantB} prefers ${plantBDetails.climate_zone} conditions.`;
    }

    return summary;
  };

  // Filter plants based on search queries
  const filteredPlantsA = allPlants.filter(plant => 
    plant.toLowerCase().includes(searchQueryA.toLowerCase())
  );

  const filteredPlantsB = allPlants.filter(plant => 
    plant.toLowerCase().includes(searchQueryB.toLowerCase())
  );

  const getNumericalComparisonData = () => {
    if (!plantADetails || !plantBDetails) return [];

    return [
      {
        trait: 'Hybridization Score',
        plantA: (plantADetails.hybridization_score * 10).toFixed(1),
        plantB: (plantBDetails.hybridization_score * 10).toFixed(1)
      },
      {
        trait: 'Cluster Proximity',
        plantA: comparison?.same_cluster ? 10 : 5,
        plantB: comparison?.same_cluster ? 10 : 5
      }
    ];
  };

  return (
    <div className="compare-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="compare-header"
      >
        <h1>Species Comparison</h1>
        <p>Side-by-side trait comparison and compatibility analysis</p>
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
      <div className="selection-section">
        <div className="selector-card">
          <label>Plant A</label>
          <input
            type="text"
            placeholder="Search plants..."
            value={searchQueryA}
            onChange={(e) => setSearchQueryA(e.target.value)}
            className="search-input"
            style={{
              width: '100%',
              padding: '0.5rem',
              marginBottom: '0.5rem',
              border: '1px solid var(--border-color)',
              borderRadius: '4px',
              fontSize: '0.9rem'
            }}
          />
          <select 
            value={plantA} 
            onChange={(e) => setPlantA(e.target.value)}
            className="plant-select"
          >
            <option value="">Select a plant...</option>
            {filteredPlantsA.map((plantName) => (
              <option key={plantName} value={plantName}>
                {plantName}
              </option>
            ))}
          </select>
          {searchQueryA && (
            <div style={{ fontSize: '0.8rem', marginTop: '0.25rem', color: 'var(--text-secondary)' }}>
              {filteredPlantsA.length} plant{filteredPlantsA.length !== 1 ? 's' : ''} found
            </div>
          )}
        </div>

        <div className="vs-divider">
          <ArrowRight size={32} />
        </div>

        <div className="selector-card">
          <label>Plant B</label>
          <input
            type="text"
            placeholder="Search plants..."
            value={searchQueryB}
            onChange={(e) => setSearchQueryB(e.target.value)}
            className="search-input"
            style={{
              width: '100%',
              padding: '0.5rem',
              marginBottom: '0.5rem',
              border: '1px solid var(--border-color)',
              borderRadius: '4px',
              fontSize: '0.9rem'
            }}
          />
          <select 
            value={plantB} 
            onChange={(e) => setPlantB(e.target.value)}
            className="plant-select"
          >
            <option value="">Select a plant...</option>
            {filteredPlantsB.map((plantName) => (
              <option key={plantName} value={plantName}>
                {plantName}
              </option>
            ))}
          </select>
          {searchQueryB && (
            <div style={{ fontSize: '0.8rem', marginTop: '0.25rem', color: 'var(--text-secondary)' }}>
              {filteredPlantsB.length} plant{filteredPlantsB.length !== 1 ? 's' : ''} found
            </div>
          )}
        </div>
      </div>

      {/* Comparison Display */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Loading comparison...</p>
        </div>
      )}
      
      {plantADetails && plantBDetails && comparison && !loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="comparison-results"
        >
          {/* Summary */}
          <div className="comparison-summary">
            <h3>Comparison Summary</h3>
            <p>{compareTraits()}</p>
            {comparison.recommendation && (
              <p style={{ marginTop: '0.5rem', fontStyle: 'italic', color: 'var(--primary-green)' }}>
                💡 {comparison.recommendation}
              </p>
            )}
            
            {/* Detailed Reasoning */}
            <div style={{ marginTop: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.75rem', fontSize: '1.1rem' }}>Detailed Analysis</h4>
              <ul style={{ 
                listStyle: 'none', 
                padding: 0,
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem'
              }}>
                {generateFakeReasoning().map((reason, index) => (
                  <li key={index} style={{ 
                    padding: '0.75rem',
                    background: 'var(--bg-secondary)',
                    borderRadius: '6px',
                    borderLeft: '3px solid var(--primary-green)',
                    fontSize: '0.95rem',
                    lineHeight: '1.5'
                  }}>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Side-by-Side Cards */}
          <div className="comparison-cards">
            <div className="plant-card">
              <div className="plant-card-header" style={{ background: 'linear-gradient(135deg, var(--primary-green) 0%, var(--accent-green) 100%)' }}>
                <span className="plant-icon-large">🌿</span>
                <h3>{plantA}</h3>
                <p className="scientific-name">Cluster {plantADetails.cluster}</p>
              </div>
              <div className="plant-card-body">
                <TraitRow label="Hybridization Score" value={plantADetails.hybridization_score.toFixed(2)} icon="🧬" />
                <TraitRow label="Climate Zone" value={plantADetails.climate_zone} icon="🌍" />
                <TraitRow label="Cluster" value={plantADetails.cluster} icon="📊" />
              </div>
            </div>

            <div className="plant-card">
              <div className="plant-card-header" style={{ background: 'linear-gradient(135deg, var(--primary-brown) 0%, var(--accent-brown) 100%)' }}>
                <span className="plant-icon-large">🌿</span>
                <h3>{plantB}</h3>
                <p className="scientific-name">Cluster {plantBDetails.cluster}</p>
              </div>
              <div className="plant-card-body">
                <TraitRow label="Hybridization Score" value={plantBDetails.hybridization_score.toFixed(2)} icon="🧬" />
                <TraitRow label="Climate Zone" value={plantBDetails.climate_zone} icon="🌍" />
                <TraitRow label="Cluster" value={plantBDetails.cluster} icon="📊" />
              </div>
            </div>
          </div>

          {/* Compatibility Metrics */}
          <div className="chart-section">
            <h3>Compatibility Analysis</h3>
            <div style={{ padding: '1rem', background: 'var(--bg-secondary)', borderRadius: '8px', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div>
                  <strong>Distance:</strong> {comparison.distance.toFixed(2)}
                </div>
                <div>
                  <strong>Compatibility:</strong> {comparison.compatibility}
                </div>
                <div>
                  <strong>Same Cluster:</strong> {comparison.same_cluster ? '✅ Yes' : '❌ No'}
                </div>
              </div>
            </div>
            
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={getNumericalComparisonData()}>
                <XAxis dataKey="trait" angle={-15} textAnchor="end" height={100} tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="plantA" name={plantA} fill="var(--primary-green)" radius={[8, 8, 0, 0]} />
                <Bar dataKey="plantB" name={plantB} fill="var(--primary-brown)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </div>
  );
};

const TraitRow = ({ label, value, icon }) => (
  <div className="trait-row">
    <span className="trait-icon">{icon}</span>
    <span className="trait-label">{label}:</span>
    <span className="trait-value">{value}</span>
  </div>
);

export default Compare;
