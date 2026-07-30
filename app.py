from __future__ import annotations

import streamlit as st
import pandas as pd

from quant_research_platform.analytics import calculate_metrics, create_factor_scores, optimize_portfolio, run_backtest
from quant_research_platform.data import download_stock_data


st.set_page_config(page_title="Quant Research Platform", page_icon="📈", layout="wide")

st.title("Quant Research Platform")
st.write("Download market data, build factors, run backtests, and examine performance metrics.")

with st.sidebar:
    st.header("Inputs")
    tickers_input = st.text_input("Tickers", value="AAPL,MSFT,GOOG")
    start_date = st.text_input("Start date", value="2023-01-01")
    end_date = st.text_input("End date", value="2024-01-01")
    factor_name = st.selectbox("Factor", ["low_volatility", "momentum"])
    run_button = st.button("Run analysis")

if run_button:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
    if not tickers:
        st.error("Please enter at least one ticker.")
        st.stop()

    with st.spinner("Downloading data..."):
        prices = download_stock_data(tickers, start_date, end_date)

    st.subheader("Price data")
    st.dataframe(prices.head())

    returns = prices.pct_change().dropna()
    metrics = calculate_metrics(returns.iloc[:, 0], risk_free_rate=0.0)
    st.subheader("Performance metrics")
    st.json(metrics)

    st.subheader("Factor scores")
    factor_scores = create_factor_scores(prices, factor_name=factor_name)
    st.dataframe(factor_scores)

    st.subheader("Portfolio weights")
    weights = optimize_portfolio(returns)
    st.json(weights)

    st.subheader("Backtest")
    backtest = run_backtest(prices, factor_name=factor_name)
    st.line_chart(backtest["portfolio_returns"])
