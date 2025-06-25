import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load and concatenate data
df1 = pd.read_csv("/Users/sarahabiassaf/quantium-starter-repo/data/daily_sales_data_0.csv")
df2 = pd.read_csv("/Users/sarahabiassaf/quantium-starter-repo/data/daily_sales_data_1.csv")
df3 = pd.read_csv("/Users/sarahabiassaf/quantium-starter-repo/data/daily_sales_data_2.csv")

df = pd.concat([df1, df2, df3])

# Filter for pink morsel product
df = df[df["product"] == "pink morsel"]

# Convert price from $ string to float
df["price"] = df["price"].str.replace('$', '', regex=False).astype(float)

# Convert quantity to numeric
df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce')

# Calculate sales
df["sales"] = df["quantity"] * df["price"]

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# ---- DASH APP ----

app = dash.Dash(__name__)

# Layout with region dropdown
app.layout = html.Div(children=[
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    html.Label("Select Region:", style={"margin": "10px"}),
    dcc.Dropdown(
        id="region-picker",
        options=[{"label": region, "value": region} for region in df["region"].unique()],
        value=df["region"].unique()[0],  # default selected region
        clearable=False,
        style={"width": "300px", "margin": "0 auto 20px"}
    ),

    dcc.Graph(id="sales-line-chart")
])

# Callback to update graph based on selected region
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-picker", "value")
)
def update_chart(selected_region):
    # Filter by selected region
    filtered_df = df[df["region"] == selected_region]

    # Group and sum sales by date
    daily_sales = filtered_df.groupby("date", as_index=False)["sales"].sum()

    # Create line chart
    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales in {selected_region}",
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )

    # Add vertical line for price increase
    price_increase_date = pd.to_datetime("2021-01-15")

    fig.update_layout(
        shapes=[
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=price_increase_date,
                x1=price_increase_date,
                y0=0,
                y1=1,
                line=dict(color="red", dash="dash")
            )
        ],
        annotations=[
            dict(
                x=price_increase_date,
                y=1,
                xref="x",
                yref="paper",
                text="Price Increase",
                showarrow=False,
                xanchor="left",
                yanchor="bottom",
                font=dict(color="red")
            )
        ]
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
