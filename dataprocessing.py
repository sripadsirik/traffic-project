import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler

# PostgreSQL database setup
db_url = 'postgresql://postgres:Indianman1$$$@localhost:5432/traffic_data'
engine = create_engine(db_url)

# Connect to the database and retrieve the data
try:
    # Query to select all columns from the historic_traffic_data table
    query = "SELECT * FROM historic_traffic_data"

    # Read data from the database into a pandas DataFrame
    df_traffic = pd.read_sql(query, con=engine)

    # Display the number of rows in the DataFrame
    print("Number of rows loaded into DataFrame:", df_traffic.shape[0])

    # Display the first few rows of the DataFrame to inspect the data
    print(df_traffic.head(10))

    # Perform data cleaning and preprocessing here

except Exception as e:
    print("Error:", e)

# Check for missing values
missing_values = df_traffic.isnull().sum()
print("\nMissing Values:\n", missing_values)

# Handle missing values if necessary (for example, filling or dropping)
df_traffic = df_traffic.dropna()

# Normalize the traffic_flow column
scaler = MinMaxScaler()
df_traffic['traffic_flow_normalized'] = scaler.fit_transform(df_traffic[['traffic_flow']])

# Feature Engineering: Extract time-based features
df_traffic['timestamp'] = pd.to_datetime(df_traffic['timestamp'])
df_traffic['hour'] = df_traffic['timestamp'].dt.hour
df_traffic['day_of_week'] = df_traffic['timestamp'].dt.dayofweek
df_traffic['month'] = df_traffic['timestamp'].dt.month

# Feature Engineering: One-hot encode the weather_condition
df_traffic = pd.get_dummies(df_traffic, columns=['weather_condition'])

# Add lag features (e.g., traffic flow 15, 30, 45 minutes ago)
df_traffic['traffic_flow_lag_1'] = df_traffic['traffic_flow'].shift(1)
df_traffic['traffic_flow_lag_2'] = df_traffic['traffic_flow'].shift(2)
df_traffic['traffic_flow_lag_3'] = df_traffic['traffic_flow'].shift(3)

# Add rolling window features (e.g., average traffic flow over the past hour)
df_traffic['traffic_flow_roll_mean_4'] = df_traffic['traffic_flow'].rolling(window=4).mean()
df_traffic['traffic_flow_roll_std_4'] = df_traffic['traffic_flow'].rolling(window=4).std()

# Drop rows with NaN values introduced by lag and rolling window features
df_traffic = df_traffic.dropna()

# Add interaction features (e.g., interaction between traffic flow and weather conditions)
df_traffic['traffic_flow_Clear'] = df_traffic['traffic_flow'] * df_traffic['weather_condition_Clear']
df_traffic['traffic_flow_Rain'] = df_traffic['traffic_flow'] * df_traffic['weather_condition_Rain']
df_traffic['traffic_flow_Snow'] = df_traffic['traffic_flow'] * df_traffic['weather_condition_Snow']
df_traffic['traffic_flow_Fog'] = df_traffic['traffic_flow'] * df_traffic['weather_condition_Fog']

# Display the DataFrame after feature engineering
print("\nDataFrame after feature engineering:\n", df_traffic.head(10))


# Save the processed DataFrame to a CSV file for model training
df_traffic.to_csv('processed_traffic_data.csv', index=False)
print("Data processing and feature engineering complete. Processed data saved to 'processed_traffic_data.csv'.")