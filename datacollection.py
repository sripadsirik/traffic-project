import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import osmnx as ox

# PostgreSQL database setup
db_url = 'postgresql://postgres:Indianman1$$$@localhost:5432/traffic_data'
engine = create_engine(db_url)

# Test database connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))  # Use the text function
        print("Database connection successful.")
except Exception as e:
    print("Failed to connect to the database.")
    print(e)

# Simulate historical traffic data
def generate_historical_traffic_data():
    data = []
    current_time = datetime.now()
    for i in range(1000):
        timestamp = current_time - timedelta(minutes=i * 15)
        traffic_flow = np.random.randint(50, 200)  # Simulate traffic flow
        weather_condition = np.random.choice(['Clear', 'Rain', 'Snow', 'Fog'])
        data.append([timestamp, traffic_flow, weather_condition])
    df = pd.DataFrame(data, columns=['timestamp', 'traffic_flow', 'weather_condition'])
    return df

historical_traffic_data = generate_historical_traffic_data()

# Print the number of rows in the DataFrame
print(f"Number of rows in the DataFrame: {len(historical_traffic_data)}")

try:
    historical_traffic_data.to_sql('historic_traffic_data', engine, if_exists='replace', index=False)
    print("Historical traffic data stored in the database.")
except Exception as e:
    print("Failed to write to the database.")
    print(e)

# Simulate real-time traffic data using OSM
def get_real_time_traffic_data():
    origin = (41.8781, -87.6298)  # Chicago coordinates (latitude, longitude)
    destination = (40.7128, -74.0060)  # New York coordinates (latitude, longitude)
    graph = ox.graph_from_point(origin, dist=1000, network_type='drive')
    origin_node = ox.distance.nearest_nodes(graph, origin[1], origin[0])
    destination_node = ox.distance.nearest_nodes(graph, destination[1], destination[0])
    route = ox.routing.shortest_path(graph, origin_node, destination_node, weight='length')
    return graph, route

graph, real_time_data = get_real_time_traffic_data()
print(f"Shortest path: {real_time_data}")

# Simulate weather data
def get_weather_data(api_key, city_name, latitude, longitude):
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"
    response = requests.get(base_url)
    data = response.json()

    try:
        weather_condition = data['current']['condition']['text']
        return weather_condition
    except KeyError:
        print(f"Error: Weather data not found for {city_name}.")
        print("Full API response:", data)
        return None

# Replace 'your_api_key' with your actual WeatherAPI.com API key
api_key = 'a80d16ef322a4f1a804234739241906'

# Chicago coordinates (latitude, longitude)
chicago_lat, chicago_lon = 41.8781, -87.6298
chicago_weather = get_weather_data(api_key, 'Chicago', chicago_lat, chicago_lon)

if chicago_weather:
    print(f"Current weather condition in Chicago: {chicago_weather}")

# New York coordinates (latitude, longitude)
ny_lat, ny_lon = 40.7128, -74.0060
ny_weather = get_weather_data(api_key, 'New York', ny_lat, ny_lon)

if ny_weather:
    print(f"Current weather condition in New York: {ny_weather}")

# Simulate traffic flow based on weather conditions
def adjust_traffic_flow(traffic_flow, weather_condition):
    if weather_condition == 'Rain':
        traffic_flow *= 0.9
    elif weather_condition == 'Snow':
        traffic_flow *= 0.7
    elif weather_condition == 'Fog':
        traffic_flow *= 0.8
    return int(traffic_flow)

# Adjust traffic flow in historical data based on weather conditions
historical_traffic_data['adjusted_traffic_flow'] = historical_traffic_data.apply(
    lambda row: adjust_traffic_flow(row['traffic_flow'], row['weather_condition']), axis=1
)

# Print the adjusted historical traffic data
print("Adjusted historical traffic data:")
print(historical_traffic_data.head())
