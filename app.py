# app.py (Streamlit Frontend)
import streamlit as st
import requests

# Set page title
st.title("Vegetable and Fruit Price Predictor")

# Input form for collecting data from user
st.subheader("Enter the following details:")

# Input fields
month = st.slider("Month", 1, 12)
day_of_week = st.slider("Day of Week (0=Monday, 6=Sunday)", 0, 6)
farmprice = st.number_input("Farm Price", min_value=0.0, step=0.01)
atlantaretail = st.number_input("Atlanta Retail Price", min_value=0.0, step=0.01)
chicagoretail = st.number_input("Chicago Retail Price", min_value=0.0, step=0.01)
losangelesretail = st.number_input("Los Angeles Retail Price", min_value=0.0, step=0.01)
newyorkretail = st.number_input("New York Retail Price", min_value=0.0, step=0.01)
averagespread = st.number_input("Average Spread", min_value=0.0, step=0.01)

# Button to trigger prediction
if st.button("Predict Price"):
    # Prepare data for API request
    data = {
        'month': month,
        'day_of_week': day_of_week,
        'farmprice': farmprice,
        'atlantaretail': atlantaretail,
        'chicagoretail': chicagoretail,
        'losangelesretail': losangelesretail,
        'newyorkretail': newyorkretail,
        'averagespread': averagespread
    }
    
    # Send the data to the Django API endpoint
    try:
        response = requests.post("http://localhost:8000/api/predict_price/", json=data)

        if response.status_code == 200:
            predicted_price = response.json()['predicted_price']
            st.write(f"Predicted Price: ${predicted_price:.2f}")
        else:
            st.error("Error in prediction. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {e}")
