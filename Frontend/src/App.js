import React, { useState } from "react";

function App() {
  const [features, setFeatures] = useState(Array(10).fill("")); // Example 10 features
  const [prediction, setPrediction] = useState(null);

  const handleChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  const handlePredict = async () => {
    try {
      // Convert string inputs to numbers
      const numericFeatures = features.map(f => parseFloat(f));
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: [numericFeatures] }),
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
      {prediction !== null && <h2>Prediction: {prediction}</h2>}
    </div>
  );
}

export default App;


