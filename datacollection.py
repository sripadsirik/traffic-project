import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

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
print(historical_traffic_data.head())

# Simulate real-time traffic data
def get_real_time_traffic_data():
    # In a real scenario, fetch data from an API
    response = requests.get("https://api.example.com/real-time-traffic")
    data = response.json()
    df = pd.DataFrame(data)
    return df

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
