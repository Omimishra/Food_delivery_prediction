import joblib
import pandas as pd
import numpy as np
import streamlit as st

def load_models():
    """Load the trained models and preprocessors"""
    try:
        encoder = joblib.load("encoder.pkl")
        scaler = joblib.load("scaler.pkl")
        model = joblib.load("rf_model.pkl")
        return encoder, scaler, model
    except FileNotFoundError as e:
        raise Exception(f"Model file not found: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading models: {str(e)}")

def prepare_input_data(input_data, encoder, scaler):
    """Prepare input data for prediction"""
    # Column lists as used during training
    num_cols = [
        "Delivery_person_Age",
        "Delivery_person_Ratings",
        "Vehicle_condition",
        "multiple_deliveries",
        "distance_km",
        "prep_time_min",
        "order_hour",
        "order_day",
        "is_weekend"
    ]
    
    cat_cols = [
        "Weatherconditions",
        "Road_traffic_density",
        "Type_of_order",
        "Type_of_vehicle",
        "Festival",
        "City"
    ]
    

    # Normalize categorical values to lowercase
    for col in cat_cols:
        input_data[col] = input_data[col].astype(str).str.lower().str.strip()

    # Encode categorical features
    encoded_data = encoder.transform(input_data[cat_cols])
    if hasattr(encoded_data, "toarray"):
        encoded_data = encoded_data.toarray()
    
    # Scale numeric features
    scaled_num = scaler.transform(input_data[num_cols])
    
    # Concatenate features
    final_input = np.hstack((scaled_num, encoded_data))
    
    return final_input

def make_prediction(model, final_input):
    """Make prediction using the trained model"""
    prediction = model.predict(final_input)[0]
    return prediction

def validate_input_data(data):
    """Validate input data for common issues"""
    issues = []
    
    # Check for missing values
    if data.isnull().any().any():
        issues.append("Missing values detected")
    
    # Check reasonable ranges
    if data['distance_km'].iloc[0] < 0 or data['distance_km'].iloc[0] > 25:
        issues.append("Distance cannot be negative")
    
    if data['prep_time_min'].iloc[0] < 0 or data['prep_time_min'].iloc[0] > 20:
        issues.append("Preparation time cannot be negative")
    
    if data['Delivery_person_Age'].iloc[0] < 21 or data['Delivery_person_Age'].iloc[0] > 50:
        issues.append("Delivery person age seems unrealistic")
    
    return issues

def process_batch_data(uploaded_file, encoder, scaler, model):
    """Process batch data for multiple predictions"""
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        required_columns = [
            "Delivery_person_Age", "Delivery_person_Ratings", "Weatherconditions",
            "Road_traffic_density", "Vehicle_condition", "Type_of_order",
            "Type_of_vehicle", "multiple_deliveries", "Festival", "City",
            "distance_km", "prep_time_min", "order_hour", "order_day", "is_weekend"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        # Process each row
        predictions = []
        for idx, row in df.iterrows():
            try:
                row_data = pd.DataFrame([row])
                final_input = prepare_input_data(row_data, encoder, scaler)
                prediction = make_prediction(model, final_input)
                predictions.append(prediction)
            except Exception as e:
                predictions.append(f"Error: {str(e)}")
        
        # Add predictions to dataframe
        df['Predicted_Delivery_Time'] = predictions
        
        return df
        
    except Exception as e:
        raise Exception(f"Error processing batch data: {str(e)}")

def create_sample_batch_data():
    """Create sample data for batch processing"""
    sample_data = {
        'Delivery_person_Age': [25, 30, 35, 28, 32],
        'Delivery_person_Ratings': [4.5, 4.2, 4.8, 4.1, 4.6],
        'Weatherconditions': ['Sunny', 'Cloudy', 'Stormy', 'Windy', 'Sunny'],
        'Road_traffic_density': ['Medium', 'Low', 'High', 'Medium', 'Low'],
        'Vehicle_condition': [1, 2, 1, 2, 1],
        'Type_of_order': ['Meal', 'Snack', 'Drinks', 'Meal', 'Buffet'],
        'Type_of_vehicle': ['Motorcycle', 'Scooter', 'Bicycle', 'Motorcycle', 'Electric Bike'],
        'multiple_deliveries': [0, 1, 0, 2, 1],
        'Festival': ['No', 'Yes', 'No', 'No', 'Yes'],
        'City': ['Metropolitan', 'Urban', 'Semi-Urban', 'Metropolitan', 'Urban'],
        'distance_km': [5.2, 3.8, 7.1, 4.5, 6.3],
        'prep_time_min': [20, 15, 25, 18, 30],
        'order_hour': [12, 19, 13, 20, 14],
        'order_day': [15, 16, 17, 18, 19],
        'is_weekend': [0, 1, 0, 1, 0]
    }
    
    return pd.DataFrame(sample_data)
