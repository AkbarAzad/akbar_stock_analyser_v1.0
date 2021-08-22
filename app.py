import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import os
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.linear_model import Ridge

data = pd.DataFrame()
dataMA = pd.DataFrame()
#for i in os.listdir():
#    if '_stock_yahoo.csv' in i:
#        df = pd.read_csv(i)
#        df['company'] = i[:-16]
#        data = pd.concat([data, df], axis = 0)
#data = data.reset_index(drop = True)
companies = ['amazon', 'singtel', 'starhub', 'keppel', 'singaporeairlines', 'genting']
for company in companies:
    df = pd.read_csv(company+'_stock_yahoo.csv')
    df['company'] = company
    df['normalised'] = df['close'].apply(lambda x: x/df['close'][0])
    df.dropna(subset=['close'], inplace=True)
    closeList = df["close"].tolist()
    lagCloseList = closeList[:-1]
    lagCloseList.insert(0, 1)
    returnsList = [((x-y)/y)*100 for (x, y) in zip(closeList, lagCloseList)]
    returnsList[0] = 0
    df['returns'] = returnsList
    df["date"] = pd.to_datetime(df["date"], format = "%Y-%m-%d")
    df.sort_values("date", ascending = True, inplace=True)
    df['ma'] = df['close'].rolling(21).mean()
    n = 1
    #df['target'] = df[['close']].shift(-n) # Create target variable for prediction
    df = df.iloc[:-1] # Remove last row due to NULL value in target
    #sc = MinMaxScaler(feature_range = (0,1))
    #dfScaled = sc.fit_transform(df[['close', 'volume', 'target']]) # keep close, volume, target
    # Create Feature and Target
   # X = dfScaled[:, :2]
    #Y = dfScaled[:,2:]
    # Split into train and test sets
  #  split = int(0.65 * len(X))
    #X_train, Y_train, X_test, Y_test = X[:split], Y[:split], X[split:], Y[split:] 
    #regression_model = Ridge() # Create ridge regression model
    #regression_model.fit(X_train, Y_train)
   # lr_accuracy = regression_model.score(X_test, Y_test) # Model evaluation
    #df['accuracy'] = lr_accuracy
   # predicted_prices = regression_model.predict(X) # Make predictions
    predicted = []
  #  for i in predicted_prices: # Store predictions in list
   #     predicted.append(i[0])
    close = [] # Store scaled close prices in list
 #   for i in dfScaled:
  #      close.append(i[0])
    #df['closeScaled'] = close
    #df['closePredicted'] = predicted
    data = pd.concat([data, df], axis = 0)
data = data.reset_index(drop = True)
data["date"] = pd.to_datetime(data["date"], format = "%Y-%m-%d")
data.sort_values("date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }
]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server
app.title = "Akbar Analytics: Understand Your Stocks!"
app.layout = html.Div(
    children = [
        html.Div(
            children=[
                html.H1(
                    children="Akbar Analytics",
                    className="header-title",
                ),
                html.P(
                    children = "Analyse selected stock data"
                    " taken from Yahoo",
                    className = "header-description",
                ),
            ],
            className = "header",
        ),
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.Div(children="Company", className = "menu-title"),
                        dcc.Dropdown(
                            id = "company-filter",
                            options = [
                                {"label": company, "value": company}
                                for company in np.sort(data.company.unique())
                            ],
                            value = "singtel",
                        clearable = False,
                        className = "dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children = [
                        html.Div(
                            children = "Date Range",
                            className = "menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.date.min().date(),
                            max_date_allowed=data.date.max().date(),
                            start_date=data.date.min().date(),
                            end_date=data.date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children = dcc.Graph(
                        id="close-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="normalised-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="histogram-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="returns-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="ma-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="ridge-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("close-chart", "figure"), Output("normalised-chart", "figure"), Output("histogram-chart", "figure"), Output("returns-chart", "figure"), Output("ma-chart", "figure"), Output("ridge-chart", "figure")],
    [
        Input("company-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)

def updateCharts(company, start_date, end_date):
    mask = (
        (data.company == company)
        & (data.date >= start_date)
        & (data.date <= end_date)
    )
    filteredData = data.loc[mask, :]
    closeChartFigure = {
        "data": [
            {
                "x": filteredData["date"],
                "y": filteredData["close"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Close Price",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    
    normalisedChartFigure = {
        "data": [
            {
                "x": filteredData["date"],
                "y": filteredData["normalised"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Normalised Price",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    
    #histogramChartFigure = {
    #    "data": [
    #        {
    #            "x": filteredData["close"],
    #            "type": "histogram",
    #        },
    #    ],
    #    "layout": {
    #        "title": {
    #            "text": "Distribution of Close Price",
    #            "x": 0.05,
    #            "xanchor": "left",
    #        },
    #        "xaxis": {"fixedrange": True},
    #        "colorway": ["#2CA02C"],
    #    },
    #}
    
    histogramChartFigure = px.histogram(filteredData["close"])
    histogramChartFigure.update_layout(
        title_text="Distribution of Close Price",
        xaxis_title_text="Close",
        yaxis_title_text="Count",
        bargap=0.2
    )
    
    returnsChartFigure = {
        "data": [
            {
                "x": filteredData["date"],
                "y": filteredData["returns"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}%<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Daily Returns",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#990099"],
        },
    }
    
    maChartFigure = px.line(x = filteredData['date'], y = filteredData['close'], title = ' Original Stock Price vs. 21-days Moving Average change')
    maChartFigure.add_scatter(x = filteredData['date'], y = filteredData['ma'], name = '21-days moving average')
    
    ridgeChartFigure = px.line(x = filteredData['date'], y = filteredData['close'], title = "Original Scaled Close Price vs Prediction")
    ridgeChartFigure.add_scatter(x = filteredData['date'], y = filteredData['ma'], name = 'Predictions')

    return closeChartFigure, normalisedChartFigure, histogramChartFigure, returnsChartFigure, maChartFigure, ridgeChartFigure
     
if __name__ == "__main__":
    app.run_server(debug=True)
    
