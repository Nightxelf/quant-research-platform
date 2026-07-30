# Quant Research Platform

A modern quant research starter built with a React frontend and Python analytics backend. It provides a simple workflow for downloading market data, building factor signals, optimizing portfolios, and evaluating strategies.

## Features

- Download historical market data with yfinance
- Create factor signals for low volatility, momentum, and value
- Optimize portfolios with equal-weight and mean-variance methods
- Run a basic backtest with transaction-cost handling
- Compute performance and risk metrics including CAGR, Sharpe, Sortino, drawdown, VaR, and CVaR
- Visualize the workflow through a React dashboard

## Tech Stack

- Python
- pandas / NumPy / SciPy
- FastAPI
- React + Vite
- yfinance

## Project Structure

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

## Getting Started

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd Quant Research Platform
pip install -r requirements.txt
cd frontend
npm install
```

### 2. Start the backend

```bash
cd ..
python server.py
```

### 3. Start the frontend

```bash
cd frontend
npm run dev
```

Open the local Vite URL shown in the terminal to use the dashboard.

## Testing

```bash
pytest -q
```

## Roadmap

Planned enhancements include:

- richer backtesting with slippage and position sizing
- more advanced factor research
- equity curve and drawdown charts
- CSV/Excel export for research results
