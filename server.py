from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import uvicorn

from quant_research_platform.analytics import calculate_metrics, optimize_portfolio, run_backtest
from quant_research_platform.data import download_stock_data

app = FastAPI(title="Quant Research Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze")
def analyze(payload: dict):
    tickers = payload.get("tickers", [])
    start_date = payload.get("start_date", "2023-01-01")
    end_date = payload.get("end_date", "2024-01-01")
    factor_name = payload.get("factor_name", "low_volatility")
    optimization_method = payload.get("optimization_method", "equal_weight")

    prices = download_stock_data(tickers, start_date, end_date)
    returns = prices.pct_change().dropna()

    first_series = returns.iloc[:, 0] if not returns.empty else pd.Series(dtype=float)
    metrics = calculate_metrics(first_series, risk_free_rate=0.0)
    weights = optimize_portfolio(returns, method=optimization_method)
    backtest = run_backtest(prices, factor_name=factor_name, rebalance=2, transaction_cost=0.001, weights=weights)

    return {
        "metrics": metrics,
        "weights": weights,
        "factor_name": factor_name,
        "equity_curve": backtest["equity_curve"].to_dict(),
        "drawdown": backtest["drawdown"].to_dict(),
    }


@app.post("/api/export")
def export_results(payload: dict):
    tickers = payload.get("tickers", [])
    start_date = payload.get("start_date", "2023-01-01")
    end_date = payload.get("end_date", "2024-01-01")
    factor_name = payload.get("factor_name", "low_volatility")
    optimization_method = payload.get("optimization_method", "equal_weight")

    prices = download_stock_data(tickers, start_date, end_date)
    returns = prices.pct_change().dropna()

    metrics = calculate_metrics(returns.iloc[:, 0] if not returns.empty else pd.Series(dtype=float), risk_free_rate=0.0)
    weights = optimize_portfolio(returns, method=optimization_method)
    backtest = run_backtest(prices, factor_name=factor_name, rebalance=2, transaction_cost=0.001, weights=weights)

    export_frame = pd.DataFrame({
        "metric": list(metrics.keys()),
        "value": list(metrics.values()),
    })
    export_frame = pd.concat([export_frame, pd.DataFrame([{"metric": "factor_name", "value": factor_name}])], ignore_index=True)
    export_frame = pd.concat([export_frame, pd.DataFrame([{"metric": "optimization_method", "value": optimization_method}])], ignore_index=True)
    export_frame = pd.concat([export_frame, pd.DataFrame([{"metric": "weights", "value": str(weights)}])], ignore_index=True)

    buffer = io.StringIO()
    export_frame.to_csv(buffer, index=False)
    response = StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=quant_analysis.csv"
    return response
