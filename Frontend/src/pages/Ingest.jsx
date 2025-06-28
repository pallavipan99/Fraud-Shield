import React, { useState } from 'react'
import api from '../api'

export default function Ingest() {
  const [amount, setAmount] = useState(42)
  const [f, setF] = useState(Object.fromEntries(Array.from({length:30}, (_,i)=>[`f${i+1}`, 0])))
  const [res, setRes] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    const payload = { ...f, amount: Number(amount) }
    const r = await api.post('/transactions', payload)
    setRes(r.data)
  }

  const randomize = () => {
    const nf = {}
    for (let i=1;i<=30;i++) nf[`f${i}`] = Number((Math.random()*4-2).toFixed(3))
    setF(nf); setAmount(Number((Math.random()*500).toFixed(2)))
  }

  return (
    <div className="card">
      <div className="header"><h2>Ingest Transaction</h2><button className="button secondary" onClick={randomize}>Randomize</button></div>
      <form onSubmit={submit} className="grid">
        <div className="grid grid-2">
          <div><label>Amount</label><input className="input" type="number" step="0.01" value={amount} onChange={e=>setAmount(e.target.value)} /></div>
          <div></div>
          {Array.from({length:30}, (_,i)=> (
            <div key={i}><label>{`f${i+1}`}</label><input className="input" type="number" step="0.001" value={f[`f${i+1}`]} onChange={e=>setF({...f,[`f${i+1}`]: Number(e.target.value)})} /></div>
          ))}
        </div>
        <button className="button" type="submit">Score & Store</button>
      </form>
      {res && <div style={{marginTop:12}}>Scored: risk {(res.probability*100).toFixed(2)}% — Flagged: {res.flagged ? 'Yes' : 'No'}</div>}
    </div>
  )
}
