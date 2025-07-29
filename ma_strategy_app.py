# filename: ma_strategy_app.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Page layout
st.set_page_config(layout="wide")
st.title("📈 Moving Average Crossover Strategy")

# User Inputs
ticker = st.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2023-01-01"))

# Fetch Data
data = yf.download(ticker, start=start_date, end=end_date)
if data.empty:
    st.warning("No data found. Try a different symbol or date.")
    st.stop()

# Calculate Moving Averages
data["SMA20"] = data["Close"].rolling(window=20).mean()
data["SMA50"] = data["Close"].rolling(window=50).mean()

# Generate Buy/Sell Signals
data["Signal"] = 0
data.loc[data["SMA20"] > data["SMA50"], "Signal"] = 1
data.loc[data["SMA20"] < data["SMA50"], "Signal"] = -1

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data["Close"], label="Close Price", alpha=0.5)
ax.plot(data["SMA20"], label="SMA 20", linestyle="--")
ax.plot(data["SMA50"], label="SMA 50", linestyle="--")

# Buy/Sell Markers
buy_signals = data[data["Signal"] == 1]
sell_signals = data[data["Signal"] == -1]
ax.scatter(buy_signals.index, buy_signals["Close"], label="Buy", marker="^", color="green")
ax.scatter(sell_signals.index, sell_signals["Close"], label="Sell", marker="v", color="red")

ax.set_title(f"{ticker} - MA Crossover Strategy")
ax.legend()
st.pyplot(fig)
