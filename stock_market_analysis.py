# ============================================================
# STOCK MARKET DATA ANALYSIS USING PYTHON AND APACHE SPARK
# BDA MINI PROJECT
# ============================================================

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    avg,
    max,
    min,
    stddev,
    count
)

warnings.filterwarnings("ignore")


# ============================================================
# 1. CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs("output", exist_ok=True)


# ============================================================
# 2. LOAD DATA USING PANDAS
# ============================================================

print("\n==========================================")
print("STOCK MARKET DATA ANALYSIS")
print("==========================================")

file_path = "data/stock_data.csv"

df = pd.read_csv(file_path)

print("\nDataset loaded successfully.")

print("\nFirst 5 records:")
print(df.head())


# ============================================================
# 3. DATA INFORMATION
# ============================================================

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())


# ============================================================
# 4. DATA CLEANING
# ============================================================

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numerical columns
numeric_columns = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Remove missing values
df = df.dropna()

# Remove duplicate records
df = df.drop_duplicates()

# Sort data
df = df.sort_values(
    by=["Stock", "Date"]
)

print("\nData cleaning completed.")

print("\nCleaned Dataset:")
print(df.head())


# ============================================================
# 5. BASIC STATISTICS
# ============================================================

print("\n==========================================")
print("BASIC STATISTICS")
print("==========================================")

print(
    df[
        ["Open", "High", "Low", "Close", "Volume"]
    ].describe()
)


# ============================================================
# 6. DAILY RETURN CALCULATION
# ============================================================

df["Daily_Return"] = (
    df.groupby("Stock")["Close"]
    .pct_change()
    * 100
)

print("\nDaily Return:")
print(
    df[
        ["Date", "Stock", "Close", "Daily_Return"]
    ].head(10)
)


# ============================================================
# 7. DAILY PRICE CHANGE
# ============================================================

df["Price_Change"] = (
    df.groupby("Stock")["Close"]
    .diff()
)

print("\nPrice Change:")
print(
    df[
        ["Date", "Stock", "Close", "Price_Change"]
    ].head(10)
)


# ============================================================
# 8. MOVING AVERAGES
# ============================================================

df["MA_20"] = (
    df.groupby("Stock")["Close"]
    .transform(
        lambda x: x.rolling(20).mean()
    )
)

df["MA_50"] = (
    df.groupby("Stock")["Close"]
    .transform(
        lambda x: x.rolling(50).mean()
    )
)

print("\nMoving averages calculated.")


# ============================================================
# 9. VOLATILITY CALCULATION
# ============================================================

volatility = (
    df.groupby("Stock")["Daily_Return"]
    .std()
    .sort_values(ascending=False)
)

print("\n==========================================")
print("STOCK VOLATILITY")
print("==========================================")

print(volatility)


# ============================================================
# 10. AVERAGE RETURN
# ============================================================

average_return = (
    df.groupby("Stock")["Daily_Return"]
    .mean()
    .sort_values(ascending=False)
)

print("\n==========================================")
print("AVERAGE DAILY RETURN")
print("==========================================")

print(average_return)


# ============================================================
# 11. TRADING VOLUME ANALYSIS
# ============================================================

average_volume = (
    df.groupby("Stock")["Volume"]
    .mean()
    .sort_values(ascending=False)
)

print("\n==========================================")
print("AVERAGE TRADING VOLUME")
print("==========================================")

print(average_volume)


# ============================================================
# 12. VOLUME RATIO
# ============================================================

df["Average_Volume_20"] = (
    df.groupby("Stock")["Volume"]
    .transform(
        lambda x: x.rolling(20).mean()
    )
)

df["Volume_Ratio"] = (
    df["Volume"] /
    df["Average_Volume_20"]
)

# Unusual volume
df["Unusual_Volume"] = (
    df["Volume_Ratio"] > 2
)

print("\nUnusual volume records:")

print(
    df[
        df["Unusual_Volume"] == True
    ][
        [
            "Date",
            "Stock",
            "Volume",
            "Volume_Ratio"
        ]
    ].head(20)
)


# ============================================================
# 13. HIGHEST AND LOWEST CLOSING PRICE
# ============================================================

highest_price = (
    df.groupby("Stock")["Close"]
    .max()
)

lowest_price = (
    df.groupby("Stock")["Close"]
    .min()
)

print("\n==========================================")
print("HIGHEST CLOSING PRICE")
print("==========================================")

print(highest_price)

print("\n==========================================")
print("LOWEST CLOSING PRICE")
print("==========================================")

print(lowest_price)


# ============================================================
# 14. TOTAL RETURN
# ============================================================

total_return = (
    df.groupby("Stock")
    .apply(
        lambda x:
        (
            x["Close"].iloc[-1]
            -
            x["Close"].iloc[0]
        )
        /
        x["Close"].iloc[0]
        * 100
    )
)

print("\n==========================================")
print("TOTAL RETURN")
print("==========================================")

print(total_return)


# ============================================================
# 15. CORRELATION ANALYSIS
# ============================================================

price_data = df.pivot(
    index="Date",
    columns="Stock",
    values="Close"
)

correlation_matrix = price_data.corr()

print("\n==========================================")
print("CORRELATION MATRIX")
print("==========================================")

print(correlation_matrix)


# Save correlation matrix
correlation_matrix.to_csv(
    "output/correlation_matrix.csv"
)


# ============================================================
# 16. VISUALIZATION - STOCK PRICE
# ============================================================

