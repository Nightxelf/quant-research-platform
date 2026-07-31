# Quant Research Platform

A polished quant research dashboard built with React and FastAPI for exploring stocks, testing factor ideas, optimizing portfolios, and reviewing performance metrics in one place.
<img width="1897" height="933" alt="Screenshot 2026-07-31 053844" src="https://github.com/user-attachments/assets/3a8923e5-1a72-4f57-a682-102bfdc3afaa" />



## What it does

- Download historical market data for selected stocks with yfinance
- Build factor signals for low volatility, momentum, and value
- Compare equal-weight and mean-variance portfolio optimization
- Run a backtest with transaction-cost handling
- Review performance and risk metrics such as CAGR, Sharpe, Sortino, drawdown, VaR, and CVaR
- Visualize equity curves and drawdowns through a modern React UI
- Export analysis results as CSV
<img width="1896" height="867" alt="Screenshot 2026-07-31 054856" src="https://github.com/user-attachments/assets/5c625b3b-3c4e-4a65-bad3-b8cc75919826" />
<img width="1893" height="917" alt="Screenshot 2026-07-31 054918" src="https://github.com/user-attachments/assets/f7d6adb0-68b9-4df7-9f6d-9c34ceeede9c" />



## Tech stack

- Python
- pandas / NumPy / SciPy
- FastAPI
- React + Vite
- yfinance

## Project structure

```text
quant_research_platform/
  analytics.py
  data.py
frontend/
  src/
server.py
requirements.txt
tests/
```

## Getting started

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
```

### 3. Start the backend

```bash
cd ..
python server.py
```

### 4. Start the frontend

```bash
cd frontend
npm run dev
```

Open the local Vite URL shown in the terminal to use the dashboard.

## Testing

```bash
python -m pytest -q
```
