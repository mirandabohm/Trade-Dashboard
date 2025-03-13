# Real-Time Financial Dashboard

## Overview
This project is a **real-time financial dashboard** built using Python and Dash. It will provide a convenient interface for users wishing to track **security prices, macroeconomic indicators, and financial news**.

## Features
- 📈 **Live Stock Price Tracking** (Using `yfinance` for real-time updates)
- 🔄 **Selectable Time Periods & Candlestick Intervals**
- 🌎 **Macroeconomic Indicators** (Treasury Yields, Inflation, Commodities)
- 📰 **Financial News with Sentiment Analysis**

## Installation
### Prerequisites
Make sure you have **Python 3.7+** and **Anaconda** installed.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mirandabohm/Trade-Dashboard.git
cd Trade-Dashboard
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
conda create --name trade_dashboard python=3.8 -y
conda activate trade_dashboard
```

### 3️⃣ Install Dependencies
Using `pip`:
```bash
pip install -r requirements.txt
```
Or using `conda`:
```bash
conda install dash plotly pandas requests yfinance -c conda-forge
```

## Running the Application
```bash
python app.py
```
Then, open your browser and go to **`http://127.0.0.1:8050/`**

## Usage
1. **Enter a stock ticker** (e.g., `AAPL`, `TSLA`) in the input field.
2. **Select a time period & candlestick interval** using the buttons.
3. **Switch between Light/Dark Mode** using the toggle switch.
4. **View macroeconomic indicators & financial news** on the right panel.

## Folder Structure
```
Trade-Dashboard/
│── app.py                 # Main application file
│── styles.py              # Theme settings for light & dark mode
│── requirements.txt       # List of dependencies
│── README.md              # Project documentation
│── assets/
│   └── style.css          # Custom CSS for UI enhancements
```

## Contributing
Feel free to open a pull request if you'd like to **add features or improve the dashboard!** 🚀

