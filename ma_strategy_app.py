# filename: ma_strategy_app.py
import ta
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

# User-selected SMA periods
sma_short = st.slider("Short-Term SMA Period", min_value=5, max_value=50, value=20)
sma_long = st.slider("Long-Term SMA Period", min_value=10, max_value=200, value=50)

# Fetch Data
data = yf.download(ticker, start=start_date, end=end_date)
if data.empty:
    st.warning("No data found. Try a different symbol or date.")
    st.stop()

# Calculate Moving Averages
data["SMA_Short"] = data["Close"].rolling(window=sma_short).mean()
data["SMA_Long"] = data["Close"].rolling(window=sma_long).mean()
# Calculate RSI using 'ta' library
rsi_indicator = ta.momentum.RSIIndicator(close=data["Close"].squeeze(), window=14)
data["RSI"] = rsi_indicator.rsi()

# Generate Buy/Sell Signals
data["Signal"] = 0
data.loc[data["SMA_Short"] > data["SMA_Long"], "Signal"] = 1
data.loc[data["SMA_Short"] < data["SMA_Long"], "Signal"] = -1

# Shift signals to simulate trade execution on next day
data["Position"] = data["Signal"].shift(1)

# Calculate daily returns
data["Daily Return"] = data["Close"].pct_change()

# Strategy return: position * daily return
data["Strategy Return"] = data["Position"] * data["Daily Return"]

# Cumulative returns
cumulative_strategy_return = (1 + data["Strategy Return"].fillna(0)).cumprod() - 1
cumulative_stock_return = (1 + data["Daily Return"].fillna(0)).cumprod() - 1

# Count trades
num_trades = (data["Position"].diff().abs() == 2).sum()


# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data["Close"], label="Close Price", alpha=0.5)
ax.plot(data["SMA_Short"], label=f"SMA{sma_short}", linestyle="--")
ax.plot(data["SMA_Long"], label=f"SMA{sma_long}", linestyle="--")


# Buy/Sell Markers
buy_signals = data[data["Signal"] == 1]
sell_signals = data[data["Signal"] == -1]
ax.scatter(buy_signals.index, buy_signals["Close"], label="Buy", marker="^", color="green")
ax.scatter(sell_signals.index, sell_signals["Close"], label="Sell", marker="v", color="red")

ax.set_title(f"{ticker} - MA Crossover Strategy")
# Display strategy performance
st.subheader("📊 Strategy Performance Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Strategy Return", f"{cumulative_strategy_return.iloc[-1]*100:.2f}%")
col2.metric("Buy & Hold Return", f"{cumulative_stock_return.iloc[-1]*100:.2f}%")
col3.metric("Trades Executed", f"{int(num_trades)}")
ax.legend()
st.pyplot(fig)

# Plot RSI
fig2, ax2 = plt.subplots(figsize=(12, 3))
ax2.plot(data["RSI"], label="RSI", color="purple")
ax2.axhline(70, color="red", linestyle="--", alpha=0.5)
ax2.axhline(30, color="green", linestyle="--", alpha=0.5)
ax2.set_title("RSI (14)")
ax2.legend()
st.pyplot(fig2)


st.subheader("Performance Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Strategy Return", f"{cumulative_strategy_return.iloc[-1]*100:.2f}%")
col2.metric("Buy & Hold Return", f"{cumulative_stock_return.iloc[-1]*100:.2f}%")
col3.metric("Total Trades", int(num_trades))
# Create trade log DataFrame
trades = data[data["Position"].diff().abs() == 2].copy()
trades["Action"] = trades["Position"].apply(lambda x: "Buy" if x == 1 else "Sell")
trade_log = trades[["Action", "Close"]]
trade_log["Date"] = trades.index
trade_log = trade_log[["Date", "Action", "Close"]].reset_index(drop=True)

# Show trade log in Streamlit
st.subheader("🧾 Trade Log")
st.dataframe(trade_log, use_container_width=True)

