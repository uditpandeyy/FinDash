# 📊 Fintech Strategy Backtester Dashboard

A clean, interactive web application to **backtest Moving Average Crossover strategies** with built-in **RSI, MACD, and Bollinger Bands** visualization — built using **Streamlit**, **Python**, and **yFinance**.

![App Title](./screenshots/App%20title%20and%20inputs.png)

---

## 🚀 Project Overview

This tool helps visualize and test basic technical analysis strategies on real market data (via Yahoo Finance). It supports:

- ✅ Customizable MA crossover strategy
- 📈 RSI & MACD overlays
- 📉 Bollinger Bands for volatility
- 📊 Performance and risk metrics
- 🧾 Auto-generated trade logs
- 📥 CSV export of trades

---

## 📌 Features

### 📥 Custom Stock + Timeframe Input

Users can specify:
- Ticker symbol (e.g., AAPL, TSLA)
- Start and end dates
- Custom SMA lengths for short and long windows

![Input Graph](./screenshots/Input%20graph.png)

---

### 📈 Visual Strategy Summary

The dashboard shows:
- Close price with overlayed SMAs
- Buy/Sell signals based on crossover logic
- RSI zone markers (30/70)
- MACD and Signal Line
- Bollinger Bands (Upper, Middle, Lower)

![Strategy Summary](./screenshots/Strategy%20summary%20and%20RSI.png)

---

### 📊 Metrics & Comparison

Key metrics to evaluate strategy performance:
- Strategy vs. Buy-and-Hold Returns
- Sharpe Ratio & Max Drawdown
- Number of trades executed

![Metrics](./screenshots/Metrics.png)

---

### 📑 Trade Log + CSV Download

Complete record of all Buy/Sell actions, shown in a table and exportable as CSV.

![Trade Log](./screenshots/Trade%20Log.png)

---

### 🔄 Cumulative Returns Comparison

Line plot comparing cumulative returns of the strategy vs. simple buy-and-hold.

![Cumulative Returns](./screenshots/Cumulative%20Returns%20Comparison.png)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (for frontend UI)
- **Pandas, NumPy, Matplotlib**
- **yFinance** (for stock data)
- **TA-Lib / `ta`** (for RSI, MACD, BBands)

---
