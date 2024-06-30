import pandas as pd
import yfinance as yf
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go

tickers = {
    'Apple Inc.': 'AAPL', 'Microsoft Corporation': 'MSFT', 'Amazon.com Inc.': 'AMZN',
    'Alphabet Inc. (Google)': 'GOOGL', 'Facebook, Inc.': 'FB', 'Tesla, Inc.': 'TSLA',
    'Berkshire Hathaway Inc. (Class A)': 'BRK-A', 'Berkshire Hathaway Inc. (Class B)': 'BRK-B',
    'JPMorgan Chase & Co.': 'JPM', 'Johnson & Johnson': 'JNJ', 'Visa Inc.': 'V',
    'NVIDIA Corporation': 'NVDA', 'Procter & Gamble Co.': 'PG', 'Home Depot, Inc.': 'HD',
    'UnitedHealth Group Incorporated': 'UNH', 'PayPal Holdings, Inc.': 'PYPL', 'Mastercard Incorporated': 'MA',
    'The Walt Disney Company': 'DIS', 'Intel Corporation': 'INTC', 'Comcast Corporation': 'CMCSA',
    'Verizon Communications Inc.': 'VZ', 'Netflix, Inc.': 'NFLX', 'Adobe Inc.': 'ADBE',
    'PepsiCo, Inc.': 'PEP', 'The Coca-Cola Company': 'KO', 'Exxon Mobil Corporation': 'XOM',
    'Chevron Corporation': 'CVX', 'Abbott Laboratories': 'ABT', 'Merck & Co., Inc.': 'MRK',
    'Nike, Inc.': 'NKE', 'Cisco Systems, Inc.': 'CSCO', 'AT&T Inc.': 'T',
    'Pfizer Inc.': 'PFE', 'Walmart Inc.': 'WMT', 'AbbVie Inc.': 'ABBV', 'Bank of America Corporation': 'BAC',
    'Novartis AG': 'NVS', 'T-Mobile US, Inc.': 'TMUS', 'Salesforce.com, Inc.': 'CRM',
    'Medtronic plc': 'MDT', 'Accenture plc': 'ACN', 'Eli Lilly and Company': 'LLY',
    'Danaher Corporation': 'DHR', 'Texas Instruments Incorporated': 'TXN', 'McDonald\'s Corporation': 'MCD',
    'Amgen Inc.': 'AMGN', 'Broadcom Inc.': 'AVGO', 'Qualcomm Incorporated': 'QCOM', 'Union Pacific Corporation': 'UNP',
    'Honeywell International Inc.': 'HON', 'Costco Wholesale Corporation': 'COST', 'NextEra Energy, Inc.': 'NEE',
    'Philip Morris International Inc.': 'PM', 'Linde plc': 'LIN', 'Wells Fargo & Company': 'WFC',
    'Oracle Corporation': 'ORCL', 'Citigroup Inc.': 'C', 'Advanced Micro Devices, Inc.': 'AMD',
    'Bristol-Myers Squibb Company': 'BMY', 'United Parcel Service, Inc.': 'UPS', 'Lockheed Martin Corporation': 'LMT',
    'International Business Machines Corporation': 'IBM', 'Lowe\'s Companies, Inc.': 'LOW', 'Intuit Inc.': 'INTU',
    '3M Company': 'MMM', 'Goldman Sachs Group, Inc.': 'GS', 'Raytheon Technologies Corporation': 'RTX',
    'BlackRock, Inc.': 'BLK', 'Charter Communications, Inc.': 'CHTR', 'Caterpillar Inc.': 'CAT',
    'Anthem, Inc.': 'ANTM', 'Intuitive Surgical, Inc.': 'ISRG', 'Micron Technology, Inc.': 'MU',
    'CVS Health Corporation': 'CVS', 'S&P Global Inc.': 'SPGI', 'Thermo Fisher Scientific Inc.': 'TMO',
    'Cigna Corporation': 'CI', 'Simon Property Group, Inc.': 'SPG', 'Becton, Dickinson and Company': 'BDX',
    'ServiceNow, Inc.': 'NOW', 'Marsh & McLennan Companies, Inc.': 'MMC', 'Stryker Corporation': 'SYK',
    'Zoetis Inc.': 'ZTS', 'Target Corporation': 'TGT', 'American Express Company': 'AXP',
    'Duke Energy Corporation': 'DUK',
    'Fidelity National Information Services, Inc.': 'FIS', 'CME Group Inc.': 'CME', 'Prologis, Inc.': 'PLD',
    'Fiserv, Inc.': 'FISV', 'Southern Company': 'SO', 'Estée Lauder Companies Inc.': 'EL', 'EOG Resources, Inc.': 'EOG',
    'MetLife, Inc.': 'MET', 'Illinois Tool Works Inc.': 'ITW', 'Chubb Limited': 'CB', 'Toyota Motor Corporation': 'TM'
}

