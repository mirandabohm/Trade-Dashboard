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
import dash_bootstrap_components as dbc  # Import Bootstrap Components
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import yfinance as yf
from styles import light_theme, dark_theme, get_global_styles  # Import styles

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define Layout
app.layout = html.Div([
    html.H1("Real-Time Financial Dashboard", id="title", style={"textAlign": "center"}),

    # Dark Mode Toggle Switch
    html.Div([
        html.Label(""),
        dbc.Switch(
            id="theme-switch",
            label="",
            value=False,  # Default: Light Mode
            className="theme-toggle"
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Stock Input
    dcc.Input(id="stock-input", type="text", value="AAPL", debounce=True, style={'marginRight': '10px'}),

    # Live Price Display
    html.Div(id="live-price", style={'fontSize': 24, 'marginTop': 10}),

    # Stock Price Graph
    dcc.Graph(id="stock-chart"),

    # Auto-update interval
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
], id="page-content", style={"minHeight": "100vh"})  # Ensures full-page styling

# Callback to update theme dynamically
@app.callback(
    Output("page-content", "style"),
    Input("theme-switch", "value")
)
def update_theme(is_dark_mode):
    selected_theme = "dark" if is_dark_mode else "light"
    return get_global_styles(selected_theme)

# Callback to update stock price & chart
@app.callback(
    [Output("live-price", "children"), Output("stock-chart", "figure")],
    [Input("stock-input", "value"), Input("interval-component", "n_intervals"), Input("theme-switch", "value")]
)
def update_stock_price(ticker, n, is_dark_mode):
    selected_theme = "dark" if is_dark_mode else "light"
    print(f"Fetching stock data for: {ticker}")  # Debugging print

    try:
        stock_data = yf.Ticker(ticker)
        latest_price = stock_data.fast_info["lastPrice"]
        price_text = f"Current Price: ${latest_price:.2f}"

        stock_price = stock_data.history(period="1d", interval="1m")

        if stock_price.empty:
            return f"Invalid Ticker: {ticker}", go.Figure()

        # Select theme colors
        theme = dark_theme if selected_theme == "dark" else light_theme

        # Define candlestick colors
        candlestick_colors = dict(
            increasing_line_color="lime" if selected_theme == "dark" else "green",
            decreasing_line_color="red"
        )

        # Create the candlestick chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=stock_price.index,
            open=stock_price["Open"],
            high=stock_price["High"],
            low=stock_price["Low"],
            close=stock_price["Close"],
            **candlestick_colors  # Apply correct colors
        ))

        fig.update_layout(
            title=f"{ticker} Stock Price",
            xaxis_title="Time",
            yaxis_title="Price ($)",
            plot_bgcolor=theme["graph_bg"],  # Graph background
            paper_bgcolor=theme["graph_bg"],
            font=dict(color=theme["graph_text"]),  # Font color
            xaxis=dict(gridcolor="gray"),
            yaxis=dict(gridcolor="gray")
        )

        return price_text, fig

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return f"Error: {str(e)}", go.Figure()

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
