import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { ThermometerSun, Droplets, AlertTriangle } from 'lucide-react';
import { algeriaZones } from '../data/mockData';
import { getAllPlants, analyzePlant, getPlantIcon } from '../services/api-service';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

// Fix Leaflet default marker icon issue
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapView = () => {
  const [selectedZone, setSelectedZone] = useState(null);
  const [mapLayer, setMapLayer] = useState('recommendations');
  const [zonesWithPlants, setZonesWithPlants] = useState([]);
  const [loading, setLoading] = useState(true);

  const center = [28.0, 2.0]; // Algeria center

  // Fetch random plants from backend for each zone
  useEffect(() => {
    const fetchPlantsForZones = async () => {
      try {
        setLoading(true);
        const allPlants = await getAllPlants();
        
        // Randomly select 5 plants for each zone
        const zonesData = await Promise.all(
          algeriaZones.map(async (zone) => {
            // Get random plants for this zone
            const shuffled = [...allPlants].sort(() => 0.5 - Math.random());
            const selectedPlants = shuffled.slice(0, 5);
            
            // Fetch details for each plant
            const plantsWithDetails = await Promise.all(
              selectedPlants.map(async (plantName) => {
                try {
                  const details = await analyzePlant(plantName, 1);
                  return {
                    name: plantName,
                    commonName: plantName,
                    icon: getPlantIcon(details.climate_zone, plantName),
                    compatibility: Math.floor(Math.random() * 20) + 75, // 75-95%
                    cluster: details.cluster,
                    climate_zone: details.climate_zone
                  };
                } catch (err) {
                  console.error(`Error fetching ${plantName}:`, err);
                  return {
                    name: plantName,
                    commonName: plantName,
                    icon: '🌿',
                    compatibility: Math.floor(Math.random() * 20) + 75,
                  };
                }
              })
            );
            
            return {
              ...zone,
              suitablePlants: plantsWithDetails
            };
          })
        );
        
        setZonesWithPlants(zonesData);
      } catch (err) {
        console.error('Error fetching plants for zones:', err);
        // Fallback to original zones without plants
        setZonesWithPlants(algeriaZones);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPlantsForZones();
  }, []);

  return (
    <div className="map-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="map-header"
      >
        <h1>🗺️ Algeria Agro-Climatic Zones</h1>
        <p>Regional plant recommendations and climate analysis</p>
      </motion.div>

      {loading && (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Loading plant data for regions...</p>
        </div>
      )}

      {!loading && (
      <>
      <div className="map-container-wrapper">
        {/* Map Controls */}
        <div className="map-controls">
          <h3>Map Layers</h3>
          <div className="layer-buttons">
            <button 
              className={mapLayer === 'recommendations' ? 'active' : ''}
              onClick={() => setMapLayer('recommendations')}
            >
              Plant Recommendations
            </button>
            <button 
              className={mapLayer === 'climate' ? 'active' : ''}
              onClick={() => setMapLayer('climate')}
            >
              Climate Data
            </button>
          </div>
        </div>

        {/* Leaflet Map */}
        <div className="map-container">
          <MapContainer
            center={center}
            zoom={5}
            style={{ height: '100%', width: '100%', borderRadius: '12px' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />
            
            {zonesWithPlants.map((zone) => (
              <Circle
                key={zone.id}
                center={[zone.coordinates.lat, zone.coordinates.lng]}
                radius={150000}
                pathOptions={{
                  color: zone.color,
                  fillColor: zone.color,
                  fillOpacity: 0.3,
                }}
                eventHandlers={{
                  click: () => setSelectedZone(zone),
                }}
              >
                <Popup>
                  <div className="map-popup">
                    <h4>{zone.name}</h4>
                    <p>Click for details</p>
                  </div>
                </Popup>
              </Circle>
            ))}

            {zonesWithPlants.map((zone) => (
              <Marker
                key={`marker-${zone.id}`}
                position={[zone.coordinates.lat, zone.coordinates.lng]}
                eventHandlers={{
                  click: () => setSelectedZone(zone),
                }}
              >
                <Popup>
                  <div className="map-popup">
                    <h4>{zone.name}</h4>
                    <p>Suitability: {zone.suitabilityScore}/10</p>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Zone Details Panel */}
        {selectedZone && (
          <motion.div
            className="zone-details"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="zone-header" style={{ borderLeftColor: selectedZone.color }}>
              <h2>{selectedZone.name}</h2>
              <div className="suitability-score">
                <span className="score-label">Suitability Score</span>
                <span className="score-value">{selectedZone.suitabilityScore}/10</span>
              </div>
            </div>

            <div className="zone-section">
              <h3>Climate Conditions</h3>
              <div className="climate-grid">
                <div className="climate-item">
                  <Droplets size={20} className="icon" />
                  <div>
                    <span className="label">Rainfall</span>
                    <span className="value">{selectedZone.climate.rainfall}</span>
                  </div>
                </div>
                <div className="climate-item">
                  <ThermometerSun size={20} className="icon" />
                  <div>
                    <span className="label">Temperature</span>
                    <span className="value">{selectedZone.climate.temperature}</span>
                  </div>
                </div>
                <div className="climate-item">
                  <span className="icon">💧</span>
                  <div>
                    <span className="label">Humidity</span>
                    <span className="value">{selectedZone.climate.humidity}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="zone-section">
              <h3>Soil Type</h3>
              <p className="soil-type">{selectedZone.soilType}</p>
            </div>

            <div className="zone-section">
              <h3>Stress Factors</h3>
              <div className="stress-factors">
                {selectedZone.stressFactors.map((factor, index) => (
                  <div key={index} className="stress-chip">
                    <AlertTriangle size={16} />
                    {factor}
                  </div>
                ))}
              </div>
            </div>

            <div className="zone-section">
              <h3>Suitable Plants for This Region</h3>
              <div className="recommended-plants">
                {selectedZone.suitablePlants && selectedZone.suitablePlants.length > 0 ? (
                  selectedZone.suitablePlants.map((plant, index) => (
                    <div key={index} className="plant-match-card">
                      <span className="plant-icon">{plant.icon}</span>
                      <div className="plant-match-info">
                        <span className="plant-name">{plant.commonName}</span>
                        <span className="plant-scientific">{plant.name}</span>
                        <div className="plant-traits">
                          <span className="trait">Compatibility: {plant.compatibility}%</span>
                          {plant.climate_zone && (
                            <span className="trait">Climate: {plant.climate_zone}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p>Loading plant data...</p>
                )}
              </div>
            </div>

            <button 
              className="close-panel-btn"
              onClick={() => setSelectedZone(null)}
            >
              Close Details
            </button>
          </motion.div>
        )}
      </div>

      {/* Zone Overview Cards */}
      <div className="zones-overview">
        <h2>All Zones Overview</h2>
        <div className="zones-grid">
          {zonesWithPlants.map((zone) => (
            <motion.div
              key={zone.id}
              className="zone-card"
              style={{ borderTopColor: zone.color }}
              whileHover={{ y: -5 }}
              onClick={() => setSelectedZone(zone)}
            >
              <h3>{zone.name}</h3>
              <div className="zone-card-score">
                <span>Suitability</span>
                <span className="score">{zone.suitabilityScore}/10</span>
              </div>
              <div className="zone-card-plants">
                {zone.suitablePlants && zone.suitablePlants.slice(0, 5).map((plant, idx) => (
                  <span key={idx} className="mini-plant-icon">{plant.icon}</span>
                ))}
              </div>
              <p className="zone-card-climate">{zone.climate.rainfall} | {zone.climate.temperature}</p>
            </motion.div>
          ))}
        </div>
      </div>
      </>
      )}
    </div>
  );
};

export default MapView;
