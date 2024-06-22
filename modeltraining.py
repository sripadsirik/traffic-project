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

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Example of making a prediction on new data
new_data = X_test.iloc[0].values.reshape(1, -1)
predicted_traffic_flow = model.predict(new_data)
print(f"Predicted Traffic Flow: {predicted_traffic_flow[0]}")