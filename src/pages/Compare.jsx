import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, ChevronDown, ArrowRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { plants } from '../data/mockData';
import './Compare.css';

const Compare = () => {
  const [plantA, setPlantA] = useState(null);
  const [plantB, setPlantB] = useState(null);
  const [searchA, setSearchA] = useState('');
  const [searchB, setSearchB] = useState('');
  const [showDropdownA, setShowDropdownA] = useState(false);
  const [showDropdownB, setShowDropdownB] = useState(false);

  const filteredPlantsA = plants.filter(p => 
    p.name.toLowerCase().includes(searchA.toLowerCase()) ||
    p.commonName.toLowerCase().includes(searchA.toLowerCase())
  );

  const filteredPlantsB = plants.filter(p => 
    p.name.toLowerCase().includes(searchB.toLowerCase()) ||
    p.commonName.toLowerCase().includes(searchB.toLowerCase())
  );

  const compareTraits = () => {
    if (!plantA || !plantB) return null;

    const droughtDiff = plantA.resistance.drought - plantB.resistance.drought;
    const salinityDiff = plantA.resistance.salinity - plantB.resistance.salinity;
    const yieldDiff = plantA.yieldPotential - plantB.yieldPotential;

    let summary = '';
    if (droughtDiff > 0) {
      summary += `${plantA.commonName} shows stronger drought tolerance. `;
    } else if (droughtDiff < 0) {
      summary += `${plantB.commonName} shows stronger drought tolerance. `;
    }

    if (Math.abs(plantA.genomeSize - plantB.genomeSize) < 5000) {
      summary += 'Both plants have compatible genome sizes. ';
    } else {
      summary += 'Significant genome size difference detected. ';
    }

    if (plantA.pollinationType === plantB.pollinationType) {
      summary += 'Same pollination type increases compatibility.';
    }

    return summary || 'These plants have mixed compatibility factors.';
  };

  const getNumericalComparisonData = () => {
    if (!plantA || !plantB) return [];

    return [
      {
        trait: 'Drought Resistance',
        plantA: plantA.resistance.drought,
        plantB: plantB.resistance.drought
      },
      {
        trait: 'Salinity Resistance',
        plantA: plantA.resistance.salinity,
        plantB: plantB.resistance.salinity
      },
      {
        trait: 'Disease Resistance',
        plantA: plantA.resistance.disease,
        plantB: plantB.resistance.disease
      },
      {
        trait: 'Yield Potential',
        plantA: plantA.yieldPotential,
        plantB: plantB.yieldPotential
      },
      {
        trait: 'Genetic Diversity',
        plantA: plantA.geneticDiversity,
        plantB: plantB.geneticDiversity
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
        <h1>📊 Species Comparison</h1>
        <p>Side-by-side trait comparison and compatibility analysis</p>
      </motion.div>

      {/* Selection Section */}
      <div className="selection-section">
        <div className="selector-card">
          <label>Plant A</label>
          <div className="dropdown-container">
            <div className="search-input-wrapper" onClick={() => setShowDropdownA(true)}>
              <Search size={18} className="search-icon" />
              <input
                type="text"
                placeholder="Select plant A..."
                value={plantA ? `${plantA.icon} ${plantA.name}` : searchA}
                onChange={(e) => {
                  setSearchA(e.target.value);
                  setPlantA(null);
                  setShowDropdownA(true);
                }}
                onFocus={() => setShowDropdownA(true)}
              />
              <ChevronDown size={18} />
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

        <div className="vs-divider">
          <ArrowRight size={32} />
        </div>

        <div className="selector-card">
          <label>Plant B</label>
          <div className="dropdown-container">
            <div className="search-input-wrapper" onClick={() => setShowDropdownB(true)}>
              <Search size={18} className="search-icon" />
              <input
                type="text"
                placeholder="Select plant B..."
                value={plantB ? `${plantB.icon} ${plantB.name}` : searchB}
                onChange={(e) => {
                  setSearchB(e.target.value);
                  setPlantB(null);
                  setShowDropdownB(true);
                }}
                onFocus={() => setShowDropdownB(true)}
              />
              <ChevronDown size={18} />
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
      </div>

      {/* Comparison Display */}
      {plantA && plantB && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="comparison-results"
        >
          {/* Summary */}
          <div className="comparison-summary">
            <h3>Comparison Summary</h3>
            <p>{compareTraits()}</p>
          </div>

          {/* Side-by-Side Cards */}
          <div className="comparison-cards">
            <div className="plant-card">
              <div className="plant-card-header" style={{ background: 'linear-gradient(135deg, var(--primary-green) 0%, var(--accent-green) 100%)' }}>
                <span className="plant-icon-large">{plantA.icon}</span>
                <h3>{plantA.commonName}</h3>
                <p className="scientific-name">{plantA.name}</p>
              </div>
              <div className="plant-card-body">
                <TraitRow label="Perenniality" value={plantA.perenniality} icon="🔄" />
                <TraitRow label="Woodiness" value={plantA.woodiness} icon="🌳" />
                <TraitRow label="Pollination" value={plantA.pollinationType} icon="🐝" />
                <TraitRow label="Genome Size" value={`${plantA.genomeSize} Mb`} icon="🧬" />
                <TraitRow label="Growth Form" value={plantA.growthForm} icon="🌱" />
                <TraitRow label="Root Depth" value={plantA.rootDepth} icon="🌿" />
                <TraitRow label="Lifespan" value={plantA.lifespan} icon="⏳" />
                <TraitRow label="Optimal Zone" value={plantA.optimalZone} icon="📍" />
                <TraitRow label="Soil Type" value={plantA.soilPreference} icon="🪨" />
                <TraitRow label="Rainfall" value={plantA.environmentalFactor.rainfall} icon="💧" />
                <TraitRow label="Temperature" value={plantA.environmentalFactor.temperature} icon="🌡️" />
              </div>
            </div>

            <div className="plant-card">
              <div className="plant-card-header" style={{ background: 'linear-gradient(135deg, var(--primary-brown) 0%, var(--accent-brown) 100%)' }}>
                <span className="plant-icon-large">{plantB.icon}</span>
                <h3>{plantB.commonName}</h3>
                <p className="scientific-name">{plantB.name}</p>
              </div>
              <div className="plant-card-body">
                <TraitRow label="Perenniality" value={plantB.perenniality} icon="🔄" />
                <TraitRow label="Woodiness" value={plantB.woodiness} icon="🌳" />
                <TraitRow label="Pollination" value={plantB.pollinationType} icon="🐝" />
                <TraitRow label="Genome Size" value={`${plantB.genomeSize} Mb`} icon="🧬" />
                <TraitRow label="Growth Form" value={plantB.growthForm} icon="🌱" />
                <TraitRow label="Root Depth" value={plantB.rootDepth} icon="🌿" />
                <TraitRow label="Lifespan" value={plantB.lifespan} icon="⏳" />
                <TraitRow label="Optimal Zone" value={plantB.optimalZone} icon="📍" />
                <TraitRow label="Soil Type" value={plantB.soilPreference} icon="🪨" />
                <TraitRow label="Rainfall" value={plantB.environmentalFactor.rainfall} icon="💧" />
                <TraitRow label="Temperature" value={plantB.environmentalFactor.temperature} icon="🌡️" />
              </div>
            </div>
          </div>

          {/* Numerical Comparison Chart */}
          <div className="chart-section">
            <h3>Resistance & Performance Metrics</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={getNumericalComparisonData()}>
                <XAxis dataKey="trait" angle={-15} textAnchor="end" height={100} tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="plantA" name={plantA.commonName} fill="var(--primary-green)" radius={[8, 8, 0, 0]} />
                <Bar dataKey="plantB" name={plantB.commonName} fill="var(--primary-brown)" radius={[8, 8, 0, 0]} />
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
