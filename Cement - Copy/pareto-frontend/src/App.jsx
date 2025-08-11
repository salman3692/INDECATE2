import React, { useState } from 'react';
import ParetoChart from './ParetoChart';

const App = () => {
  const [inputs, setInputs] = useState({
    cEE: "0.05",
    cH2: "0.075",
    cNG: "0.055",
    cbioCH4: "0.07",
    cbiomass: "0.04",
    cCoal: "0.04",
    cMSW: "0.04",
    cCO2: "0.150",
    cCO2TnS: "0.050",
  });

  const [emissionScenario, setEmissionScenario] = useState("RE1");
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

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

  const handleScenarioChange = (e) => {
    setEmissionScenario(e.target.value);
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

    payload["emission_scenario"] = emissionScenario;

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

  return (
    <div style={{ padding: "30px 50px", fontFamily: "Segoe UI, sans-serif", background: "#f9f9f9" }}>
      <h1 style={{ fontWeight: 500, marginBottom: "20px" }}>Cement Decarbonization: Pareto Visualizer</h1>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        <div style={{ flex: 1, minWidth: "250px" }}>
          <h3>Energy Prices (€/kWh, €/kg, €/ton)</h3>
          {Object.keys(inputs).map((key) => (
            <div key={key} style={{ marginBottom: "10px" }}>
              <label>
                {key} ({minMaxValues[key].min}–{minMaxValues[key].max}):{" "}
                <input
                  type="number"
                  step="0.001"
                  name={key}
                  value={inputs[key]}
                  onChange={handleInputChange}
                  style={{
                    width: "100px",
                    marginLeft: "10px",
                    padding: "4px 8px",
                    borderRadius: "4px",
                    border: "1px solid #ccc",
                  }}
                />
              </label>
            </div>
          ))}

          <div style={{ marginTop: "15px", marginBottom: "10px" }}>
            <label>
              Emission Scenario:{" "}
              <select
                value={emissionScenario}
                onChange={handleScenarioChange}
                style={{ padding: "6px", borderRadius: "4px", border: "1px solid #ccc" }}
              >
                <option value="fossil">Fossil-dominant</option>
                <option value="RE1">Renewable Mix 1 (RE1)</option>
                <option value="RE2">Renewable Mix 2 (RE2)</option>
              </select>
            </label>
          </div>

          <button
            onClick={handleSubmit}
            style={{
              marginTop: "10px",
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Generate
          </button>

          {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
        </div>

        <div style={{ flex: 2, minWidth: "600px" }}>
          <ParetoChart results={results} emissionScenario={emissionScenario} />
        </div>
      </div>
    </div>
  );
};

export default App;
