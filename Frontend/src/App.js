import React from "react";

function App() {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1>Fraud Shield</h1>
      <p>Protecting users with intelligent fraud detection.</p>
      <button 
        style={{
          padding: "10px 20px",
          border: "none",
          borderRadius: "5px",
          backgroundColor: "#007BFF",
          color: "white",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Get Started
      </button>
    </div>
  );
}

export default App;
