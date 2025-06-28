import React, { useEffect, useState } from 'react'
import api from '../api'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({ total:0, flagged:0, flagged_rate:0, timeseries:[] })
  const [recent, setRecent] = useState([])

  const load = async () => {
    const m = await api.get('/metrics'); setMetrics(m.data)
    const r = await api.get('/transactions', { params:{ limit: 15 } }); setRecent(r.data)
  }

  useEffect(()=>{
    load(); const t = setInterval(load, 3000); return () => clearInterval(t)
  }, [])

  const COLORS = ['#4f8cff', '#ff7e6b']

  return (
    <div className="grid grid-2">
      <div className="card">
        <div className="header"><h3>Overview</h3></div>
        <div className="grid" style={{gridTemplateColumns:'repeat(3,1fr)'}}>
          <div className="kpi"><div>Total</div><div className="value">{metrics.total}</div></div>
          <div className="kpi"><div>Flagged</div><div className="value">{metrics.flagged}</div></div>
          <div className="kpi"><div>Flag Rate</div><div className="value">{(metrics.flagged_rate*100).toFixed(2)}%</div></div>
        </div>
        <div style={{height:280, marginTop:12}}>
          <ResponsiveContainer>
            <LineChart data={metrics.timeseries.map((d,i)=>({t:d.t.slice(11,19), v:d.flagged}))}>
              <XAxis dataKey="t" /><YAxis allowDecimals={false} /><Tooltip />
              <Line type="monotone" dataKey="v" stroke="#4f8cff" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="card">
        <div className="header"><h3>Recent Transactions</h3></div>
        <table className="table">
          <thead><tr><th>Time</th><th>Amount</th><th>Risk</th><th>Flag</th></tr></thead>
          <tbody>
            {recent.map(r => (
              <tr key={r.id}>
                <td>{new Date(r.ts).toLocaleTimeString()}</td>
                <td>${r.amount?.toFixed(2)}</td>
                <td>{(r.probability*100).toFixed(2)}%</td>
                <td>{r.flagged ? 'Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
