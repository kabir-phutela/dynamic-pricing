import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
file_path = "dynamic_pricing.csv"  # Ensure correct file path
df = pd.read_csv(file_path)

# Step 1: Feature Engineering - Create adjusted_ride_cost based on demand & supply
df["Supply_Demand_Ratio"] = df["Number_of_Drivers"] / df["Number_of_Riders"]
df["adjusted_ride_cost"] = df["Historical_Cost_of_Ride"] * (1 + (1 - df["Supply_Demand_Ratio"]))

# Step 2: Encoding categorical features using OneHotEncoder
categorical_cols = ["Location_Category", "Customer_Loyalty_Status", "Time_of_Booking", "Vehicle_Type"]
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output =False)
encoded_features = encoder.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_cols))

# Drop original categorical columns and merge encoded features
df = df.drop(columns=categorical_cols).reset_index(drop=True)
df = pd.concat([df, encoded_df], axis=1)

# Step 3: Selecting Features & Target
X = df.drop(columns=["Historical_Cost_of_Ride", "adjusted_ride_cost"])
y = df["adjusted_ride_cost"]

# Step 4: Scaling Numerical Features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 6: Model Training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 7: Model Evaluation
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Step 8: Save Model, Scaler, and Encoder for Deployment
joblib.dump(model, "dynamic_pricing_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(encoder, "encoder.pkl")  # Save OneHotEncoder

print("✅ Model, Scaler, and Encoder saved successfully!")
