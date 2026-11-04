import os
import yfinance as yf
import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

DATA_FOLDER = "data"

# NIFTY 50 / major Indian stocks
STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "ITC.NS",
    "LT.NS",
    "HINDUNILVR.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "BAJFINANCE.NS",
    "MARUTI.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "SUNPHARMA.NS",
    "WIPRO.NS",
    "TECHM.NS",
    "HCLTECH.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "ONGC.NS",
    "COALINDIA.NS",
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "ASIANPAINT.NS",
    "BAJAJFINSV.NS",
    "BEL.NS",
    "BPCL.NS",
    "CIPLA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HEROMOTOCO.NS",
    "INDUSINDBK.NS",
    "JSWSTEEL.NS",
    "M&M.NS",
    "NESTLEIND.NS",
    "TATACONSUM.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "UPL.NS",
    "APOLLOHOSP.NS",
    "HINDALCO.NS",
    "SHRIRAMFIN.NS",
    "SBILIFE.NS",
    "TRENT.NS",
    "TATAELXSI.NS"
]

START_DATE = "2010-01-01"

# ============================================================
# CREATE DATA FOLDER
# ============================================================

os.makedirs(DATA_FOLDER, exist_ok=True)

print("=" * 60)
print("STOCK MARKET DATA DOWNLOADER")
print("=" * 60)

print(f"\nStocks: {len(STOCKS)}")
print(f"Start date: {START_DATE}")
print("Downloading daily historical data...\n")


# ============================================================
# DOWNLOAD DATA
# ============================================================

all_data = []

for ticker in STOCKS:

    print(f"Downloading {ticker}...")

    try:

        df = yf.download(
            ticker,
            start=START_DATE,
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"  WARNING: No data found for {ticker}")
            continue

        # Handle yfinance MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        # Keep required columns
        required_columns = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        df = df[
            [
                column
                for column in required_columns
                if column in df.columns
            ]
        ]

        # Add stock name
        df["Stock"] = ticker.replace(".NS", "")

        all_data.append(df)

        print(
            f"  Downloaded {len(df):,} records"
        )

    except Exception as e:

        print(
            f"  ERROR downloading {ticker}: {e}"
        )


# ============================================================
# COMBINE ALL STOCKS
# ============================================================

print("\nCombining datasets...")

if not all_data:
    print("No data downloaded.")
    exit()

final_df = pd.concat(
    all_data,
    ignore_index=True
)


# ============================================================
# ORGANIZE COLUMNS
# ============================================================

final_df = final_df[
    [
        "Date",
        "Stock",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]
]


# ============================================================
# CLEAN DATA
# ============================================================

final_df["Date"] = pd.to_datetime(
    final_df["Date"]
)

numeric_columns = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

for column in numeric_columns:

    final_df[column] = pd.to_numeric(
        final_df[column],
        errors="coerce"
    )


# Remove missing values
final_df = final_df.dropna()


# Remove duplicates
final_df = final_df.drop_duplicates()


# Sort data
final_df = final_df.sort_values(
    ["Stock", "Date"]
)


# ============================================================
# SAVE DATASET
# ============================================================

output_file = os.path.join(
    DATA_FOLDER,
    "stock_data.csv"
)

final_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DOWNLOAD COMPLETED")
print("=" * 60)

print(f"\nFile created:")
print(output_file)

print(
    f"\nTotal records: {len(final_df):,}"
)

print(
    f"Total stocks: {final_df['Stock'].nunique()}"
)

print(
    f"Date range: "
    f"{final_df['Date'].min().date()} "
    f"to "
    f"{final_df['Date'].max().date()}"
)

print("\nRecords per stock:")

print(
    final_df
    .groupby("Stock")
    .size()
    .sort_values(ascending=False)
)

print("\nDataset size:")

file_size_mb = (
    os.path.getsize(output_file)
    / (1024 * 1024)
)

print(
    f"{file_size_mb:.2f} MB"
)

print("\nFirst 10 records:")

print(
    final_df.head(10).to_string(
        index=False
    )
)

print("\nDataset successfully saved.")