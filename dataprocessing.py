import pandas as pd
from sqlalchemy import create_engine

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

    # Handling Missing Values
    # Check for missing values
    missing_values = df_traffic.isnull().sum()
    print("\nMissing Values:")
    print(missing_values)

    # Drop rows with missing values (if needed)
    df_traffic.dropna(inplace=True)

    # Impute missing values (if needed)
    # Example: impute missing numerical values with mean
    df_traffic.fillna(df_traffic.mean(), inplace=True)

    # Display the updated DataFrame after handling missing values
    print("\nDataFrame after handling missing values:")
    print(df_traffic.head(10))

except Exception as e:
    print("Error:", e)