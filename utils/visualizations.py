import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_prediction_charts(prediction_record):
    """Create various charts for prediction analysis"""
    data = prediction_record['input_data']
    prediction = prediction_record['prediction']
    
    # Factor impact chart
    factors = {
        'Distance': data['distance_km'].iloc[0],
        'Prep Time': data['prep_time_min'].iloc[0],
        'Age': data['Delivery_person_Age'].iloc[0],
        'Rating': data['Delivery_person_Ratings'].iloc[0],
        'Multiple Deliveries': data['multiple_deliveries'].iloc[0],
        'Vehicle Condition': data['Vehicle_condition'].iloc[0]
    }
    
    # Normalize factors for visualization
    normalized_factors = {}
    for key, value in factors.items():
        if key == 'Distance':
            normalized_factors[key] = min(value / 30.0, 1.0) * 100
        elif key == 'Prep Time':
            normalized_factors[key] = min(value / 60.0, 1.0) * 100
        elif key == 'Age':
            normalized_factors[key] = min(value / 60.0, 1.0) * 100
        elif key == 'Rating':
            normalized_factors[key] = (value / 5.0) * 100
        elif key == 'Multiple Deliveries':
            normalized_factors[key] = min(value / 4.0, 1.0) * 100
        elif key == 'Vehicle Condition':
            normalized_factors[key] = (value / 2.0) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(normalized_factors.keys()),
        y=list(normalized_factors.values()),
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
        text=[f"{v:.1f}%" for v in normalized_factors.values()],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Factor Impact on Delivery Time",
        xaxis_title="Factors",
        yaxis_title="Impact Level (%)",
        template="plotly_white",
        height=400
    )
    
    return {'factor_impact': fig}

def create_factor_analysis(data):
    """Create factor analysis visualization"""
    # Create a radar chart for categorical factors
    categories = ['Weather', 'Traffic', 'Order Type', 'Vehicle Type', 'City', 'Festival']
    
    # Map categorical values to scores
    weather_scores = {'sunny': 5, 'cloudy': 4, 'windy': 3, 'stormy': 2, 'sandstorms': 1, 'fog': 2}
    traffic_scores = {'low': 5, 'medium': 3, 'high': 2, 'jam': 1}
    order_scores = {'snack': 5, 'drinks': 4, 'meal': 3, 'buffet': 2}
    vehicle_scores = {'bicycle': 2, 'electric bike': 3, 'scooter': 4, 'motorcycle': 5}
    city_scores = {'semi-urban': 5, 'urban': 3, 'metropolitan': 2}
    festival_scores = {'no': 5, 'yes': 2}

    
    values = [
        weather_scores.get(data['Weatherconditions'].iloc[0], 3),
        traffic_scores.get(data['Road_traffic_density'].iloc[0], 3),
        order_scores.get(data['Type_of_order'].iloc[0], 3),
        vehicle_scores.get(data['Type_of_vehicle'].iloc[0], 3),
        city_scores.get(data['City'].iloc[0], 3),
        festival_scores.get(data['Festival'].iloc[0], 3)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Order',
        line_color='#FF6B6B'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="Order Characteristics Analysis",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_batch_analysis_chart(batch_results):
    """Create analysis charts for batch processing results"""
    if batch_results is None or batch_results.empty:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Prediction Distribution', 'Distance vs Time', 'Weather Impact', 'Traffic Impact'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "box"}, {"type": "box"}]]
    )
    
    # Prediction distribution
    fig.add_trace(
        go.Histogram(x=batch_results['Predicted_Delivery_Time'], name='Predictions'),
        row=1, col=1
    )
    
    # Distance vs Time scatter
    fig.add_trace(
        go.Scatter(
            x=batch_results['distance_km'],
            y=batch_results['Predicted_Delivery_Time'],
            mode='markers',
            name='Distance vs Time',
            marker=dict(color='#4ECDC4')
        ),
        row=1, col=2
    )
    
    # Weather impact
    fig.add_trace(
        go.Box(
            x=batch_results['Weatherconditions'],
            y=batch_results['Predicted_Delivery_Time'],
            name='Weather Impact'
        ),
        row=2, col=1
    )
    
    # Traffic impact
    fig.add_trace(
        go.Box(
            x=batch_results['Road_traffic_density'],
            y=batch_results['Predicted_Delivery_Time'],
            name='Traffic Impact'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        template="plotly_white",
        title_text="Batch Processing Analysis"
    )
    
    return fig

def create_time_series_chart(history_data):
    """Create time series chart for prediction history"""
    if not history_data:
        return None
    
    timestamps = [record['timestamp'] for record in history_data]
    predictions = [record['prediction'] for record in history_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=predictions,
        mode='lines+markers',
        name='Predictions',
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Prediction History Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Predicted Delivery Time (minutes)",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_comparison_chart(scenarios):
    """Create comparison chart for multiple scenarios"""
    if not scenarios or len(scenarios) < 2:
        return None
    
    scenario_names = [f"Scenario {i+1}" for i in range(len(scenarios))]
    predictions = [scenario['prediction'] for scenario in scenarios]
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=predictions,
        marker_color=colors[:len(scenarios)],
        text=[f"{p:.1f} min" for p in predictions],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Scenario Comparison",
        xaxis_title="Scenarios",
        yaxis_title="Predicted Delivery Time (minutes)",
        template="plotly_white",
        height=400
    )
    
    return fig
