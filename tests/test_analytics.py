import unittest
import pandas as pd
import numpy as np

from quant_research_platform.analytics import (
    calculate_metrics,
    create_factor_scores,
    optimize_portfolio,
    run_backtest,
)


class AnalyticsTests(unittest.TestCase):
    def test_calculate_metrics_returns_expected_shapes(self):
        returns = pd.Series([0.01, 0.02, -0.01, 0.03, 0.02], index=pd.date_range("2024-01-01", periods=5, freq="D"))
        metrics = calculate_metrics(returns, risk_free_rate=0.01)

        self.assertAlmostEqual(metrics["cagr"], 0.0139, places=4)
        self.assertGreater(metrics["sharpe"], 0.0)
        self.assertGreaterEqual(metrics["max_drawdown"], 0.0)
        self.assertIn("sortino", metrics)
        self.assertIn("var_95", metrics)
        self.assertIn("cvar_95", metrics)

    def test_calculate_metrics_with_benchmark_produces_risk_metrics(self):
        returns = pd.Series([0.05, 0.02, -0.02, 0.03, 0.01], index=pd.date_range("2024-01-01", periods=5, freq="D"))
        benchmark = pd.Series([0.01, 0.01, -0.01, 0.02, 0.00], index=returns.index)

        metrics = calculate_metrics(returns, risk_free_rate=0.0, benchmark_returns=benchmark)

        self.assertTrue(np.isfinite(metrics["beta"]))
        self.assertTrue(np.isfinite(metrics["alpha"]))
        self.assertTrue(np.isfinite(metrics["information_ratio"]))
        self.assertGreater(metrics["beta"], 0.0)
        self.assertGreater(metrics["alpha"], 0.0)
        self.assertGreater(metrics["information_ratio"], 0.0)

    def test_create_factor_scores_uses_ranked_signal(self):
        prices = pd.DataFrame(
            {
                "A": [100, 101, 100, 103],
                "B": [100, 95, 97, 98],
                "C": [100, 110, 108, 112],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        signals = create_factor_scores(prices, factor_name="low_volatility")
        self.assertEqual(signals.shape[0], prices.shape[0])
        self.assertIn("A", signals.columns)

    def test_optimize_portfolio_returns_normalized_weights(self):
        returns = pd.DataFrame(
            {
                "A": [0.01, 0.02, 0.03, 0.01],
                "B": [0.02, 0.03, 0.01, 0.02],
                "C": [0.00, 0.01, 0.02, 0.03],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        weights = optimize_portfolio(returns)
        self.assertEqual(len(weights), returns.shape[1])
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=6)
        self.assertTrue(all(w >= 0 for w in weights.values()))

    def test_mean_variance_optimizer_returns_normalized_weights(self):
        returns = pd.DataFrame(
            {
                "A": [0.02, 0.01, 0.03, 0.04, 0.02],
                "B": [0.01, 0.03, 0.01, 0.02, 0.03],
                "C": [0.00, 0.02, 0.01, 0.03, 0.01],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        weights = optimize_portfolio(returns, method="mean_variance")
        self.assertEqual(len(weights), returns.shape[1])
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=6)
        self.assertTrue(all(w >= 0 for w in weights.values()))

    def test_run_backtest_produces_portfolio_series(self):
        prices = pd.DataFrame(
            {
                "A": [100, 102, 101, 104],
                "B": [100, 98, 99, 100],
                "C": [100, 101, 103, 102],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        result = run_backtest(prices, factor_name="low_volatility", lookback=2, rebalance=2, transaction_cost=0.001)
        self.assertIn("portfolio_returns", result)
        self.assertGreaterEqual(result["portfolio_returns"].shape[0], 1)

    def test_run_backtest_uses_supplied_weights(self):
        prices = pd.DataFrame(
            {
                "A": [100, 102, 103, 104],
                "B": [100, 98, 97, 96],
                "C": [100, 101, 102, 103],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        result = run_backtest(
            prices,
            factor_name="momentum",
            rebalance=1,
            transaction_cost=0.0,
            weights={"A": 0.1, "B": 0.2, "C": 0.7},
        )

        self.assertIn("equity_curve", result)
        self.assertGreaterEqual(result["equity_curve"].shape[0], 1)
        self.assertTrue(np.isfinite(result["equity_curve"].iloc[-1]))
        self.assertTrue(np.isfinite(result["drawdown"].iloc[-1]))
        self.assertGreaterEqual(result["drawdown"].min(), 0.0)

    def test_run_backtest_calculates_positive_drawdown(self):
        prices = pd.DataFrame(
            {
                "A": [100, 110, 105, 108],
                "B": [100, 100, 100, 100],
                "C": [100, 100, 100, 100],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        result = run_backtest(prices, rebalance=1, transaction_cost=0.0)
        self.assertGreater(result["drawdown"].max(), 0.0)
        self.assertEqual(result["drawdown"].iloc[0], 0.0)

    def test_calculate_metrics_max_drawdown(self):
        returns = pd.Series([0.1, -0.2, 0.05], index=pd.date_range("2024-01-01", periods=3, freq="D"))
        metrics = calculate_metrics(returns)

        self.assertAlmostEqual(metrics["max_drawdown"], 0.2, places=6)


if __name__ == "__main__":
    unittest.main()
