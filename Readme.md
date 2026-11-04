# Stock Market Analysis Using Big Data Analytics

A Big Data Analytics project that analyzes historical stock market data using Python, Pandas, NumPy, and Apache Spark. The project processes stock market information, identifies trends, calculates financial indicators, and presents insights through an interactive Streamlit dashboard.

## Project Details

| Detail | Information |
|---|---|
| Project Title | Stock Market Analysis |
| Domain | Big Data Analytics |
| Department | Computer Science and Engineering |
| College | Guru Nanak Dev Engineering College, Bidar |
| Academic Year | 2026–2027 |

### Team Members

| Name | USN |
|---|---|
| Darshan | 3GN23CS020 |
| Vishwa | 3GN22CS124 |

---

## 1. Overview

Stock market data contains large volumes of historical information, including opening prices, closing prices, highest and lowest prices, and trading volumes.

This project uses Big Data Analytics techniques to process and analyze historical stock market data. It helps users understand stock price movements, identify market trends, compare companies, and explore trading patterns through visualizations.

The project uses **Apache Spark (PySpark)** for distributed data processing and **Python-based libraries** for data analysis and visualization.

## 2. Objectives

- Collect historical stock market data.
- Clean and preprocess the collected dataset.
- Analyze stock prices and trading volumes.
- Calculate daily returns and moving averages.
- Identify volatility and unusual trading activity.
- Perform large-scale data processing using Apache Spark.
- Visualize stock market trends through an interactive dashboard.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Apache Spark (PySpark) | Big Data processing |
| Matplotlib | Data visualization |
| Plotly | Interactive charts |
| Streamlit | Interactive web dashboard |
| yfinance | Historical stock market data collection |

## 4. Project Features

- Historical stock market data collection.
- Data cleaning and preprocessing.
- Daily stock return calculations.
- Moving average analysis (MA20 and MA50).
- Stock price trend visualization.
- Trading volume analysis.
- Rolling volatility analysis.
- Stock correlation analysis.
- Unusual trading volume identification.
- Interactive stock selection and date filtering.
- Downloadable historical data.

## 5. Project Structure

```text
Stock-Market-Analysis/
│
├── data/
│   └── stock_data.csv
│
├── outputs/
│   ├── charts/
│   └── analysis_results/
│
├── download_stock_data.py
├── stock_market_analysis.py
├── dashboard.py
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The structure above is the intended project layout. Adjust filenames and folders if your actual implementation differs.*

## 6. Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.11 or later
- Java Development Kit (JDK), compatible with your PySpark version
- Git
- A code editor such as Visual Studio Code

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

```bash
cd Stock-Market-Analysis
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the dependencies manually:

```bash
pip install pandas numpy matplotlib pyspark yfinance streamlit plotly
```

### Step 4: Download Stock Market Data

Run:

```bash
python download_stock_data.py
```

The script downloads historical stock market information and saves the processed dataset as:

```text
data/stock_data.csv
```

### Step 5: Run Data Analysis

```bash
python stock_market_analysis.py
```

This performs data preprocessing, statistical analysis, and Spark-based aggregations.

### Step 6: Launch the Dashboard

```bash
streamlit run dashboard.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 7. Dataset Description

The project uses historical stock market data obtained through Yahoo Finance using the `yfinance` Python library.

The dataset contains the following fields:

| Column | Description |
|---|---|
| Date | Trading date |
| Stock | Stock symbol |
| Open | Opening stock price |
| High | Highest price during the trading session |
| Low | Lowest price during the trading session |
| Close | Closing stock price |
| Volume | Number of shares traded |

The project can analyze multiple NSE-listed companies, including Reliance, TCS, Infosys, HDFC Bank, ICICI Bank, SBI, and other selected stocks.

## 8. Analysis Performed

### 8.1 Daily Returns

Calculates the percentage change in closing prices between consecutive trading sessions.

### 8.2 Moving Averages

- MA20: 20-trading-day moving average.
- MA50: 50-trading-day moving average.

These indicators help identify short-term and medium-term price trends.

### 8.3 Volatility Analysis

Measures fluctuations in stock returns to understand changes in market risk.

### 8.4 Volume Analysis

Examines trading activity and identifies unusual volume changes.

### 8.5 Correlation Analysis

Compares stock price movements to identify relationships between selected companies.

### 8.6 Apache Spark Processing

Uses PySpark DataFrames and aggregation operations to process stock market records and calculate summary statistics.

## 9. Dashboard

The Streamlit dashboard provides an interactive interface for exploring stock market data.

Main dashboard components include:

- Stock selection.
- Date-range filtering.
- Opening and closing price information.
- Stock price charts.
- Moving average indicators.
- Trading volume charts.
- Daily return visualization.
- Rolling volatility.
- Unusual volume records.
- Historical data table.
- CSV data download.

## 10. Expected Output

The project generates analytical information such as:

- Historical stock price trends.
- Daily percentage returns.
- Moving average comparisons.
- Trading volume patterns.
- Volatility measurements.
- Stock correlation results.
- Summary statistics generated through Spark.

Actual results depend on the downloaded dataset and the selected date range.

## 11. Limitations

- Historical data availability depends on the external data provider.
- Stock market prices may be delayed or adjusted.
- Internet connectivity is required to download fresh data.
- Historical analysis does not guarantee future stock performance.
- The project is intended for academic analysis and is not an investment recommendation.

## 12. Future Enhancements

- Integrate real-time stock market data.
- Add machine learning-based price forecasting.
- Implement sentiment analysis using financial news.
- Include additional technical indicators.
- Deploy the dashboard to a cloud platform.
- Improve scalability using larger distributed datasets.

## 13. Disclaimer

This project is developed strictly for educational and academic purposes as part of the Big Data Analytics curriculum. The analysis and visualizations are not intended to provide financial or investment advice.

## 14. Authors

**Darshan** — 3GN23CS020  
**Vishwa** — 3GN22CS124

Department of Computer Science and Engineering  
Guru Nanak Dev Engineering College, Bidar.