import React from 'react'
import './App.css'
import { Navigate, Route, Routes } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import PillarDetail from './components/PillarDetail'

function App() {
  return React.createElement(
    'div',
    { className: 'app' },
    React.createElement(Routes, null,
      React.createElement(Route, { path: '/', element: React.createElement(Dashboard) }),
      React.createElement(Route, { path: '/pillar/:pillarSlug', element: React.createElement(PillarDetail) }),
      React.createElement(Route, { path: '*', element: React.createElement(Navigate, { to: '/', replace: true }) })
    )
  )
}

export default App
