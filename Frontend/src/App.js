import React, { useState } from "react";

function App() {
  const [features, setFeatures] = useState(Array(10).fill("")); // Example 10 features
  const [results, setResults] = useState([]); // Array of prediction results

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
        setResults(data); // Save response array
      } else {
        setResults([{ prediction: "Error", probabilities: [] }]);
      }
    } catch (error) {
      console.error(error);
      setResults([{ prediction: "Error", probabilities: [] }]);
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1>🚀 Fraud Shield</h1>
      <p>Enter transaction features to get a fraud prediction:</p>
      <form
        onSubmit={e => {
          e.preventDefault();
          handlePredict();
        }}
      >
        {features.map((f, i) => (
          <input
            key={i}
            type="number"
            placeholder={`Feature ${i + 1}`}
            value={features[i]}
            onChange={e => handleChange(i, e.target.value)}
            style={{ margin: "5px", width: "100px" }}
          />
        ))}
        <br />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            backgroundColor: "#007BFF",
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
        <table
          style={{
            margin: "20px auto",
            borderCollapse: "collapse",
            width: "80%"
          }}
        >
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
      )}
    </div>
  );
}

export default App;
