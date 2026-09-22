import React from 'react';
import './App.css';
import { Navigate, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PillarDetail from './components/PillarDetail';
import { pillarData } from './data/pillarData';
import GovernanceQuestionnaire from './components/GovernanceQuestionnaire';
import FinancialRiskDashboard from './components/FinancialRiskDashboard';

function App() {
  return (
    <div className="app-shell">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/governance-assessment" element={<GovernanceQuestionnaire />} />
        <Route path="/financial-risk" element={<FinancialRiskDashboard />} />
        {pillarData.map((pillar) => (
          <Route key={pillar.slug} path={pillar.route} element={<PillarDetail />} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
