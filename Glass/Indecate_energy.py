<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Stacked Bar Chart with Conditional CC & Axis Titles</title>
    <!-- Using a recent version of Plotly -->
    <script src="https://cdn.plot.ly/plotly-2.18.2.min.js"></script>
    <style>
      .toggle-button {
        padding: 8px 16px;
        margin: 4px;
        border: none;
        background-color: #3498db;
        color: #fff;
        cursor: pointer;
        border-radius: 4px;
      }
      .toggle-button.active {
        background-color: #2c3e50;
      }
      body {
        font-family: "Familjen Grotesk", sans-serif;
      }
    </style>
  </head>
  <body>
    <div id="chart" style="width:80%; height:500px; margin:auto;"></div>
    
    <!-- Toggle button for CC -->
    <div style="text-align:center; margin-top:20px;">
      <button class="toggle-button" id="toggleCCButton" onclick="toggleCC()">Toggle Carbon Capture</button>
    </div>

    <script>
      // X-axis categories
      const configurations = ["NGfur", "NGOxyfur", "Hybfur", "ELfur", "H2fur"];

      // (1) Base data for the 6 processes (Q-Process, EL-Process, Q-CCS, EL-CCS, EL-CPU, EL-ASU)
      const baseData = {
        "NGfur":    [5.34, 0.80, 0, 0, 0, 0],
        "NGOxyfur": [4.23, 0.80, 0, 0, 0, 0.29],
        "Hybfur":   [1.92, 2.03, 0, 0, 0, 0.13],
        "ELfur":    [0,    4.19, 0, 0, 0, 0],
        "H2fur":    [5.59, 0.80, 0, 0, 0, 0]
      };

      // Additional data
      // Heat Recovered
      const heatRecoveredNonCC = [0, 0, 0, 0, 0];
      const heatRecoveredCC    = [-0.65, 0, 0, 0, -0.51];

      // Power Generated
      const powerGeneratedNonCC = [-0.22, -0.23, -0.15, 0, -0.23];
      const powerGeneratedCC    = [0, -0.23, -0.15, 0, 0];

      // Emissions
      const emissionsNonCC = [0.61, 0.54, 0.41, 0.36, 0.31];
      const emissionsCC    = [0.22, 0.14, 0.14, 0.18, 0.15];

      // Extra CC traces (with assigned colors)
      const extraQCCS  = { 
        x: configurations, 
        y: [1.44, 0, 0, 0, 0.51],
        name: "Q-CCS (CC)",
        type: 'bar',
        marker: { color: '#228B22 ' }
      };
      const extraELCCS = {
        x: configurations,
        y: [0.27, 0, 0, 0, 0.09],
        name: "EL-CCS (CC)",
        type: 'bar',
        marker: { color: '#ff9896' }
      };
      const extraELCPU = {
        x: configurations,
        y: [0, 0.51, 0.35, 0.23, 0],
        name: "EL-CPU (CC)",
        type: 'bar',
        marker: { color: '#7f7f7f' }
      };

      let ccToggled = false;

      // Build base traces for the 6 processes, with custom colors
      function buildBaseTraces(dataObj) {
        // The 6 processes in order:
        const processNames = [
          "Q-Process",  // index 0
          "EL-Process", // index 1
          "Q-CCS",      // index 2
          "EL-CCS",     // index 3
          "EL-CPU",     // index 4
          "EL-ASU"      // index 5
        ];

        // We'll hide the legend for Q-CCS, EL-CCS, and EL-CPU in base data
        const noLegendProcesses = new Set(["Q-CCS", "EL-CCS", "EL-CPU"]);

        // Distinctive colors for the 6 base processes
        const baseColors = [
          '#1f77b4', // Q-Process (blue)
          '#ff7f0e', // EL-Process (orange)
          '#2ca02c', // Q-CCS (green)
          '#9467bd', // EL-CCS (purple)
          '#8c564b', // EL-CPU (brown)
          '#e377c2'  // EL-ASU (pinkish)
        ];

        const traces = [];
        for (let i = 0; i < 6; i++) {
          const pName = processNames[i];
          const yVals = configurations.map(cfg => dataObj[cfg][i]);

          traces.push({
            x: configurations,
            y: yVals,
            name: pName,
            type: 'bar',
            showlegend: !noLegendProcesses.has(pName), 
            marker: { color: baseColors[i] }
          });
        }
        return traces;
      }

      // Base traces
      const baseTraces = buildBaseTraces(baseData);

      // "Heat Recovered" (red) + "Power Generated" (teal) + "Emissions" (black)
      let heatRecoveredTrace = {
        x: configurations,
        y: heatRecoveredNonCC.slice(),
        name: "Heat Recovered",
        type: 'bar',
        marker: { color: '#d62728' } // red
      };
      let powerGeneratedTrace = {
        x: configurations,
        y: powerGeneratedNonCC.slice(),
        name: "Power Generated",
        type: 'bar',
        marker: { color: '#17becf' } // teal
      };
      let emissionsTrace = {
        x: configurations,
        y: emissionsNonCC.slice(),
        mode: 'markers',
        name: 'Emissions',
        type: 'scatter',
        yaxis: 'y2',
        marker: { color: '#000000', size: 10 } // black
      };

      // Layout
      const layout = {
        title: 'Energy Consumption by Configuration',
        legend: {
          orientation: 'h',
          x: 0.5,
          xanchor: 'center',
          y: 1.05,
          yanchor: 'bottom'
        },
        barmode: 'relative',
        yaxis: {
          zeroline: true,
          title: 'Energy Consumption (GJ/tCO<sub>2</sub>)',
          range: [-1, 8.5],
          showgrid: false
        },
        yaxis2: {
          title: 'Emissions (direct + indirect) (t<sub>CO2</sub>/t<sub>glass</sub>)',
          overlaying: 'y',
          side: 'right',
          range: [-0.1, 0.85],
          showgrid: false
        }
      };

      // Initial data (non-CC)
      let currentData = [
        ...baseTraces,
        heatRecoveredTrace,
        powerGeneratedTrace,
        emissionsTrace
      ];

      // Plot initial chart
      Plotly.newPlot('chart', currentData, layout);

      // Toggle CC function
      function toggleCC() {
        ccToggled = !ccToggled;

        if (ccToggled) {
          // Switch to CC
          heatRecoveredTrace.y = heatRecoveredCC;
          powerGeneratedTrace.y = powerGeneratedCC;
          emissionsTrace.y = emissionsCC;

          currentData = [
            ...baseTraces,
            extraQCCS,
            extraELCCS,
            extraELCPU,
            heatRecoveredTrace,
            powerGeneratedTrace,
            emissionsTrace
          ];
          document.getElementById('toggleCCButton').classList.add('active');
        } else {
          heatRecoveredTrace.y = heatRecoveredNonCC;
          powerGeneratedTrace.y = powerGeneratedNonCC;
          emissionsTrace.y = emissionsNonCC;

          currentData = [
            ...baseTraces,
            heatRecoveredTrace,
            powerGeneratedTrace,
            emissionsTrace
          ];
          document.getElementById('toggleCCButton').classList.remove('active');
        }

        Plotly.react('chart', currentData, layout);
      }
    </script>
  </body>
</html>
