import React from 'react';
import './App.css';
import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PillarDetail from './components/PillarDetail';
import { pillarData } from './data/pillarData';

function App() {
  return (
    <div className="app-shell">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        {pillarData.map((pillar) => (
          <Route key={pillar.slug} path={pillar.route} element={<PillarDetail />} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
