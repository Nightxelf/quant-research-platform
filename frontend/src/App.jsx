import { useState } from 'react';

function App() {
  const [tickers, setTickers] = useState(['AAPL', 'MSFT']);
  const [startDate, setStartDate] = useState('2023-01-01');
  const [endDate, setEndDate] = useState('2024-01-01');
  const [factorName, setFactorName] = useState('low_volatility');
  const [optimizationMethod, setOptimizationMethod] = useState('equal_weight');
  const [metrics, setMetrics] = useState(null);
  const [weights, setWeights] = useState(null);
  const [equityCurve, setEquityCurve] = useState([]);
  const [drawdown, setDrawdown] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const runAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const selectedTickers = tickers.length ? tickers : ['AAPL'];
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tickers: selectedTickers,
          start_date: startDate,
          end_date: endDate,
          factor_name: factorName,
          optimization_method: optimizationMethod
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Analysis failed');
      setMetrics(data.metrics);
      setWeights(data.weights);
      setEquityCurve(Object.entries(data.equity_curve || {}).map(([date, value]) => ({ date, value: Number(value) })));
      setDrawdown(Object.entries(data.drawdown || {}).map(([date, value]) => ({ date, value: Number(value) })));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const exportResults = async () => {
    const selectedTickers = tickers.length ? tickers : ['AAPL'];
    const response = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tickers: selectedTickers,
        start_date: startDate,
        end_date: endDate,
        factor_name: factorName,
        optimization_method: optimizationMethod
      })
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'quant_analysis.csv';
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const renderChart = (series, color, label) => {
    if (!series.length) return null;
    const width = 420;
    const height = 220;
    const values = series.map((item) => Number(item.value));
    const max = Math.max(...values);
    const min = Math.min(...values);
    const points = values.map((value, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * width;
      const y = height - ((value - min) / Math.max(max - min, 1e-6)) * height;
      return `${x},${y}`;
    }).join(' ');
    const lastValue = values[values.length - 1] ?? 0;
    return (
      <div className="chart-card">
        <svg viewBox={`0 0 ${width} ${height}`} className="chart">
          <line x1="0" y1={height} x2={width} y2={height} className="chart-axis" />
          <line x1="0" y1="0" x2="0" y2={height} className="chart-axis" />
          <polyline fill="none" stroke={color} strokeWidth="3" points={points} />
        </svg>
        <div className="chart-caption">
          <span>{label}</span>
          <strong>{Number(lastValue).toFixed(4)}</strong>
        </div>
      </div>
    );
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <span className="eyebrow">Quant Research Studio</span>
          <h1>Monitor factor strategies with a polished research workspace.</h1>
          <p>Choose assets, compare optimization styles, and review risk-adjusted results in seconds.</p>
        </div>

        <label>
          Tickers
          <select
            multiple
            size="5"
            value={tickers}
            onChange={(e) => setTickers(Array.from(e.target.selectedOptions, (option) => option.value))}
          >
            <option value="AAPL">AAPL</option>
            <option value="MSFT">MSFT</option>
            <option value="NVDA">NVDA</option>
            <option value="GOOGL">GOOGL</option>
            <option value="AMZN">AMZN</option>
            <option value="TSLA">TSLA</option>
            <option value="META">META</option>
            <option value="JPM">JPM</option>
          </select>
        </label>
        <label>
          Start date
          <input value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </label>
        <label>
          End date
          <input value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </label>
        <label>
          Factor
          <select value={factorName} onChange={(e) => setFactorName(e.target.value)}>
            <option value="low_volatility">Low volatility</option>
            <option value="momentum">Momentum</option>
            <option value="value">Value</option>
          </select>
        </label>
        <label>
          Optimization
          <select value={optimizationMethod} onChange={(e) => setOptimizationMethod(e.target.value)}>
            <option value="equal_weight">Equal weight</option>
            <option value="mean_variance">Mean variance</option>
          </select>
        </label>

        <div className="button-group">
          <button onClick={runAnalysis} disabled={loading}>
            {loading ? 'Analyzing…' : 'Run analysis'}
          </button>
          <button onClick={exportResults} className="secondary-button">
            Export CSV
          </button>
        </div>
        {error ? <p className="error">{error}</p> : null}
      </aside>

      <main className="content">
        <section className="hero-card">
          <div>
            <p className="eyebrow">Live research snapshot</p>
            <h2>Factor-driven portfolio insights</h2>
            <p>Review performance, allocation weights, and drawdown behavior without leaving the dashboard.</p>
          </div>
          <div className="hero-pill">{tickers.join(', ') || 'AAPL'}</div>
        </section>

        <section className="card">
          <h2>Performance metrics</h2>
          {metrics ? (
            <div className="metric-grid">
              {Object.entries(metrics).map(([key, value]) => (
                <div key={key} className="metric-pill">
                  <span>{key}</span>
                  <strong>{Number(value).toFixed(4)}</strong>
                </div>
              ))}
            </div>
          ) : (
            <p>Run an analysis to see the metrics.</p>
          )}
        </section>

        <section className="card">
          <h2>Portfolio weights</h2>
          {weights ? (
            <div className="metric-grid">
              {Object.entries(weights).map(([key, value]) => (
                <div key={key} className="metric-pill">
                  <span>{key}</span>
                  <strong>{Number(value).toFixed(4)}</strong>
                </div>
              ))}
            </div>
          ) : (
            <p>Weights appear here after analysis.</p>
          )}
        </section>

        <section className="card">
          <h2>Equity curve</h2>
          {equityCurve.length ? renderChart(equityCurve, '#4ade80', 'Equity curve') : <p>No equity curve yet.</p>}
        </section>

        <section className="card">
          <h2>Drawdown</h2>
          {drawdown.length ? renderChart(drawdown, '#f87171', 'Drawdown') : <p>No drawdown data yet.</p>}
        </section>
      </main>
    </div>
  );
}

export default App;
