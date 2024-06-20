import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from datetime import datetime

# PostgreSQL database setup
db_url = 'postgresql://postgres:Indianman1$$$@localhost:5432/traffic_data'
engine = create_engine(db_url)

# Connect to the database and retrieve the data
try:
    # Query to select all columns from the historic_traffic_data table
    query = "SELECT * FROM historic_traffic_data"

    # Read data from the database into a pandas DataFrame
    df_traffic = pd.read_sql(query, con=engine)

    # Handle missing values (if any)
    df_traffic = df_traffic.dropna()

    # Normalize the 'traffic_flow' column
    scaler = MinMaxScaler()
    df_traffic['traffic_flow_normalized'] = scaler.fit_transform(df_traffic[['traffic_flow']])

    # Extract timestamp features
    df_traffic['timestamp'] = pd.to_datetime(df_traffic['timestamp'])
    df_traffic['hour'] = df_traffic['timestamp'].apply(lambda x: x.hour)
    df_traffic['day_of_week'] = df_traffic['timestamp'].apply(lambda x: x.dayofweek)
    df_traffic['month'] = df_traffic['timestamp'].apply(lambda x: x.month)

    # One-hot encode the 'weather_condition' column
    encoder = OneHotEncoder(sparse_output=False)
    weather_encoded = encoder.fit_transform(df_traffic[['weather_condition']])
    weather_encoded_df = pd.DataFrame(weather_encoded, columns=encoder.get_feature_names_out(['weather_condition']))

    # Concatenate the original DataFrame with the encoded weather DataFrame
    df_traffic = pd.concat([df_traffic, weather_encoded_df], axis=1)

    # Display the DataFrame after feature engineering
    print("\nDataFrame after feature engineering:")
    print(df_traffic.head(10))

except Exception as e:
    print("Error:", e)
