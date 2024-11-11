import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


excel_file = pd.ExcelFile("who_ambient_air_quality_database_version_2024_(v6.1).xlsx")  
print(excel_file.sheet_names) #opening the excel doc, see what the tabs are called so i can refer to the one with data


#reading only the 'Update 2024 (V6.1)''tab
df = pd.read_excel("who_ambient_air_quality_database_version_2024_(v6.1).xlsx", sheet_name="Update 2024 (V6.1)")
print(df.columns)  # Inspect the labels of the columns

df = df.dropna(subset=["pm10_concentration", "pm25_concentration", "no2_concentration"])
#this removes rows where data is missing, in either pm10 or pm25 or no2_concentration

#plotting the map for pm10 concentrations for cities in dataset
def scatter_mapbox(df):
    """
    Generates an interactive scatter map displaying air quality data across various cities.

    Parameters:
    df (DataFrame): A pandas DataFrame containing air quality data for cities. 
                    Expected columns include:
                    - 'latitude' (float): The latitude of each city.
                    - 'longitude' (float): The longitude of each city.
                    - 'pm10_concentration' (float): pm10 pollutant concentration for each city.
                    - 'pm25_concentration' (float, optional): pm25 pollutant concentration for each city.

    Returns:
    Figure: A Plotly figure object representing an interactive map where city points are sized 
            and colored according to pm10 levels. The map includes tooltips that display the 
            pm10 and, if available, pm2.5 values for each city.

    Notes:
    - The color of each city point on the map is proportional to its pm10 value, with higher 
      concentrations appearing in a more intense color.
    - The size of each city point reflects the magnitude of PM10 levels, making higher 
      concentrations more visually prominent.
    - The map uses Mapbox's "carto-positron" style for a clean, grayscale background.
    """
    fig_pm10 = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="pm10_concentration",  # or "PM2.5" for PM2.5 levels
            size="pm10_concentration",   # Adjust the size based on pollutant level
            hover_name="city",
            hover_data={"pm10_concentration": True, "latitude": False, "longitude": False},
            color_continuous_scale="sunset",
            title="Air Quality Snapshot - PM10 Levels Across Cities",
            zoom=1,
    )
    fig_pm10.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    return fig_pm10     

fig_pm10 = scatter_mapbox(df)
fig_pm10.show()

#doing the same for pm2.5 concentrations
def scatter_mapbox_pm25(df):
    fig_pm25 = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="pm25_concentration",  # or "PM2.5" for PM2.5 levels
            size="pm25_concentration",   # Adjust the size based on pollutant level
            hover_name="city",
            hover_data={"pm25_concentration": True, "latitude": False, "longitude": False},
            color_continuous_scale="sunset",
            title="Air Quality Snapshot - PM2.5 Levels Across Cities",
            zoom=1,
    )
    fig_pm25.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    return fig_pm25     

fig_pm25 = scatter_mapbox_pm25(df)
fig_pm25.show() 

#and lastly for no2_concentrations
def scatter_mapbox_no2(df):
    fig_no2 = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="no2_concentration",  # or "PM2.5" for PM2.5 levels
            size="no2_concentration",   # Adjust the size based on pollutant level
            hover_name="city",
            hover_data={"no2_concentration": True, "latitude": False, "longitude": False},
            color_continuous_scale="sunset",
            title="Air Quality Snapshot - NO_2 concentrations across cities",
            zoom=1,
    )
    fig_no2.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    return fig_no2     

fig_no2 = scatter_mapbox_no2(df)
fig_no2.show()  

#top 10 cities of highest pollutant concentration 
avg_pollution_by_country = df.groupby('city')[['pm10_concentration', 'pm25_concentration', 'no2_concentration']].mean()

# Sorting the data by each pollutant to get the most polluted countries
top_polluted_pm10 = avg_pollution_by_country['pm10_concentration'].sort_values(ascending=False).head(10)  # Top 10 countries by PM10
top_polluted_pm25 = avg_pollution_by_country['pm25_concentration'].sort_values(ascending=False).head(10)  # Top 10 countries by PM2.5
top_polluted_no2 = avg_pollution_by_country['no2_concentration'].sort_values(ascending=False).head(10)  # Top 10 countries by NO2

# Create a bar graph for each pollutant (PM10, PM2.5, and NO2)
fig_pm10 = px.bar(top_polluted_pm10, x=top_polluted_pm10.index, y=top_polluted_pm10.values,
                  title="Top 10 cities with the highest pm10 concentration",
                  labels={'x': 'country', 'y': 'average pm10 concentration'},
                  color=top_polluted_pm10.values, color_continuous_scale='sunset')

fig_pm25 = px.bar(top_polluted_pm25, x=top_polluted_pm25.index, y=top_polluted_pm25.values,
                  title="top 10 cities with the highest pm2.5 concentration",
                  labels={'x': 'country', 'y': 'average pm2.5 concentration'},
                  color=top_polluted_pm25.values, color_continuous_scale='sunset')

fig_no2 = px.bar(top_polluted_no2, x=top_polluted_no2.index, y=top_polluted_no2.values,
                 title="top 10 cities with the highest no2 concentration",
                 labels={'x': 'Country', 'y': 'average no2 concentration'},
                 color=top_polluted_no2.values, color_continuous_scale='sunset')

# Show the figures
fig_pm10.show()
fig_pm25.show()
fig_no2.show()

