import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_csv("formatted_data.csv")

df["date"] = pd.to_datetime(df["date"])

# Group by date and sum sales
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# Sort by date just to be safe
daily_sales = daily_sales.sort_values("date")

# Create a line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)

# Add vertical line for price change on 15 Jan 2021
fig.add_vline(x="2021-01-15", line_dash="dash", line_color="red",
              annotation_text="Price Increase", annotation_position="top left")

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
