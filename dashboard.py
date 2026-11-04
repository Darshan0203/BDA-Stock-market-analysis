
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from plotly.subplots import make_subplots


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Stock Market Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.2);
        padding: 15px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA
# =====================================================

DATA_PATH = "data/stock_data.csv"


@st.cache_data
def load_data():

    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    data = pd.read_csv(DATA_PATH)

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    numeric_cols = [
        "Open", "High", "Low", "Close", "Volume"
    ]

    for col in numeric_cols:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    data = data.dropna(
        subset=["Date", "Stock", "Open",
                "High", "Low", "Close", "Volume"]
    )

    data = data.drop_duplicates(
        subset=["Date", "Stock"]
    )

    data = data.sort_values(
        ["Stock", "Date"]
    )

    return data


df = load_data()


if df.empty:
    st.error("Dataset not found or empty.")
    st.info("Place stock_data.csv inside the data folder.")
    st.stop()


# =====================================================
# HEADER
# =====================================================

st.title("📈 Stock Market Analytics Dashboard")

st.caption(
    "Big Data Analytics Mini Project | "
    "Python • Pandas • NumPy • Apache Spark"
)

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Dashboard Controls")

stocks = sorted(df["Stock"].unique().tolist())

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stocks
)

stock_data = df[
    df["Stock"] == selected_stock
].copy()

min_date = stock_data["Date"].min().date()
max_date = stock_data["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.warning("Select both start and end dates.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

stock_data = stock_data[
    (stock_data["Date"].dt.date >= start_date) &
    (stock_data["Date"].dt.date <= end_date)
].copy()

if stock_data.empty:
    st.warning("No records found for this date range.")
    st.stop()


# =====================================================
# CALCULATE ANALYTICS
# =====================================================

stock_data = stock_data.sort_values("Date")

stock_data["Daily_Return"] = (
    stock_data["Close"].pct_change() * 100
)

stock_data["MA_20"] = (
    stock_data["Close"].rolling(20).mean()
)

stock_data["MA_50"] = (
    stock_data["Close"].rolling(50).mean()
)

stock_data["Rolling_Volatility"] = (
    stock_data["Daily_Return"]
    .rolling(20)
    .std()
)

stock_data["Average_Volume_20"] = (
    stock_data["Volume"].rolling(20).mean()
)

stock_data["Volume_Ratio"] = (
    stock_data["Volume"] /
    stock_data["Average_Volume_20"].replace(0, np.nan)
)

stock_data["Unusual_Volume"] = (
    stock_data["Volume_Ratio"] > 2
)


# =====================================================
# KEY PERFORMANCE INDICATORS
# =====================================================

latest = stock_data.iloc[-1]

first_close = stock_data["Close"].iloc[0]
last_close = stock_data["Close"].iloc[-1]

period_return = (
    (last_close - first_close) /
    first_close * 100
) if first_close else 0

previous_close = (
    stock_data["Close"].iloc[-2]
    if len(stock_data) > 1
    else np.nan
)

daily_change = (
    (last_close / previous_close - 1) * 100
    if pd.notna(previous_close) and previous_close != 0
    else np.nan
)

high_price = stock_data["High"].max()
low_price = stock_data["Low"].min()

avg_volume = stock_data["Volume"].mean()

volatility = (
    stock_data["Daily_Return"].std()
    if stock_data["Daily_Return"].notna().sum() > 1
    else 0
)


# =====================================================
# STOCK OVERVIEW
# =====================================================

st.subheader(f"{selected_stock} — Stock Overview")

st.caption(
    f"Historical data: {start_date} to {end_date}"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Latest Close",
    f"₹{last_close:,.2f}",
    f"{daily_change:+.2f}%" if pd.notna(daily_change) else None
)

c2.metric(
    "Period Return",
    f"{period_return:+.2f}%"
)

c3.metric(
    "Highest Price",
    f"₹{high_price:,.2f}"
)

c4.metric(
    "Lowest Price",
    f"₹{low_price:,.2f}"
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Average Volume",
    f"{avg_volume:,.0f}"
)

c6.metric(
    "Daily Volatility",
    f"{volatility:.2f}%"
)

c7.metric(
    "Total Trading Days",
    f"{len(stock_data):,}"
)

c8.metric(
    "Unusual Volume Days",
    f"{int(stock_data['Unusual_Volume'].sum()):,}"
)


# =====================================================
# PRICE CHART
# =====================================================

st.divider()

st.subheader("Price Movement Analysis")

show_ma20 = st.sidebar.checkbox(
    "Show 20-Day Moving Average", True
)

show_ma50 = st.sidebar.checkbox(
    "Show 50-Day Moving Average", True
)

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=stock_data["Date"],
        open=stock_data["Open"],
        high=stock_data["High"],
        low=stock_data["Low"],
        close=stock_data["Close"],
        name="Price"
    )
)

