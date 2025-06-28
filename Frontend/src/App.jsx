import React, { useEffect, useState } from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Ingest from './pages/Ingest'
import Batch from './pages/Batch'
import api from './api'

function Navbar() {
  return (
    <div className="card" style={{marginBottom:16}}>
      <div className="nav">
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/ingest">Ingest</NavLink>
        <NavLink to="/batch">Batch Score</NavLink>
        <div style={{marginLeft:'auto', opacity:0.8}}>
          <Health />
        </div>
      </div>
    </div>
  )
}

function Health() {
  const [state, setState] = useState({status:'...', model_loaded:false})
  useEffect(()=>{ api.get('/health').then(res=>setState(res.data)).catch(()=>setState({status:'down'})) },[])
  return <span>API: {state.status} {state.model_loaded ? '✓ model' : '× model'}</span>
}

export default function App() {
  return (
    <div className="container">
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/ingest" element={<Ingest />} />
        <Route path="/batch" element={<Batch />} />
      </Routes>
    </div>
  )
}
