import React, { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

function App() {
  const [features, setFeatures] = useState(Array(10).fill(""));
  const [results, setResults] = useState([]);

  const handleChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

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
