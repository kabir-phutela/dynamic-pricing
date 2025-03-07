from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Initialize Flask App
app = Flask(__name__)

# Load trained model, scaler, and encoder
model = joblib.load("dynamic_pricing_model.pkl")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")  # Load encoder for categorical variables

@app.route('/')
def home():
    return jsonify({"message": "Dynamic Pricing Model API is Running!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Print request data for debugging
        print("Received Data:", request.json)

        # Extract features from request
        data_dict = request.json['features']  # Expecting a dictionary

        # Define correct feature order
        correct_feature_order = ["Number_of_Drivers", "Number_of_Riders", "Location_Category",
                                 "Customer_Loyalty_Status", "Time_of_Booking", "Vehicle_Type",
                                 "Average_Ratings", "Expected_Ride_Duration",
                                 "Number_of_Past_Rides", "Supply_Demand_Ratio"]

        # Convert data dictionary to DataFrame
        df = pd.DataFrame([data_dict])

        # Ensure all required features are present
        missing_features = [col for col in correct_feature_order if col not in df.columns]
        if missing_features:
            return jsonify({"error": f"Missing features: {missing_features}"}), 400

        # Separate categorical & numerical features
        categorical_cols = ["Location_Category", "Customer_Loyalty_Status", "Time_of_Booking", "Vehicle_Type"]
        numerical_cols = ["Number_of_Drivers", "Number_of_Riders", "Average_Ratings",
                          "Expected_Ride_Duration", "Number_of_Past_Rides", "Supply_Demand_Ratio"]

        cat_data = df[categorical_cols]
        num_data = df[numerical_cols]

        # Transform categorical data using encoder
        encoded_categorical = encoder.transform(cat_data)
        encoded_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(categorical_cols))

        # Combine numerical and encoded categorical data
        final_df = pd.concat([num_data.reset_index(drop=True), encoded_df], axis=1)

        # **Ensure the order of features matches the training data**
        final_df = final_df[scaler.feature_names_in_]  # Fix column order

        # Debugging output
        print("Expected Feature Order:", scaler.feature_names_in_)
        print("Received Feature Order:", final_df.columns.tolist())

        # Scale numerical data
        final_scaled = scaler.transform(final_df)

        # Make prediction
        prediction = model.predict(final_scaled)

        # Return prediction result
        return jsonify({'predicted_price': round(prediction[0], 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
