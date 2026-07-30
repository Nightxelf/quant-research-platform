from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def calculate_metrics(returns: pd.Series, risk_free_rate: float = 0.0) -> dict[str, float]:
    """Calculate common performance and risk metrics."""
    if returns.empty:
        return {
            "cagr": 0.0,
            "sharpe": 0.0,
            "sortino": 0.0,
            "max_drawdown": 0.0,
            "beta": 0.0,
            "alpha": 0.0,
            "information_ratio": 0.0,
            "var_95": 0.0,
            "cvar_95": 0.0,
        }

    cumulative = (1 + returns).cumprod()
    cagr = cumulative.iloc[-1] ** (1 / len(returns)) - 1

    excess_returns = returns - risk_free_rate
    sharpe = excess_returns.mean() / excess_returns.std(ddof=0) if excess_returns.std(ddof=0) != 0 else 0.0
    downside = excess_returns.where(excess_returns < 0, 0)
    sortino = downside.mean() / downside.std(ddof=0) if downside.std(ddof=0) != 0 else 0.0

    running_max = cumulative.cummax()
    drawdowns = (cumulative / running_max) - 1
    max_drawdown = max(drawdowns.min(), 0.0)

    beta = 0.0
    alpha = 0.0
    information_ratio = 0.0
    var_95 = float(np.percentile(returns, 5))
    cvar_95 = float(returns[returns <= var_95].mean()) if (returns <= var_95).any() else 0.0

    return {
        "cagr": float(cagr),
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "max_drawdown": float(max_drawdown),
        "beta": float(beta),
        "alpha": float(alpha),
        "information_ratio": float(information_ratio),
        "var_95": var_95,
        "cvar_95": cvar_95,
    }


def create_factor_scores(prices: pd.DataFrame, factor_name: str = "low_volatility") -> pd.DataFrame:
    """Create a simple factor score matrix for each asset over time."""
    if prices.empty:
        return pd.DataFrame()

    returns = prices.pct_change()
    if returns.empty:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)

    if factor_name == "low_volatility":
        rolling_vol = returns.rolling(window=min(3, len(returns)), min_periods=1).std().fillna(0.0)
        scores = 1 / (rolling_vol + 1e-8)
    elif factor_name == "momentum":
        scores = returns.rolling(window=min(3, len(returns)), min_periods=1).mean().fillna(0.0)
    elif factor_name == "value":
        scores = prices.rank(axis=1, ascending=True).astype(float)
    else:
        scores = pd.DataFrame(1.0, index=returns.index, columns=returns.columns)

    ranked = scores.rank(axis=1, ascending=False, method="first")
    return ranked.fillna(0.0)


def optimize_portfolio(returns: pd.DataFrame, method: str = "equal_weight") -> dict[str, float]:
    """Generate portfolio allocations using equal-weight or mean-variance methods."""
    if returns.empty:
        return {}

    if method == "mean_variance":
        cov = returns.cov().to_numpy()
        mean_returns = returns.mean().to_numpy()
        n = len(mean_returns)

        def objective(weights: np.ndarray) -> float:
            portfolio_vol = np.sqrt(weights @ cov @ weights)
            return portfolio_vol

        constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0})
        bounds = [(0.0, 1.0)] * n
        initial = np.full(n, 1.0 / n)
        result = minimize(objective, initial, method="SLSQP", bounds=bounds, constraints=[constraints])
        weights = result.x if result.success else initial
    else:
        n = returns.shape[1]
        weights = np.full(n, 1.0 / n)

    return {col: float(weight) for col, weight in zip(returns.columns, weights)}


def run_backtest(
    prices: pd.DataFrame,
    factor_name: str = "low_volatility",
    lookback: int = 2,
    rebalance: int = 2,
    transaction_cost: float = 0.001,
    weights: dict[str, float] | None = None,
) -> dict[str, pd.Series | pd.DataFrame]:
    """Run a simple backtest using either supplied weights or equal-weight portfolios."""
    if prices.empty:
        return {"portfolio_returns": pd.Series(dtype=float), "equity_curve": pd.Series(dtype=float), "drawdown": pd.Series(dtype=float)}

    returns = prices.pct_change().dropna()
    if returns.empty:
        return {"portfolio_returns": pd.Series(dtype=float), "equity_curve": pd.Series(dtype=float), "drawdown": pd.Series(dtype=float)}

    if weights is None:
        base_weights = {col: 1.0 / len(returns.columns) for col in returns.columns}
    else:
        base_weights = {col: float(weights.get(col, 0.0)) for col in returns.columns}
        total = sum(base_weights.values())
        if total > 0:
            base_weights = {col: value / total for col, value in base_weights.items()}

    portfolio_returns = []
    prev_weights = None
    for idx in range(len(returns)):
        if idx % rebalance == 0:
            current_weights = pd.Series(base_weights, index=returns.columns)
            if prev_weights is not None:
                turnover = abs(current_weights - prev_weights).sum() / 2.0
                cost = transaction_cost * turnover
            else:
                cost = 0.0
            prev_weights = current_weights
        else:
            cost = 0.0
            current_weights = prev_weights if prev_weights is not None else pd.Series(base_weights, index=returns.columns)

        daily_return = (returns.iloc[idx] * current_weights).sum() - cost
        portfolio_returns.append(daily_return)

    portfolio_series = pd.Series(portfolio_returns, index=returns.index)
    equity_curve = (1 + portfolio_series).cumprod()
    drawdown = 1 - equity_curve / equity_curve.cummax()
    return {
        "portfolio_returns": portfolio_series,
        "equity_curve": equity_curve,
        "drawdown": drawdown,
    }
