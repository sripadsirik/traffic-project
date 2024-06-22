#import libraries neede
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

#load the processed data
df_traffic = pd.read_csv('processed_traffic_data.csv')


# Split the data into features (X) and target (y)
X = df_traffic.drop(columns=['timestamp', 'traffic_flow'])
y = df_traffic['traffic_flow']