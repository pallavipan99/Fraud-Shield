import React, { useState } from "react";

function App() {
  const [prediction, setPrediction] = useState(null);

  // Example feature array for a single transaction
  const exampleFeatures = [0.1, -1.2, 0.5, 0.3, -0.4, 0.2, 1.1, -0.5, 0.0, 0.7]; // Adjust length to match dataset

  const handlePredict = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: [exampleFeatures] }),
      });

      const data = await response.json();
      if (Array.isArray(data) && data.length > 0) {
        setPrediction(data[0].prediction);
      } else {
        setPrediction("Error: Invalid response from API");
      }
    } catch (error) {
      console.error(error);
      setPrediction("Error calling API");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1>🚀 Fraud Shield</h1>
      <p>Protecting users with intelligent fraud detection.</p>
      <button
        style={{
          padding: "10px 20px",
          border: "none",
          borderRadius: "5px",
          backgroundColor: "#007BFF",
          color: "white",
          fontSize: "16px",
          cursor: "pointer",
        }}
        onClick={handlePredict}
      >
        Get Prediction
      </button>
      {prediction !== null && <h2>Prediction: {prediction}</h2>}
    </div>
  );
}

export default App;