if show_ma20:
    fig.add_trace(
        go.Scatter(
            x=stock_data["Date"],
            y=stock_data["MA_20"],
            name="20-Day MA",
            line=dict(width=2)
        )
    )

if show_ma50:
    fig.add_trace(
        go.Scatter(
            x=stock_data["Date"],
            y=stock_data["MA_50"],
            name="50-Day MA",
            line=dict(width=2)
        )
    )

fig.update_layout(
    height=550,
    xaxis_rangeslider_visible=False,
    template="plotly_dark",
    hovermode="x unified",
    yaxis_title="Price (INR)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# VOLUME ANALYSIS
# =====================================================

st.divider()

st.subheader("Trading Volume Analysis")

volume_fig = go.Figure()

volume_fig.add_trace(
    go.Bar(
        x=stock_data["Date"],
        y=stock_data["Volume"],
        name="Trading Volume"
    )
)

volume_fig.add_trace(
    go.Scatter(
        x=stock_data["Date"],
        y=stock_data["Average_Volume_20"],
        name="20-Day Average Volume",
        line=dict(width=2)
    )
)

volume_fig.update_layout(
    template="plotly_dark",
    height=400,
    hovermode="x unified",
    yaxis_title="Number of Shares"
)

st.plotly_chart(
    volume_fig,
    use_container_width=True
)


# =====================================================
# DAILY RETURNS AND VOLATILITY
# =====================================================

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("Daily Returns")

    return_fig = px.bar(
        stock_data,
        x="Date",
        y="Daily_Return",
        title="Daily Percentage Returns"
    )

    return_fig.add_hline(
        y=0,
        line_dash="dash"
    )

    return_fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        return_fig,
        use_container_width=True
    )


with right:

    st.subheader("Rolling Volatility")

    volatility_fig = px.line(
        stock_data,
        x="Date",
        y="Rolling_Volatility",
        title="20-Day Rolling Volatility"
    )

    volatility_fig.update_layout(
        template="plotly_dark",
        height=400,
        yaxis_title="Standard Deviation (%)"
    )

    st.plotly_chart(
        volatility_fig,
        use_container_width=True
    )


# =====================================================
# UNUSUAL MARKET ACTIVITY
# =====================================================

st.divider()

st.subheader("Unusual Trading Activity")

unusual_data = stock_data[
    stock_data["Unusual_Volume"]
].copy()

if unusual_data.empty:

    st.success(
        "No unusual volume days detected in this period."
    )

else:

    st.warning(
        f"{len(unusual_data)} days recorded volume "
        "more than twice their 20-day average."
    )

    st.dataframe(
        unusual_data[
            [
                "Date",
                "Close",
                "Volume",
                "Average_Volume_20",
                "Volume_Ratio"
            ]
        ].sort_values(
            "Volume_Ratio",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# HISTORICAL DATA TABLE
# =====================================================

st.divider()

st.subheader("Historical Stock Records")

st.dataframe(
    stock_data.sort_values(
        "Date", ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# =====================================================
# DOWNLOAD DATA
# =====================================================

csv = stock_data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Stock Analysis CSV",
    data=csv,
    file_name=f"{selected_stock}_analysis.csv",
    mime="text/csv"
)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Stock Market Data Analysis | "
    "BDA Mini Project | "
    "Historical data analysis only. "
    "Not investment advice."
)

st.caption(
    f"Dataset contains {len(df):,} records "
    f"across {df['Stock'].nunique()} stocks."
)
