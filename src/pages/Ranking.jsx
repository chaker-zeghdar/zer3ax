import { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Filter, Star, Award } from 'lucide-react';
import { rankedPlants } from '../data/mockData';
import './Ranking.css';

const Ranking = () => {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('hybrid');

  const filteredPlants = rankedPlants.filter(plant => {
    if (filter === 'all') return true;
    if (filter === 'northern') return plant.optimalZone === 'Northern';
    if (filter === 'plateau') return plant.optimalZone === 'High Plateau';
    if (filter === 'sahara') return plant.optimalZone === 'Sahara';
    if (filter === 'drought') return plant.resistance.drought >= 7;
    return true;
  });

  const sortedPlants = [...filteredPlants].sort((a, b) => {
    if (sortBy === 'hybrid') return b.hybridPotentialScore - a.hybridPotentialScore;
    if (sortBy === 'adaptability') return b.environmentalAdaptability - a.environmentalAdaptability;
    if (sortBy === 'yield') return b.yieldPotential - a.yieldPotential;
    if (sortBy === 'diversity') return b.geneticDiversity - a.geneticDiversity;
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
        <h1>🏆 Plant Rankings</h1>
        <p>Performance-based ranking with advanced filtering</p>
      </motion.div>

      {/* Top Recommendation of the Week */}
      {topRecommendation && (
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
              <h2>{topRecommendation.commonName}</h2>
              <p className="scientific-name">{topRecommendation.name}</p>
              <div className="stats">
                <div className="stat">
                  <span className="stat-label">Hybrid Score:</span>
                  <span className="stat-value">{topRecommendation.hybridPotentialScore.toFixed(1)}/10</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Zone:</span>
                  <span className="stat-value">{topRecommendation.optimalZone}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Rating:</span>
                  <span className="stat-value">{'⭐'.repeat(topRecommendation.overallRating)}</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Filters */}
      <div className="filters-section">
        <div className="filter-group">
          <Filter size={20} />
          <label>Zone Filter:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Zones</option>
            <option value="northern">Northern</option>
            <option value="plateau">High Plateau</option>
            <option value="sahara">Sahara</option>
            <option value="drought">High Drought Tolerance</option>
          </select>
        </div>

        <div className="filter-group">
          <TrendingUp size={20} />
          <label>Sort By:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="hybrid">Hybrid Potential</option>
            <option value="adaptability">Environmental Adaptability</option>
            <option value="yield">Yield Potential</option>
            <option value="diversity">Genetic Diversity</option>
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
              <th>Adaptability</th>
              <th>Genetic Diversity</th>
              <th>Zone</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {sortedPlants.map((plant, index) => (
              <motion.tr
                key={plant.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
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
                      <div className="plant-name">{plant.commonName}</div>
                      <div className="plant-scientific">{plant.name}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <div className="score-cell">
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ width: `${(plant.hybridPotentialScore / 10) * 100}%` }}
                      />
                    </div>
                    <span className="score-value">{plant.hybridPotentialScore.toFixed(1)}</span>
                  </div>
                </td>
                <td>
                  <div className="score-cell">
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ width: `${(plant.environmentalAdaptability / 10) * 100}%` }}
                      />
                    </div>
                    <span className="score-value">{plant.environmentalAdaptability.toFixed(1)}</span>
                  </div>
                </td>
                <td>
                  <div className="score-cell">
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ width: `${(plant.geneticDiversity / 10) * 100}%` }}
                      />
                    </div>
                    <span className="score-value">{plant.geneticDiversity.toFixed(1)}</span>
                  </div>
                </td>
                <td>
                  <span className="zone-badge">{plant.optimalZone}</span>
                </td>
                <td>
                  <div className="rating-stars">
                    {'⭐'.repeat(plant.overallRating)}
                  </div>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </div>
  );
};

export default Ranking;
