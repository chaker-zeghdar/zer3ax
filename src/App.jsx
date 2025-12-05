import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './components/Layout';
import Home from './pages/Home';
import Predict from './pages/Predict';
import Compare from './pages/Compare';
import Ranking from './pages/Ranking';
import MapView from './pages/MapView';
import Chatbot from './pages/Chatbot';
import './App.css';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/ranking" element={<Ranking />} />
          <Route path="/map" element={<MapView />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;