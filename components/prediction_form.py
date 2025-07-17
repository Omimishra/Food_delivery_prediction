import streamlit as st
import pandas as pd

def render_prediction_form():
    """Render the prediction form and return input data"""
    
    st.markdown("### 📝 Enter Delivery Details")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Delivery Person")
        age = st.slider("Age", 21, 50, 30, help="Age of the delivery person")
        rating = st.slider("Rating", 0.0, 5.0, 4.5, step=0.1, help="Average rating of the delivery person")
        
        st.markdown("#### 🌤️ Environment")
        weather = st.selectbox("Weather Conditions", 
                              ["Sunny", "Stormy", "Sandstorms", "Windy", "Cloudy", "Fog"],
                              help="Current weather conditions")
        traffic = st.selectbox("Road Traffic", 
                              ["Low", "Medium", "High", "Jam"],
                              help="Traffic density on the route")
        
        st.markdown("#### 🚗 Vehicle")
        vehicle_condition = st.slider("Vehicle Condition", 0, 2, 1, 
                                    help="0=Poor, 1=Average, 2=Good")
        vehicle_type = st.selectbox("Vehicle Type", 
                                  ["Motorcycle", "Scooter", "Electric Bike", "Bicycle"],
                                  help="Type of delivery vehicle")
    
    with col2:
        st.markdown("#### 🍕 Order Details")
        order_type = st.selectbox("Order Type", 
                                 ["Snack", "Meal", "Drinks", "Buffet"],
                                 help="Type of food order")
        prep_time = st.slider("Food Preparation Time (min)", 5, 20, 10,
                             help="Time needed to prepare the food")
        
        st.markdown("#### 📍 Location & Logistics")
        city = st.selectbox("City Type", 
                           ["Metropolitan", "Urban", "Semi-Urban"],
                           help="Type of city area")
        distance = st.slider("Distance (km)", 1.0, 25.0, 5.0,
                           help="Distance from restaurant to delivery location")
        multi_deliveries = st.slider("Multiple Deliveries", 0, 4, 0,
                                   help="Number of other deliveries in the same trip")
        
        st.markdown("#### 📅 Timing")
        festival = st.selectbox("Festival Season", ["Yes", "No"],
                               help="Is it festival season?")
        hour = st.slider("Order Hour (24h format)", 7, 23, 13,
                        help="Hour when the order was placed")
        day = st.slider("Day of Week", 0, 6, 3,
                       help="Day of week")
        is_weekend = st.radio("Weekend?", [0, 1], 
                             format_func=lambda x: "Yes" if x == 1 else "No",
                             help="Is it a weekend?")
    
    # Create input DataFrame
    input_data = pd.DataFrame([[
        age, rating, weather, traffic, vehicle_condition, order_type, vehicle_type,
        multi_deliveries, festival, city, distance, prep_time, hour, day, is_weekend
    ]], columns=[
        "Delivery_person_Age", "Delivery_person_Ratings", "Weatherconditions", "Road_traffic_density",
        "Vehicle_condition", "Type_of_order", "Type_of_vehicle", "multiple_deliveries",
        "Festival", "City", "distance_km", "prep_time_min", "order_hour", "order_day", "is_weekend"
    ])
    
    # Show input summary
    with st.expander("📋 Input Summary", expanded=False):
        st.write("Current input values:")
        summary_data = {
            "Parameter": ["Distance", "Prep Time", "Weather", "Traffic", "Vehicle", "City"],
            "Value": [f"{distance} km", f"{prep_time} min", weather, traffic, vehicle_type, city]
        }
        st.table(pd.DataFrame(summary_data))
    
    return input_data

def render_quick_presets():
    """Render quick preset buttons for common scenarios"""
    st.markdown("### ⚡ Quick Presets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏃‍♂️ Rush Hour"):
            return get_preset_data("rush_hour")
    
    with col2:
        if st.button("🌅 Morning Order"):
            return get_preset_data("morning")
    
    with col3:
        if st.button("🌧️ Bad Weather"):
            return get_preset_data("bad_weather")
    
    return None

def get_preset_data(preset_type):
    """Get preset data for different scenarios"""
    presets = {
        "rush_hour": {
            "Delivery_person_Age": 28,
            "Delivery_person_Ratings": 4.3,
            "Weatherconditions": "Cloudy",
            "Road_traffic_density": "High",
            "Vehicle_condition": 1,
            "Type_of_order": "Meal",
            "Type_of_vehicle": "Motorcycle",
            "multiple_deliveries": 1,
            "Festival": "No",
            "City": "Metropolitan",
            "distance_km": 8.5,
            "prep_time_min": 25,
            "order_hour": 19,
            "order_day": 1,
            "is_weekend": 0
        },
        "morning": {
            "Delivery_person_Age": 25,
            "Delivery_person_Ratings": 4.6,
            "Weatherconditions": "Sunny",
            "Road_traffic_density": "Low",
            "Vehicle_condition": 2,
            "Type_of_order": "Snack",
            "Type_of_vehicle": "Scooter",
            "multiple_deliveries": 0,
            "Festival": "No",
            "City": "Urban",
            "distance_km": 3.2,
            "prep_time_min": 15,
            "order_hour": 10,
            "order_day": 4,
            "is_weekend": 0
        },
        "bad_weather": {
            "Delivery_person_Age": 32,
            "Delivery_person_Ratings": 4.4,
            "Weatherconditions": "Stormy",
            "Road_traffic_density": "Medium",
            "Vehicle_condition": 1,
            "Type_of_order": "Meal",
            "Type_of_vehicle": "Motorcycle",
            "multiple_deliveries": 0,
            "Festival": "No",
            "City": "Metropolitan",
            "distance_km": 6.8,
            "prep_time_min": 20,
            "order_hour": 14,
            "order_day": 5,
            "is_weekend": 1
        }
    }
    
    data = presets.get(preset_type, presets["rush_hour"])
    return pd.DataFrame([data])
