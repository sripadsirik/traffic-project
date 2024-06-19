import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

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

# Simulate real-time traffic data
def get_real_time_traffic_data(api_key):
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': 'Chicago, IL',  # Example origin
        'destination': 'New York, NY',  # Example destination
        'key': api_key,
        'departure_time': 'now',
        'traffic_model': 'best_guess',  # or 'pessimistic', 'optimistic'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

real_time_data = get_real_time_traffic_data('AIzaSyD035l7OlCdc42zYBnb9eoT86rhx_r_6gM')
print(real_time_data)

# Simulate weather data
def get_weather_data():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=city&appid=your_api_key")
    data = response.json()
    weather_condition = data['weather'][0]['main']
    return weather_condition

# Real-time data simulation
# Uncomment the following lines if you have access to real APIs
# real_time_traffic_data = get_real_time_traffic_data()
# current_weather = get_weather_data()
