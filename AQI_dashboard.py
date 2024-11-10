import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
df = pd.read_csv("annual_aqi_by_cbsa_2023.csv")


# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout for the dashboard
app.layout = html.Div([
    html.H1("Global Air Quality Snapshot - 2024"),
    
    # Dropdown for selecting PM level to display
    html.Label("Select Particulate Matter to Display:"),
    dcc.Dropdown(
        id="pollutant-dropdown",
        options=[
            {"label": "PM2.5", "value": "PM2.5"},
            {"label": "PM10", "value": "PM10"}
        ],
        value="PM2.5",
        clearable=False
    ),
    
    # Map for visualizing PM levels
    dcc.Graph(id="map-plot"),
    
    # Bar chart for comparing PM levels across cities
    dcc.Graph(id="bar-plot")
])

# Define callback to update both plots based on selected pollutant
@app.callback(
    [Output("map-plot", "figure"),
     Output("bar-plot", "figure")],
    [Input("pollutant-dropdown", "value")]
)
def update_plots(selected_pollutant):
    # Filter dataset based on the selected pollutant (PM2.5 or PM10)
    fig_map = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        hover_data={selected_pollutant: True, "Latitude": False, "Longitude": False},
        color=selected_pollutant,
        color_continuous_scale="YlOrRd",
        size=selected_pollutant,
        size_max=15,
        zoom=1,
        mapbox_style="carto-positron"
    )
    fig_map.update_layout(title=f"{selected_pollutant} Levels Across Cities")
    
    # Bar chart to compare PM levels across cities
    fig_bar = px.bar(
        df,
        x="City",
        y=selected_pollutant,
        color=selected_pollutant,
        color_continuous_scale="YlOrRd",
        title=f"{selected_pollutant} Levels in Major Cities"
    )
    fig_bar.update_layout(xaxis_title="City", yaxis_title=f"{selected_pollutant} Level (µg/m³)")
    
    return fig_map, fig_bar

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
