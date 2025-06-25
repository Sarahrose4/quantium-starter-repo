import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

DATA_DIRECTORY = "./data"
file_list = [os.path.join(DATA_DIRECTORY, f) for f in os.listdir(DATA_DIRECTORY) if f.endswith(".csv")]
df_list = [pd.read_csv(f) for f in file_list]
df = pd.concat(df_list, ignore_index=True)

df = df[df["product"].str.lower() == "pink morsel"]
df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)
df["sales"] = df["quantity"] * df["price"]
df["date"] = pd.to_datetime(df["date"])
df["region"] = df["region"].str.lower()

app = dash.Dash(__name__)
app.title = "Soul Foods Pink Morsel Sales Visualiser"


styles = {
    "container": {
        "maxWidth": "900px",
        "margin": "auto",
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "padding": "20px",
        "backgroundColor": "#f9f9f9",
        "borderRadius": "10px",
        "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
    },
    "header": {
        "textAlign": "center",
        "color": "#2c3e50",
        "marginBottom": "30px",
        "fontWeight": "700",
    },
    "radio": {
        "display": "flex",
        "justifyContent": "center",
        "marginBottom": "30px",
        "fontWeight": "600",
        "color": "#34495e",
        "gap": "20px"
    }
}


app.layout = html.Div(style=styles["container"], children=[
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style=styles["header"]),

    dcc.RadioItems(
        id="region-selector",
        options=[
            {"label": "All", "value": "all"},
            {"label": "North", "value": "north"},
            {"label": "East", "value": "east"},
            {"label": "South", "value": "south"},
            {"label": "West", "value": "west"},
        ],
        value="all",
        labelStyle={"display": "inline-block"},
        style=styles["radio"]
    ),

    dcc.Graph(id="sales-line-chart")
])


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-selector", "value")
)
def update_line_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    daily_sales = filtered_df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top left"
    )

    fig.update_layout(
        plot_bgcolor="#ffffff",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=80, b=40),
        font=dict(family="Segoe UI", size=14, color="#2c3e50")
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

