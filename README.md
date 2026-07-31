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

<img width="1898" height="935" alt="Screenshot 2026-07-31 053958" src="https://github.com/user-attachments/assets/d946c8b1-a1e6-4e91-879d-85cf85e8a3d6" />


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
