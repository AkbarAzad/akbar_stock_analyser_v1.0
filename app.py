import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import os
import numpy as np
from dash.dependencies import Output, Input

data = pd.DataFrame()
#for i in os.listdir():
#    if '_stock_yahoo.csv' in i:
#        df = pd.read_csv(i)
#        df['company'] = i[:-16]
#        data = pd.concat([data, df], axis = 0)
#data = data.reset_index(drop = True)
companies = ['amazon', 'singtel', 'starhub', 'keppel', 'singaporeairlines', 'genting', 'comfortdelgro']
for company in companies:
    df = pd.read_csv(company+'_stock_yahoo.csv')
    df['company'] = company
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
                    children = "Analyse stock data for Singtel"
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
                        id="open-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("close-chart", "figure"), Output("open-chart", "figure")],
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
    
    openChartFigure = {
        "data": [
            {
                "x": filteredData["date"],
                "y": filteredData["open"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Open Price",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    return closeChartFigure, openChartFigure
     
if __name__ == "__main__":
    app.run_server(debug=True)
    
