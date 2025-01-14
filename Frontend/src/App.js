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
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", margin: "50px auto", maxWidth: "800px" }}>
      <h1 style={{ color: "#007BFF" }}>🚀 Fraud Shield</h1>
      <p>Enter transaction features below and get fraud predictions:</p>
      <form
        onSubmit={e => { e.preventDefault(); handlePredict(); }}
        style={{ marginBottom: "20px" }}
      >
        {features.map((f, i) => (
          <input
            key={i}
            type="number"
            placeholder={`Feature ${i + 1}`}
            value={features[i]}
            onChange={e => handleChange(i, e.target.value)}
            style={{ margin: "5px", width: "90px", padding: "5px", borderRadius: "4px", border: "1px solid #ccc" }}
          />
        ))}
        <br />
        <button
          type="submit"
          style={{
            padding: "10px 25px",
            border: "none",
            borderRadius: "5px",
            backgroundColor: "#28a745",
            color: "white",
            fontSize: "16px",
            cursor: "pointer",
            marginTop: "10px"
          }}
        >
          Predict
        </button>
      </form>

      {results.length > 0 && (
        <>
          <h2>Prediction Results</h2>
          <table style={{ margin: "20px auto", borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th style={{ border: "1px solid black", padding: "8px" }}>Transaction</th>
                <th style={{ border: "1px solid black", padding: "8px" }}>Prediction</th>
                <th style={{ border: "1px solid black", padding: "8px" }}>Probability (Fraud)</th>
              </tr>
            </thead>
            <tbody>
              {results.map((res, idx) => (
                <tr key={idx}>
                  <td style={{ border: "1px solid black", padding: "8px" }}>{idx + 1}</td>
                  <td style={{ border: "1px solid black", padding: "8px" }}>{res.prediction}</td>
                  <td style={{ border: "1px solid black", padding: "8px" }}>
                    {res.probabilities && res.probabilities[1] ? res.probabilities[1].toFixed(4) : "N/A"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Fraud vs Non-Fraud Chart</h2>
          <BarChart width={500} height={300} data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#007BFF" />
          </BarChart>

          <h2>Flagged Transactions</h2>
          {flaggedTransactions.length > 0 ? (
            <ul>
              {flaggedTransactions.map(t => (
                <li key={t.transaction}>
                  Transaction {t.transaction}: Fraud Probability {t.probabilities[1].toFixed(4)}
                </li>
              ))}
            </ul>
          ) : (
            <p>No transactions flagged as fraud.</p>
          )}
        </>
      )}
    </div>
  );
}

export default App;



