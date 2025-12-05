import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Filter, Star, Award } from 'lucide-react';
import { getGlobalStats, getAllClusters, getPlantIcon } from '../services/api-service';
import './Ranking.css';

const Ranking = () => {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('hybrid');
  const [rankedPlants, setRankedPlants] = useState([]);
  const [allClusters, setAllClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [stats, clusters] = await Promise.all([
          getGlobalStats(),
          getAllClusters()
        ]);
        
        // Transform cluster data into ranked plants
        const plants = [];
        clusters.forEach(cluster => {
          cluster.plants.forEach(plantName => {
            plants.push({
              name: plantName,
              cluster: cluster.cluster_id,
              hybridPotentialScore: cluster.avg_hybridization_score,
              climateZone: Object.keys(cluster.climate_zones)[0] || 'Unknown',
              plantCount: cluster.plant_count,
              icon: getPlantIcon(Object.keys(cluster.climate_zones)[0], plantName)
            });
          });
        });
        
        setAllClusters(clusters);
        setRankedPlants(plants);
      } catch (err) {
        console.error('Error fetching ranking data:', err);
        setError('Failed to load ranking data. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredPlants = rankedPlants.filter(plant => {
    if (filter === 'all') return true;
    if (filter === 'tropical') return plant.climateZone === 'Tropical';
    if (filter === 'temperate') return plant.climateZone === 'Temperate';
    if (filter === 'arid') return plant.climateZone === 'Arid';
    if (filter === 'cold') return plant.climateZone === 'Cold';
    if (filter === 'high-score') return plant.hybridPotentialScore >= 0.7;
    return true;
  });

  const sortedPlants = [...filteredPlants].sort((a, b) => {
    if (sortBy === 'hybrid') return b.hybridPotentialScore - a.hybridPotentialScore;
    if (sortBy === 'cluster') return a.cluster - b.cluster;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });

  const topRecommendation = sortedPlants[0];

  return (
    <div className="ranking-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="ranking-header"
      >
        <h1>Plant Rankings</h1>
        <p>Performance-based ranking with advanced filtering</p>
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

      {loading && (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Loading ranking data...</p>
        </div>
      )}

      {!loading && topRecommendation && (
        <motion.div
          className="top-recommendation"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="recommendation-badge">
            <Award size={24} />
            <span>Top Recommendation of the Week</span>
          </div>
          <div className="recommendation-content">
            <span className="plant-icon-large">{topRecommendation.icon}</span>
            <div className="recommendation-info">
              <h2>{topRecommendation.name}</h2>
              <p className="scientific-name">Cluster {topRecommendation.cluster}</p>
              <div className="stats">
                <div className="stat">
                  <span className="stat-label">Hybrid Score:</span>
                  <span className="stat-value">{(topRecommendation.hybridPotentialScore * 10).toFixed(1)}/10</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Zone:</span>
                  <span className="stat-value">{topRecommendation.climateZone}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Cluster:</span>
                  <span className="stat-value">{topRecommendation.cluster}</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {!loading && (
        <>
          <div className="filters-section">
            <div className="filter-group">
              <Filter size={20} />
              <label>Zone Filter:</label>
              <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                <option value="all">All Zones</option>
                <option value="tropical">Tropical</option>
                <option value="temperate">Temperate</option>
                <option value="arid">Arid</option>
                <option value="cold">Cold</option>
                <option value="high-score">High Score (≥0.7)</option>
              </select>
            </div>

            <div className="filter-group">
              <TrendingUp size={20} />
              <label>Sort By:</label>
              <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                <option value="hybrid">Hybrid Potential</option>
                <option value="cluster">Cluster</option>
                <option value="name">Name</option>
              </select>
            </div>
          </div>

          {/* Ranking Table */}
          <motion.div
            className="ranking-table-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <table className="ranking-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Plant</th>
                  <th>Hybrid Score</th>
                  <th>Cluster</th>
                  <th>Zone</th>
                </tr>
              </thead>
              <tbody>
                {sortedPlants.slice(0, 100).map((plant, index) => (
                  <motion.tr
                    key={`${plant.name}-${plant.cluster}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.02 }}
                    className={index === 0 ? 'top-rank' : ''}
                  >
                    <td className="rank-cell">
                      <div className={`rank-badge ${index < 3 ? 'medal' : ''}`}>
                        {index === 0 && '🥇'}
                        {index === 1 && '🥈'}
                        {index === 2 && '🥉'}
                        {index > 2 && `#${index + 1}`}
                      </div>
                    </td>
                    <td>
                      <div className="plant-cell">
                        <span className="plant-icon">{plant.icon}</span>
                        <div>
                          <div className="plant-name">{plant.name}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="score-cell">
                        <div className="score-bar">
                          <div 
                            className="score-fill"
                            style={{ width: `${plant.hybridPotentialScore * 100}%` }}
                          />
                        </div>
                        <span className="score-value">{(plant.hybridPotentialScore * 10).toFixed(1)}</span>
                      </div>
                    </td>
                    <td>
                      <span className="zone-badge">{plant.cluster}</span>
                    </td>
                    <td>
                      <span className="zone-badge">{plant.climateZone}</span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        </>
      )}
    </div>
  );
};

export default Ranking;
