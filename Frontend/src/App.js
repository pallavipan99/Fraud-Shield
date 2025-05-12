import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

function App() {
  const [features, setFeatures] = useState(Array(10).fill(""));
  const [results, setResults] = useState([]);
  const [streamAlerts, setStreamAlerts] = useState([]);

  const handleChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  // Example: fetch streaming alerts from backend
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch("http://localhost:5000/api/stream-fraud");
        const data = await response.json();
        if (data.length > 0) setStreamAlerts(prev => [...data, ...prev]);
      } catch (err) {
        console.error("Error fetching stream alerts:", err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Fraud Shield Dashboard</h1>

      <div style={{ marginTop: "30px" }}>
        <h2 style={{ color: "#b71c1c" }}>🚨 Streaming Fraud Alerts</h2>
        {streamAlerts.length > 0 ? (
          <ul style={{
            listStyle: "none",
            padding: 0,
            maxHeight: "250px",
            overflowY: "auto",
            border: "1px solid #f5c6cb",
            borderRadius: "8px",
            backgroundColor: "#fff0f0"
          }}>
            {streamAlerts.map((alert, idx) => (
              <li key={idx} style={{
                padding: "10px",
                margin: "5px",
                borderBottom: "1px solid #f5c6cb",
                borderRadius: "5px",
                backgroundColor: "#ffe6e6",
                fontWeight: "bold"
              }}>
                <div>Transaction ID: {alert.transactionId}</div>
                <div>Fraud probability: {alert.probability.toFixed(4)}</div>
                <div style={{ fontSize: "0.8rem", color: "#333" }}>
                  Timestamp: {new Date(alert.timestamp).toLocaleString()}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ color: "#555" }}>No new fraud alerts.</p>
        )}
      </div>

      <div style={{ marginTop: "30px" }}>
        <h2>Fraud Probability Chart</h2>
        <BarChart width={600} height={300} data={results}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="transactionId" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="probability" fill="#b71c1c" />
        </BarChart>
      </div>
    </div>
  );
}

export default App;

