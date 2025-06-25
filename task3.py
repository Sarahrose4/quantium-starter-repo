import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df1 = pd.read_csv("daily_sales_data_0.csv")
df2 = pd.read_csv("daily_sales_data_1.csv")
df3 = pd.read_csv("daily_sales_data_2.csv")

df = pd.concat([df1, df2, df3])
df = df[df["product"] == "pink morsel"]
df["sales"] = df["quantity"] * df["price"]
df = df[["sales", "date", "region"]]


df["date"] = pd.to_datetime(df["date"])

daily_sales = df.groupby("date", as_index=False)["sales"].sum()

daily_sales = daily_sales.sort_values("date")

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)

fig.add_vline(x="2021-01-15", line_dash="dash", line_color="red",
              annotation_text="Price Increase", annotation_position="top left")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
