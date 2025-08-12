import { useMemo } from 'react';

export default function Controls({
  inputs, setInputs,
  emissionScenario, setEmissionScenario,
  onGenerate, loading, error,
}) {
  const fields = useMemo(() => ({
    cEE: { label: 'Electricity', unit: '€/kWh', min: 0.01, max: 0.175, step: 0.001 },
    cH2: { label: 'Hydrogen', unit: '€/kWh', min: 0.01, max: 0.1, step: 0.001 },
    cNG: { label: 'Nat. Gas', unit: '€/kWh', min: 0.01, max: 0.1, step: 0.001 },
    cbioCH4: { label: 'Bio-CH₄', unit: '€/kWh', min: 0.03, max: 0.09, step: 0.001 },
    cbiomass: { label: 'Biomass', unit: '€/kWh', min: 0.01, max: 0.09, step: 0.001 },
    cCoal: { label: 'Coal', unit: '€/kWh', min: 0.01, max: 0.09, step: 0.001 },
    cMSW: { label: 'MSW', unit: '€/kWh', min: 0.01, max: 0.09, step: 0.001 },
    cCO2: { label: 'CO₂ price', unit: '€/kg', min: 0.075, max: 0.25, step: 0.001 },
    cCO2TnS: { label: 'CO₂ T&S', unit: '€/kg', min: 0.025, max: 0.1, step: 0.001 },
  }), []);

  const handleChange = (k, v) => setInputs(prev => ({ ...prev, [k]: v }));

  return (
    <section className="rounded-2xl bg-white border border-gray-200 shadow-sm p-4">
      {/* Scenario row (centered) */}
      <div className="flex justify-center mb-3">
        <div className="inline-flex rounded-xl border overflow-hidden">
          {['fossil', 'RE1', 'RE2'].map(s => (
            <button
              key={s}
              type="button"
              onClick={() => setEmissionScenario(s)}
              className={`px-4 py-2 text-sm transition ${
                emissionScenario === s
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white hover:bg-neutral-50 text-neutral-700'
              }`}
            >
              {s === 'fossil' ? 'Scenario fossil' : `Scenario ${s}`}
            </button>
          ))}
        </div>
      </div>

      {/* Sliders grid (wide, like your boxes) */}
      <div className="grid gap-3 grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        {Object.entries(fields).map(([key, meta]) => {
          const val = inputs[key];
          return (
            <div key={key} className="rounded-lg border p-3">
              <label className="block text-xs font-medium text-neutral-700 mb-1">
                {meta.label} <span className="text-[10px] text-neutral-500">{meta.unit}</span>
              </label>
              <input
                type="number"
                value={val}
                step={meta.step}
                min={meta.min}
                max={meta.max}
                onChange={e => handleChange(key, e.target.value)}
                className="w-full rounded-md border px-2 py-1 text-[11px] mb-2 focus:outline-none focus:ring-1 focus:ring-indigo-500/40 focus:border-indigo-500"
              />
              <input
                type="range"
                value={val}
                min={meta.min}
                max={meta.max}
                step={meta.step}
                onChange={e => handleChange(key, e.target.value)}
                className="w-full h-1 accent-indigo-600"
              />
            </div>
          );
        })}
      </div>

      {/* Generate button centered */}
      <div className="flex justify-center mt-4">
        <button
          onClick={onGenerate}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-lg border border-indigo-600 bg-indigo-600 px-5 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
        >
          {loading ? 'Generating…' : 'Generate'}
        </button>
      </div>

      {error && (
        <p className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 border border-red-200 text-center">
          {error}
        </p>
      )}
    </section>
  );
}
