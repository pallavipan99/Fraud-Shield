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

  const handlePredict = async () => {
    try {
      const numericFeatures = features.map(f => parseFloat(f));
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: [numericFeatures] }),
      });
      const data = await response.json();
      if (Array.isArray(data)) {
        setResults(data);
      } else {
        setResults([{ prediction: "Error", probabilities: [] }]);
      }
    } catch (error) {
      console.error(error);
      setResults([{ prediction: "Error", probabilities: [] }]);
    }
  };

  const fraudCount = results.filter(r => r.prediction === 1).length;
  const nonFraudCount = results.filter(r => r.prediction === 0).length;
  const chartData = [
    { name: "Non-Fraud", count: nonFraudCount },
    { name: "Fraud", count: fraudCount },
  ];
  const flaggedTransactions = results
    .map((res, idx) => ({ ...res, transaction: idx + 1 }))
    .filter(res => res.prediction === 1);

  return (
    <div style={{
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      margin: "50px auto",
      maxWidth: "900px",
      textAlign: "center",
      backgroundColor: "#f9f9f9",
      padding: "20px",
      borderRadius: "10px",
      boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
    }}>
      <h1 style={{ color: "#007BFF", marginBottom: "20px" }}>🚀 Fraud Shield</h1>
      <p style={{ marginBottom: "30px", fontSize: "16px" }}>Enter transaction features below to get fraud predictions:</p>

      <form
        onSubmit={e => { e.preventDefault(); handlePredict(); }}
        style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "10px", marginBottom: "30px" }}
      >
        {features.map((f, i) => (
          <input
            key={i}
            type="number"
            placeholder={`Feature ${i + 1}`}
            value={features[i]}
            onChange={e => handleChange(i, e.target.value)}
            style={{ width: "80px", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
          />
        ))}
        <button
          type="submit"
          style={{
            padding: "10px 30px",
            border: "none",
            borderRadius: "5px",
            backgroundColor: "#28a745",
            color: "white",
            fontSize: "16px",
            cursor: "pointer",
            transition: "background-color 0.3s"
          }}
          onMouseOver={e => e.target.style.backgroundColor = "#218838"}
          onMouseOut={e => e.target.style.backgroundColor = "#28a745"}
        >
          Predict
        </button>
      </form>

      {results.length > 0 && (
        <>
          <h2 style={{ marginBottom: "15px" }}>Prediction Results</h2>
          <div style={{ maxHeight: "300px", overflowY: "auto", marginBottom: "30px" }}>
            <table style={{ margin: "0 auto", borderCollapse: "collapse", width: "100%", backgroundColor: "#fff", borderRadius: "5px", overflow: "hidden" }}>
              <thead style={{ backgroundColor: "#007BFF", color: "#fff" }}>
                <tr>
                  <th style={{ padding: "10px" }}>Transaction</th>
                  <th style={{ padding: "10px" }}>Prediction</th>
                  <th style={{ padding: "10px" }}>Probability (Fraud)</th>
                </tr>
              </thead>
              <tbody>
                {results.map((res, idx) => (
                  <tr key={idx} style={{ backgroundColor: idx % 2 === 0 ? "#f1f1f1" : "#fff" }}>
                    <td style={{ padding: "8px" }}>{idx + 1}</td>
                    <td style={{ padding: "8px" }}>{res.prediction}</td>
                    <td style={{ padding: "8px" }}>
                      {res.probabilities && res.probabilities[1] ? res.probabilities[1].toFixed(4) : "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h2 style={{ marginBottom: "15px" }}>Fraud vs Non-Fraud Chart</h2>
          <BarChart width={500} height={300} data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#007BFF" />
          </BarChart>

     



// Example: polling backend endpoint /stream-fraud every 2 seconds
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