ticker_values = list(tickers.values())

data = yf.download(ticker_values, start="2021-01-01", end=pd.Timestamp("today").date())

# Initialize Dash app
external_stylesheets = [
    {'href': 'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap', 'rel': 'stylesheet'}]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Stock Market Analytics"

# Define app layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Stock Market Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Interactive stock market analytics with advanced charts and key metrics."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Ticker", className="menu-title"),
                        dcc.Dropdown(
                            id="ticker-dropdown",
                            options=[{"label": key, "value": value} for key, value in tickers.items()],
                            value=ticker_values[0],
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.index.min(),
                            max_date_allowed=data.index.max(),
                            start_date=pd.Timestamp("2024-01-01").date(),
                            end_date=data.index.max(),
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    id='price-chart-div',
                    children=dcc.Graph(id="price-chart"),
                    className="card",
                ),
                html.Div(
                    id='volume-chart-div',
                    children=dcc.Graph(id="volume-chart"),
                    className="card",
                ),
                html.Div(
                    id='candlestick-chart-div',
                    children=dcc.Graph(id="candlestick-chart"),
                    className="card",
                ),
                html.Div(
                    id='ohlc-bars-chart-div',
                    children=dcc.Graph(id="ohlc-bars-chart"),
                    className="card",
                ),
                html.Div(
                    id='profit-margin-chart-div',
                    children=dcc.Graph(id="profit-margin-chart"),
                    className="card",
                ),
                html.Div(
                    id='pe-ratio-chart-div',
                    children=dcc.Graph(id="pe-ratio-chart"),
                    className="card",
                ),
                html.Div(
                    id='bollinger-bands-chart-div',
                    children=dcc.Graph(id="bollinger-bands-chart"),
                    className="card",
                ),
                html.Div(
                    id='macd-chart-div',
                    children=dcc.Graph(id="macd-chart"),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


# Callback to update price chart
@app.callback(
    Output("price-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_price_chart(ticker, start_date, end_date):
    filtered_data = data.loc[start_date:end_date]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=filtered_data.index, y=filtered_data['Adj Close'][ticker], mode='lines', name='Adj Close'))
    fig.update_layout(title=f"Price Chart ({ticker})", xaxis_title="Date", yaxis_title="Price ($)")
    return fig


# Callback to update volume chart
@app.callback(
    Output("volume-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_volume_chart(ticker, start_date, end_date):
    filtered_data = data.loc[start_date:end_date]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data['Volume'][ticker], name='Volume', marker_color='blue'))
    fig.update_layout(title=f"Volume Chart ({ticker})", xaxis_title="Date", yaxis_title="Volume")
    return fig


# Callback to update candlestick chart
@app.callback(
    Output("candlestick-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_candlestick_chart(ticker, start_date, end_date):
    filtered_data = data.loc[start_date:end_date]
    fig = go.Figure(data=[go.Candlestick(x=filtered_data.index,
                                         open=filtered_data['Open'][ticker],
                                         high=filtered_data['High'][ticker],
                                         low=filtered_data['Low'][ticker],
                                         close=filtered_data['Close'][ticker])])
    fig.update_layout(title=f"Candlestick Chart ({ticker})", xaxis_title="Date", yaxis_title="Price ($)")
    return fig


# Callback to update OHLC bars chart
@app.callback(
    Output("ohlc-bars-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_ohlc_bars_chart(ticker, start_date, end_date):
    filtered_data = data.loc[start_date:end_date]
    fig = go.Figure(data=[go.Ohlc(x=filtered_data.index,
                                  open=filtered_data['Open'][ticker],
                                  high=filtered_data['High'][ticker],
                                  low=filtered_data['Low'][ticker],
                                  close=filtered_data['Close'][ticker])])
    fig.update_layout(title=f"OHLC Bars Chart ({ticker})", xaxis_title="Date", yaxis_title="Price ($)")
    return fig


# Callback to update P/E ratio chart
@app.callback(
    Output("pe-ratio-chart", "figure"),
    Input("ticker-dropdown", "value"),
)
def update_pe_ratio_chart(ticker):
    try:
        pe_ratio = data['Adj Close'][ticker].iloc[-1] / data['Close'][ticker].iloc[
            -1]  # Simplified P/E ratio calculation
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=pe_ratio,
            title="P/E Ratio",
            number={'prefix': "P/E Ratio: "},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        return fig
    except Exception as e:
        return {}


# Callback to update profit margin chart
@app.callback(
    Output("profit-margin-chart", "figure"),
    Input("ticker-dropdown", "value"),
)
def update_profit_margin_chart(ticker):
    try:
        profit_margin = (data['Close'][ticker].iloc[-1] - data['Open'][ticker].iloc[-1]) / data['Open'][ticker].iloc[
            -1] * 100  # Simplified profit margin calculation
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=profit_margin,
            title="Profit Margin (%)",
            number={'suffix': "%"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        return fig
    except Exception as e:
        return {}


# Callback to update Bollinger Bands chart
@app.callback(
    Output("bollinger-bands-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_bollinger_bands_chart(ticker, start_date, end_date):
    try:
        filtered_data = data.loc[start_date:end_date]
        upper_band, middle_band, lower_band = filtered_data['Close'][ticker].rolling(window=20).mean(), \
            filtered_data['Close'][ticker].rolling(window=20).mean() - 2 * \
            filtered_data['Close'][ticker].rolling(window=20).std(), \
            filtered_data['Close'][ticker].rolling(window=20).mean() + 2 * \
            filtered_data['Close'][ticker].rolling(window=20).std()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['Close'][ticker], mode='lines', name='Close'))
        fig.add_trace(go.Scatter(x=filtered_data.index, y=upper_band, mode='lines', name='Upper Band'))
        fig.add_trace(go.Scatter(x=filtered_data.index, y=middle_band, mode='lines', name='Middle Band'))
        fig.add_trace(go.Scatter(x=filtered_data.index, y=lower_band, mode='lines', name='Lower Band'))
        fig.update_layout(title=f"Bollinger Bands ({ticker})", xaxis_title="Date", yaxis_title="Price ($)")
        return fig
    except Exception as e:
        return {}


# Callback to update MACD chart
@app.callback(
    Output("macd-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_macd_chart(ticker, start_date, end_date):
    try:
        filtered_data = data.loc[start_date:end_date]
        macd = filtered_data['Close'][ticker].ewm(span=12, adjust=False).mean() - filtered_data['Close'][ticker].ewm(
            span=26, adjust=False).mean()
        signal = macd.ewm(span=9, adjust=False).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data.index, y=macd, mode='lines', name='MACD'))
        fig.add_trace(go.Scatter(x=filtered_data.index, y=signal, mode='lines', name='Signal'))
        fig.update_layout(title=f"MACD ({ticker})", xaxis_title="Date", yaxis_title="MACD")
        return fig
    except Exception as e:
        return {}


# Run the app
if __name__ == "__main__":
    app.run_server()
