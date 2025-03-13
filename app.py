#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Real-Time Financial Dashboard
=============================
This script initializes a Dash web application to display real-time stock prices 
and macroeconomic indicators using APIs and web scraping.

Features:
- Fetches stock data using Yahoo Finance (`yfinance`)
- Displays real-time price updates (every 5 seconds)
- Web-scrapes financial news headlines with sentiment analysis
- Integrates macroeconomic indicators (inflation, bond yields, etc.)

Author: mirandabohm
Created: Tues Jan 7 2025
Last Updated: Tues Mar 11 2025
Version: 1.0
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc  # For improved styling
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import yfinance as yf
from styles import light_theme, dark_theme, get_global_styles  # Import styles

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define available periods and intervals
period_options = ["1d", "5d", "1mo", "3mo", "1y"]
interval_options = ["1m", "5m", "15m", "1h", "1d"]

# Define Layout
app.layout = html.Div([
    html.H1("Real-Time Financial Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),

    dbc.Switch(
        id="theme-switch",
        value=False,  # Default: Light Mode
        className="theme-toggle",
        style={"textAlign": "center", "marginBottom": "20px"}
    ),

    html.Div([
        html.Div([
            html.H2("📈 Stock Market Data"),
            dcc.Input(id="stock-input", type="text", value="AAPL", debounce=True, 
                      style={"marginBottom": "10px", "width": "100%"}),
            html.Div(id="live-price", children="💲 Current Price: (Loading...)"),
            dcc.Graph(id="stock-chart", figure={}),
            
            # Period Selection Buttons
            html.Div([
                html.H5("Select Time Period:"),
                *[dbc.Button(period, id={"type": "period-button", "index": period}, 
                             color="primary", outline=True, className="me-1") for period in period_options]
            ], style={"marginTop": "10px", "textAlign": "center"}),

            # Interval Selection Buttons
            html.Div([
                html.H5("Select Candlestick Interval:"),
                *[dbc.Button(interval, id={"type": "interval-button", "index": interval}, 
                             color="secondary", outline=True, className="me-1") for interval in interval_options]
            ], style={"marginTop": "10px", "textAlign": "center"}),
        ], style={"width": "50%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"}),

        # Macro Indicators & News
        html.Div([
            html.H2("🌎 Macroeconomic Indicators"),
            html.Div(id="macro-data", children=[
                html.Div("📉 10-Year Treasury Yield: (Loading...)", id="treasury-yield"),
                html.Div("💹 Inflation (CPI): (Loading...)", id="inflation"),
                html.Div("🛢️ Gold, Oil, Bitcoin: (Loading...)", id="commodities"),
            ]),
            html.H2("📰 Financial News"),
            html.Div(id="news-feed", children="Latest headlines will go here..."),
        ], style={"width": "50%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"}),
    ], style={"display": "flex", "justifyContent": "space-between"}),  
], id="page-content")  # ✅ Ensures dark mode applies globally

# Callback to update stock price & chart
@app.callback(
    [Output("live-price", "children"), Output("stock-chart", "figure")],
    [Input("stock-input", "value"), Input("theme-switch", "value"),
     Input({"type": "period-button", "index": dash.ALL}, "n_clicks"),
     Input({"type": "interval-button", "index": dash.ALL}, "n_clicks")]
)
def update_stock_price(ticker, is_dark_mode, period_clicks, interval_clicks):
    selected_theme = "dark" if is_dark_mode else "light"
    period = period_options[next((i for i, v in enumerate(period_clicks) if v), 0)]  # Default to first option if no click
    interval = interval_options[next((i for i, v in enumerate(interval_clicks) if v), 0)]  # Default to first option if no click
    print(f"Fetching stock data for: {ticker} with period={period} and interval={interval}")  # Debugging print

    try:
        stock_data = yf.Ticker(ticker)
        latest_price = stock_data.fast_info["lastPrice"]
        price_text = f"Current Price: ${latest_price:.2f}"

        stock_price = stock_data.history(period=period, interval=interval)

        if stock_price.empty:
            return f"Invalid Ticker: {ticker}", go.Figure()

        # Select theme colors
        theme = dark_theme if selected_theme == "dark" else light_theme

        # Create the candlestick chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=stock_price.index,
            open=stock_price["Open"],
            high=stock_price["High"],
            low=stock_price["Low"],
            close=stock_price["Close"],
            increasing_line_color="lime" if selected_theme == "dark" else "green",
            decreasing_line_color="red"
        ))

        fig.update_layout(
            title=f"{ticker} Stock Price",
            xaxis_title="Time",
            yaxis_title="Price ($)",
            plot_bgcolor=theme["graph_bg"],
            paper_bgcolor=theme["graph_bg"],
            font=dict(color=theme["graph_text"]),
            xaxis=dict(gridcolor="gray"),
            yaxis=dict(gridcolor="gray")
        )

        return price_text, fig

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return f"Error: {str(e)}", go.Figure()

# Callback to update page theme
@app.callback(
    Output("page-content", "style"),
    Input("theme-switch", "value")
)
def update_theme(is_dark_mode):
    theme = dark_theme if is_dark_mode else light_theme
    return {
        "backgroundColor": theme["background"],  
        "color": theme["text"],  
        "height": "100vh",  
        "width": "100vw",
        "fontFamily": "Arial, sans-serif",  
        "padding": "20px",
        "transition": "background-color 0.5s ease"
    }

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
