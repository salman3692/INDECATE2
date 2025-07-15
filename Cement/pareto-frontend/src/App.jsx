import React, { useState } from "react";
import Plot from "react-plotly.js";

const App = () => {
  const [inputs, setInputs] = useState({
    cEE: "",
    cH2: "",
    cNG: "",
    cbioCH4: "",
    cbiomass: "",
    cCoal: "",
    cMSW: "",
    cCO2: "",
    cCO2TnS: "",
  });

  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  // ✅ New: Allowed min/max ranges
  const minMaxValues = {
    cEE: { min: 0.01, max: 0.175 },
    cH2: { min: 0.01, max: 0.1 },
    cNG: { min: 0.01, max: 0.1 },
    cbioCH4: { min: 0.03, max: 0.09 },
    cbiomass: { min: 0.01, max: 0.09 },
    cCoal: { min: 0.01, max: 0.09 },
    cMSW: { min: 0.01, max: 0.09 },
    cCO2: { min: 0.075, max: 0.25 },
    cCO2TnS: { min: 0.025, max: 0.1 },
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    setError("");

    const payload = {};
    for (const key in inputs) {
      const val = parseFloat(inputs[key]);
      if (isNaN(val)) {
        setError(`Invalid input for ${key}`);
        return;
      }

      const { min, max } = minMaxValues[key];
      if (val < min || val > max) {
        setError(`Value for ${key} must be between ${min} and ${max}`);
        return;
      }

      payload[key] = val;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      setError("Failed to fetch prediction.");
    }
  };

  const renderPlot = () => {
    if (!results) return null;

    const configs = Object.keys(results);
    const costs = [];
    const emissions = [];
    const labels = [];

    for (const config of configs) {
      const point = results[config];
      if (
        typeof point.cost === "number" &&
        typeof point.emissions === "number" &&
        !isNaN(point.cost) &&
        !isNaN(point.emissions)
      ) {
        labels.push(config);
        costs.push(point.cost);
        emissions.push(point.emissions);
      }
    }

    return (
      <Plot
        data={[
          {
            x: costs,
            y: emissions,
            text: labels,
            type: "scatter",
            mode: "markers+text",
            marker: { size: 10 },
            textposition: "top center",
          },
        ]}
        layout={{
          title: "Pareto Front (Emissions vs Cost)",
          xaxis: { title: "Total Cost (€/ton)", autorange: true },
          yaxis: { title: "Emissions (tCO₂/ton)", range: [-0.2, 1.0] },
          width: 1000, // You can adjust here
          height: 600,
          margin: { t: 60, l: 80, r: 60, b: 60 },
        }}
        style={{ width: "1000px", height: "600px" }}
        config={{ responsive: true }}
      />
    );
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Energy Prices Input (€/kWh or €/kg or €/ton)</h2>
      {Object.keys(inputs).map((key) => (
        <div key={key} style={{ marginBottom: "8px" }}>
          <label>
            {key} (range: {minMaxValues[key].min}–{minMaxValues[key].max}):{" "}
            <input
              type="number"
              step="0.001"
              name={key}
              value={inputs[key]}
              onChange={handleInputChange}
              style={{ width: "100px" }}
            />
          </label>
        </div>
      ))}
      <button onClick={handleSubmit} style={{ marginTop: "10px", padding: "8px 16px" }}>
        Generate
      </button>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      <div style={{ marginTop: "30px" }}>{renderPlot()}</div>
    </div>
  );
};

export default App;
