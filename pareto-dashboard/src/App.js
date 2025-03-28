import React from 'react';
import ParetoPlot from './ParetoPlot'; // or './pareto_plot' if file isn't renamed

function App() {
  return (
    <div className="App">
      <ParetoPlot />  {/* PascalCase component call */}
    </div>
  );
}

export default App;
