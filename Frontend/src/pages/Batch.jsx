import React, { useState } from 'react'
import api from '../api'

export default function Batch() {
  const [jsonText, setJsonText] = useState('[{"f1":0.2,"f2":-1.1,"amount":120.50}]')
  const [result, setResult] = useState(null)
  const submit = async () => {
    try {
      const payload = JSON.parse(jsonText)
      const res = await api.post('/batch-score', payload)
      setResult(res.data)
    } catch (e) {
      alert('Invalid JSON')
    }
  }
  return (
    <div className="card">
      <div className="header"><h2>Batch Score</h2></div>
      <textarea className="textarea" rows="10" value={jsonText} onChange={e=>setJsonText(e.target.value)} />
      <div style={{marginTop:8}}><button className="button" onClick={submit}>Score</button></div>
      {result && <pre style={{marginTop:12, background:'#0e1627', padding:12, borderRadius:10}}>{JSON.stringify(result,null,2)}</pre>}
    </div>
  )
}