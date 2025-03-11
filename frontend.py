import streamlit as st
import requests

# Set the title of the web app
st.title("🚖 Dynamic Pricing Prediction")

# User inputs for features
num_drivers = st.number_input("Number of Drivers", min_value=1, value=10)
num_riders = st.number_input("Number of Riders", min_value=1, value=30)
location_category = st.selectbox("Location Category", ["Urban", "Suburban", "Rural"])
customer_loyalty = st.selectbox("Customer Loyalty Status", ["Silver", "Gold", "Bronze"])
time_of_booking = st.selectbox("Time of Booking", ["Morning", "Afternoon", "Night"])
vehicle_type = st.selectbox("Vehicle Type", ["SUV", "Sedan", "Hatchback"])
average_ratings = st.slider("Average Ratings", 1.0, 5.0, 4.5)
expected_duration = st.number_input("Expected Ride Duration (mins)", min_value=1, value=45)
past_rides = st.number_input("Number of Past Rides", min_value=0, value=10)
supply_demand_ratio = st.number_input("Supply-Demand Ratio", min_value=0.1, value=1.2)

# API URL (Update if deployed on AWS)
api_url = "https://dynamic-pricing-server2.onrender/predict"

# Button to make prediction
if st.button("Predict Price"):
    # Create JSON payload
    payload = {
        "features": {
            "Number_of_Drivers": num_drivers,
            "Number_of_Riders": num_riders,
            "Location_Category": location_category,
            "Customer_Loyalty_Status": customer_loyalty,
            "Time_of_Booking": time_of_booking,
            "Vehicle_Type": vehicle_type,
            "Average_Ratings": average_ratings,
            "Expected_Ride_Duration": expected_duration,
            "Number_of_Past_Rides": past_rides,
            "Supply_Demand_Ratio": supply_demand_ratio
        }
    }

      # Send request to API
    try:
        response = requests.post(api_url, json=payload)

        # Debugging: Print API response details
        st.write("Response Status Code:", response.status_code)
        st.write("Raw Response Text:", response.text)

        # Check if response is valid JSON
        result = response.json()
        if response.status_code == 200:
            st.success(f"Predicted Ride Price: ${result['predicted_price']:.2f}")
        else:
            st.error(f"Error: {result.get('error', 'Unknown error')}")

    except requests.exceptions.JSONDecodeError:
        st.error("Error: Invalid JSON response from API. Check backend logs.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request Failed: {str(e)}")
