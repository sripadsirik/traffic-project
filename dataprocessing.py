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

    # Check for missing values
    print("\nMissing Values:")
    print(df_traffic.isnull().sum())

    # Handle missing values (if any)
    df_traffic = df_traffic.dropna()

    # Display the DataFrame after handling missing values
    print("\nDataFrame after handling missing values:")
    print(df_traffic.head(10))

    # Normalize the 'traffic_flow' column
    scaler = MinMaxScaler()
    df_traffic['traffic_flow_normalized'] = scaler.fit_transform(df_traffic[['traffic_flow']])

    # Display the DataFrame after normalization
    print("\nDataFrame after normalization:")
    print(df_traffic.head(10))

except Exception as e:
    print("Error:", e)