stocks = df["Stock"].unique()

for stock in stocks:

    stock_df = df[
        df["Stock"] == stock
    ]

    plt.figure(figsize=(12, 6))

    plt.plot(
        stock_df["Date"],
        stock_df["Close"],
        label="Closing Price"
    )

    plt.plot(
        stock_df["Date"],
        stock_df["MA_20"],
        label="20-Day MA"
    )

    plt.plot(
        stock_df["Date"],
        stock_df["MA_50"],
        label="50-Day MA"
    )

    plt.title(
        f"{stock} Stock Price and Moving Averages"
    )

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"output/{stock}_price_analysis.png"
    )

    plt.show()


# ============================================================
# 17. VISUALIZATION - TRADING VOLUME
# ============================================================

for stock in stocks:

    stock_df = df[
        df["Stock"] == stock
    ]

    plt.figure(figsize=(12, 5))

    plt.bar(
        stock_df["Date"],
        stock_df["Volume"]
    )

    plt.title(
        f"{stock} Trading Volume"
    )

    plt.xlabel("Date")
    plt.ylabel("Volume")

    plt.tight_layout()

    plt.savefig(
        f"output/{stock}_volume.png"
    )

    plt.show()


# ============================================================
# 18. VISUALIZATION - DAILY RETURNS
# ============================================================

for stock in stocks:

    stock_df = df[
        df["Stock"] == stock
    ]

    plt.figure(figsize=(12, 5))

    plt.plot(
        stock_df["Date"],
        stock_df["Daily_Return"]
    )

    plt.axhline(
        0,
        linestyle="--"
    )

    plt.title(
        f"{stock} Daily Returns"
    )

    plt.xlabel("Date")

    plt.ylabel(
        "Daily Return (%)"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"output/{stock}_daily_returns.png"
    )

    plt.show()


# ============================================================
# 19. VISUALIZATION - VOLATILITY
# ============================================================

plt.figure(figsize=(10, 6))

volatility.plot(
    kind="bar"
)

plt.title(
    "Stock Volatility Comparison"
)

plt.xlabel("Stock")

plt.ylabel(
    "Standard Deviation of Daily Returns"
)

plt.tight_layout()

plt.savefig(
    "output/volatility_comparison.png"
)

plt.show()


# ============================================================
# 20. VISUALIZATION - AVERAGE VOLUME
# ============================================================

plt.figure(figsize=(10, 6))

average_volume.plot(
    kind="bar"
)

plt.title(
    "Average Trading Volume by Stock"
)

plt.xlabel("Stock")

plt.ylabel(
    "Average Volume"
)

plt.tight_layout()

plt.savefig(
    "output/average_volume.png"
)

plt.show()


# ============================================================
# 21. CORRELATION HEATMAP USING MATPLOTLIB
# ============================================================

plt.figure(figsize=(10, 7))

plt.imshow(
    correlation_matrix,
    interpolation="nearest"
)

plt.colorbar()

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=45
)

plt.yticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

plt.title(
    "Stock Price Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    "output/correlation_heatmap.png"
)

plt.show()


# ============================================================
# 22. APACHE SPARK INITIALIZATION
# ============================================================

print("\n==========================================")
print("APACHE SPARK ANALYSIS")
print("==========================================")

spark = SparkSession.builder \
    .appName("StockMarketBDA") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\nSpark Session Started.")


# ============================================================
# 23. LOAD DATA INTO SPARK
# ============================================================

spark_df = spark.read.csv(
    file_path,
    header=True,
    inferSchema=True
)

print("\nSpark DataFrame:")

spark_df.show(10)

print("\nSpark Schema:")

spark_df.printSchema()


# ============================================================
# 24. SPARK DATA CLEANING
# ============================================================

spark_df = spark_df.dropDuplicates()

spark_df = spark_df.dropna()

print("\nCleaned Spark Data:")

spark_df.show(10)


# ============================================================
# 25. SPARK GROUP-BY ANALYSIS
# ============================================================

spark_summary = (
    spark_df
    .groupBy("Stock")
    .agg(
        avg("Close").alias(
            "Average_Close"
        ),

        max("Close").alias(
            "Maximum_Close"
        ),

        min("Close").alias(
            "Minimum_Close"
        ),

        avg("Volume").alias(
            "Average_Volume"
        ),

        stddev("Close").alias(
            "Price_StdDev"
        ),

        count("*").alias(
            "Number_of_Records"
        )
    )
)

print("\n==========================================")
print("SPARK STOCK SUMMARY")
print("==========================================")

spark_summary.show()


# ============================================================
# 26. SPARK SORTING
# ============================================================

print("\nStocks sorted by average closing price:")

spark_summary \
    .orderBy(
        col("Average_Close").desc()
    ) \
    .show()


# ============================================================
# 27. SPARK VOLUME ANALYSIS
# ============================================================

print("\nStocks sorted by average trading volume:")

spark_summary \
    .orderBy(
        col("Average_Volume").desc()
    ) \
    .show()


# ============================================================
# 28. SAVE SPARK RESULTS
# ============================================================

spark_summary \
    .coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(
        "output/spark_summary"
    )


# ============================================================
# 29. SAVE PROCESSED DATA
# ============================================================

df.to_csv(
    "output/processed_stock_data.csv",
    index=False
)


# ============================================================
# 30. STOP SPARK
# ============================================================

spark.stop()

print("\n==========================================")
print("PROJECT COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nGenerated files are available inside:")
print("output/")