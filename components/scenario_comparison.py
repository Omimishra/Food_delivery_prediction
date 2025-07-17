import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_handler import prepare_input_data, make_prediction
from utils.analytics import calculate_confidence_interval, generate_prediction_insights

def render_scenario_comparison(encoder, scaler, model):
    """Render scenario comparison tool"""
    
    st.markdown("### 🔄 Scenario Comparison")
    st.markdown("Compare different delivery scenarios side by side to optimize your decisions")
    
    # Initialize session state for scenarios
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []
    
    # Quick preset scenarios
    st.markdown("#### ⚡ Quick Scenario Presets")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏃‍♂️ Rush Hour", key="rush_scenario"):
            add_preset_scenario("rush_hour")
    
    with col2:
        if st.button("🌅 Morning", key="morning_scenario"):
            add_preset_scenario("morning")
    
    with col3:
        if st.button("🌧️ Bad Weather", key="weather_scenario"):
            add_preset_scenario("bad_weather")
    
    with col4:
        if st.button("🎉 Festival", key="festival_scenario"):
            add_preset_scenario("festival")
    
    # Create custom scenario
    st.markdown("#### 🎯 Create Custom Scenario")
    
    with st.expander("➕ Add New Scenario", expanded=False):
        scenario_name = st.text_input("Scenario Name", placeholder="e.g., Lunch Rush")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Delivery Person Age", 21, 50, 30, key="scenario_age")
            rating = st.slider("Delivery Person Rating", 1.0, 5.0, 4.5, step=0.1, key="scenario_rating")
            weather = st.selectbox("Weather", ["Sunny", "Stormy", "Sandstorms", "Windy", "Cloudy", "Fog"], key="scenario_weather")
            traffic = st.selectbox("Traffic", ["Low", "Medium", "High", "Jam"], key="scenario_traffic")
            vehicle_condition = st.slider("Vehicle Condition", 0, 2, 1, key="scenario_vehicle_condition")
            
        with col2:
            order_type = st.selectbox("Order Type", ["Snack", "Meal", "Drinks", "Buffet"], key="scenario_order_type")
            vehicle_type = st.selectbox("Vehicle Type", ["Motorcycle", "Scooter", "Electric Bike", "Bicycle"], key="scenario_vehicle_type")
            distance = st.slider("Distance (km)", 1.0, 25.0, 5.0, key="scenario_distance")
            prep_time = st.slider("Prep Time (min)", 5, 20, 10, key="scenario_prep_time")
            hour = st.slider("Order Hour", 7, 23, 13, key="scenario_hour")
        
        col3, col4 = st.columns(2)
        with col3:
            city = st.selectbox("City", ["Metropolitan", "Urban", "Semi-Urban"], key="scenario_city")
            multi_deliveries = st.slider("Multiple Deliveries", 0, 4, 0, key="scenario_multi")
        
        with col4:
            festival = st.selectbox("Festival", ["Yes", "No"], key="scenario_festival")
            day = st.slider("Day of Week", 0, 6, 3, key="scenario_day")
            is_weekend = st.radio("Weekend?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", key="scenario_weekend")
        
        if st.button("➕ Add Scenario", type="primary"):
            if scenario_name:
                scenario_data = create_scenario_data(
                    scenario_name, age, rating, weather, traffic, vehicle_condition,
                    order_type, vehicle_type, distance, prep_time, hour, city,
                    multi_deliveries, festival, day, is_weekend
                )
                
                # Make prediction
                final_input = prepare_input_data(scenario_data['data'], encoder, scaler)
                prediction = make_prediction(model, final_input)
                confidence = calculate_confidence_interval(model, final_input)
                
                scenario_data['prediction'] = prediction
                scenario_data['confidence'] = confidence
                
                st.session_state.scenarios.append(scenario_data)
                st.success(f"✅ Added scenario: {scenario_name}")
                st.rerun()
    
    # Display scenarios
    if st.session_state.scenarios:
        # Ensure all scenarios have predictions
        for scenario in st.session_state.scenarios:
            if scenario['prediction'] is None:
                try:
                    final_input = prepare_input_data(scenario['data'], encoder, scaler)
                    prediction = make_prediction(model, final_input)
                    confidence = calculate_confidence_interval(model, final_input)
                    scenario['prediction'] = prediction
                    scenario['confidence'] = confidence
                except Exception as e:
                    st.error(f"Error predicting scenario {scenario['name']}: {str(e)}")
        
        st.markdown("#### 📊 Scenario Comparison Results")
        
        # Scenario cards
        display_scenario_cards(st.session_state.scenarios)
        
        # Comparison chart
        st.markdown("#### 📈 Visual Comparison")
        comparison_chart = create_scenario_comparison_chart(st.session_state.scenarios)
        st.plotly_chart(comparison_chart, use_container_width=True)
        
        # Detailed analysis
        st.markdown("#### 🔍 Detailed Analysis")
        analysis_chart = create_detailed_analysis_chart(st.session_state.scenarios)
        st.plotly_chart(analysis_chart, use_container_width=True)
        
        # Recommendations
        st.markdown("#### 💡 Recommendations")
        display_recommendations(st.session_state.scenarios)
        
        # Clear scenarios
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear All", type="secondary"):
                st.session_state.scenarios = []
                st.rerun()
    
    else:
        st.info("No scenarios created yet. Add some scenarios to start comparing!")

def create_scenario_data(name, age, rating, weather, traffic, vehicle_condition, 
                        order_type, vehicle_type, distance, prep_time, hour, 
                        city, multi_deliveries, festival, day, is_weekend):
    """Create scenario data structure with standardized lowercase strings"""
    
    # Lowercase string inputs to match label-encoded training data
    weather = weather.lower()
    traffic = traffic.lower()
    order_type = order_type.lower()
    vehicle_type = vehicle_type.lower()
    festival = festival.lower()
    city = city.lower()
    
    data = pd.DataFrame([[ 
        age, rating, weather, traffic, vehicle_condition, order_type, vehicle_type,
        multi_deliveries, festival, city, distance, prep_time, hour, day, is_weekend
    ]], columns=[ 
        "Delivery_person_Age", "Delivery_person_Ratings", "Weatherconditions", "Road_traffic_density",
        "Vehicle_condition", "Type_of_order", "Type_of_vehicle", "multiple_deliveries",
        "Festival", "City", "distance_km", "prep_time_min", "order_hour", "order_day", "is_weekend"
    ])
    
    return {
        'name': name,
        'data': data,
        'prediction': None,
        'confidence': None
    }


def add_preset_scenario(preset_type):
    """Add preset scenario to comparison"""
    # Import at function level to avoid circular imports
    from utils.data_handler import prepare_input_data, make_prediction
    from utils.analytics import calculate_confidence_interval
    
    presets = {
        "rush_hour": {
            "name": "Rush Hour",
            "age": 28, "rating": 4.3, "weather": "Cloudy", "traffic": "High",
            "vehicle_condition": 1, "order_type": "Meal", "vehicle_type": "Motorcycle",
            "distance": 8.5, "prep_time": 25, "hour": 19, "city": "Metropolitan",
            "multi_deliveries": 1, "festival": "No", "day": 1, "is_weekend": 0
        },
        "morning": {
            "name": "Morning Order",
            "age": 25, "rating": 4.6, "weather": "Sunny", "traffic": "Low",
            "vehicle_condition": 2, "order_type": "Snack", "vehicle_type": "Scooter",
            "distance": 3.2, "prep_time": 15, "hour": 10, "city": "Urban",
            "multi_deliveries": 0, "festival": "No", "day": 5, "is_weekend": 0
        },
        "bad_weather": {
            "name": "Bad Weather",
            "age": 32, "rating": 4.4, "weather": "Stormy", "traffic": "Medium",
            "vehicle_condition": 1, "order_type": "Meal", "vehicle_type": "Motorcycle",
            "distance": 6.8, "prep_time": 20, "hour": 14, "city": "Metropolitan",
            "multi_deliveries": 0, "festival": "No", "day": 3, "is_weekend": 1
        },
        "festival": {
            "name": "Festival Rush",
            "age": 30, "rating": 4.2, "weather": "Sunny", "traffic": "Jam",
            "vehicle_condition": 1, "order_type": "Buffet", "vehicle_type": "Scooter",
            "distance": 7.5, "prep_time": 35, "hour": 20, "city": "Metropolitan",
            "multi_deliveries": 2, "festival": "Yes", "day": 2, "is_weekend": 1
        }
    }
    
    preset = presets.get(preset_type, presets["rush_hour"])
    scenario_data = create_scenario_data(**preset)
    
    # Skip adding if already exists
    existing_names = [s['name'] for s in st.session_state.scenarios]
    if scenario_data['name'] not in existing_names:
        st.session_state.scenarios.append(scenario_data)

def display_scenario_cards(scenarios):
    """Display scenario cards"""
    
    cols = st.columns(min(len(scenarios), 3))
    
    for i, scenario in enumerate(scenarios):
        with cols[i % 3]:
            # Create gradient color based on prediction
            if scenario['prediction']:
                if scenario['prediction'] < 25:
                    color = "#10B981"  # Green
                elif scenario['prediction'] < 35:
                    color = "#F59E0B"  # Yellow
                else:
                    color = "#EF4444"  # Red
            else:
                color = "#6B7280"  # Gray
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}15 0%, {color}25 100%);
                border-left: 4px solid {color};
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                backdrop-filter: blur(10px);
            ">
                <h4 style="color: {color}; margin: 0 0 0.5rem 0; font-size: 1.2rem;">
                    {scenario['name']}
                </h4>
                <div style="color: white; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    {scenario['prediction']:.1f} min
                </div>
                <div style="color: #A0AEC0; font-size: 0.9rem;">
                    Distance: {scenario['data']['distance_km'].iloc[0]:.1f} km | 
                    Weather: {scenario['data']['Weatherconditions'].iloc[0]}
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_scenario_comparison_chart(scenarios):
    """Create comparison chart for scenarios"""
    
    scenario_names = [s['name'] for s in scenarios]
    predictions = [s['prediction'] for s in scenarios]
    confidence_lower = [s['confidence'][0] for s in scenarios]
    confidence_upper = [s['confidence'][1] for s in scenarios]
    
    fig = go.Figure()
    
    # Add confidence intervals
    fig.add_trace(go.Scatter(
        x=scenario_names,
        y=confidence_upper,
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False,
        name='Upper Confidence'
    ))
    
    fig.add_trace(go.Scatter(
        x=scenario_names,
        y=confidence_lower,
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        name='Confidence Interval',
        fillcolor='rgba(124, 58, 237, 0.2)'
    ))
    
    # Add predictions
    colors = ['#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4']
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=predictions,
        marker_color=colors[:len(scenarios)],
        name='Predicted Time',
        text=[f"{p:.1f} min" for p in predictions],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Scenario Comparison - Delivery Time Predictions",
        xaxis_title="Scenarios",
        yaxis_title="Delivery Time (minutes)",
        template="plotly_dark",
        height=500,
        showlegend=True
    )
    
    return fig

def create_detailed_analysis_chart(scenarios):
    """Create detailed analysis chart"""
    
    # Extract data for analysis
    scenario_names = [s['name'] for s in scenarios]
    distances = [s['data']['distance_km'].iloc[0] for s in scenarios]
    prep_times = [s['data']['prep_time_min'].iloc[0] for s in scenarios]
    predictions = [s['prediction'] for s in scenarios]
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Distance vs Prediction', 'Prep Time vs Prediction'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    colors = ['#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4']
    
    # Distance vs Prediction
    fig.add_trace(
        go.Scatter(
            x=distances,
            y=predictions,
            mode='markers+text',
            text=scenario_names,
            textposition='top center',
            marker=dict(size=12, color=colors[:len(scenarios)]),
            name='Distance Impact'
        ),
        row=1, col=1
    )
    
    # Prep Time vs Prediction
    fig.add_trace(
        go.Scatter(
            x=prep_times,
            y=predictions,
            mode='markers+text',
            text=scenario_names,
            textposition='top center',
            marker=dict(size=12, color=colors[:len(scenarios)]),
            name='Prep Time Impact'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Distance (km)", row=1, col=1)
    fig.update_xaxes(title_text="Prep Time (min)", row=1, col=2)
    fig.update_yaxes(title_text="Delivery Time (min)", row=1, col=1)
    fig.update_yaxes(title_text="Delivery Time (min)", row=1, col=2)
    
    return fig

def display_recommendations(scenarios):
    """Display recommendations based on scenarios"""
    
    if not scenarios:
        return
    
    # Find best and worst scenarios
    best_scenario = min(scenarios, key=lambda x: x['prediction'])
    worst_scenario = max(scenarios, key=lambda x: x['prediction'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #10B98115 0%, #10B98125 100%);
            border-left: 4px solid #10B981;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #10B981; margin: 0 0 0.5rem 0;">
                🏆 Best Scenario
            </h4>
            <div style="color: white; font-size: 1.5rem; font-weight: 600;">
                {best_scenario['name']}
            </div>
            <div style="color: #A0AEC0; font-size: 0.9rem; margin-top: 0.5rem;">
                Predicted Time: {best_scenario['prediction']:.1f} minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #EF444415 0%, #EF444425 100%);
            border-left: 4px solid #EF4444;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #EF4444; margin: 0 0 0.5rem 0;">
                ⚠️ Worst Scenario
            </h4>
            <div style="color: white; font-size: 1.5rem; font-weight: 600;">
                {worst_scenario['name']}
            </div>
            <div style="color: #A0AEC0; font-size: 0.9rem; margin-top: 0.5rem;">
                Predicted Time: {worst_scenario['prediction']:.1f} minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key insights
    st.markdown("#### 🔍 Key Insights")
    
    avg_prediction = sum(s['prediction'] for s in scenarios) / len(scenarios)
    time_diff = worst_scenario['prediction'] - best_scenario['prediction']
    
    insights = [
        f"Average delivery time across scenarios: {avg_prediction:.1f} minutes",
        f"Time difference between best and worst: {time_diff:.1f} minutes",
        f"Best conditions: {best_scenario['data']['Weatherconditions'].iloc[0]} weather, {best_scenario['data']['Road_traffic_density'].iloc[0]} traffic",
        f"Avoid: {worst_scenario['data']['Weatherconditions'].iloc[0]} weather with {worst_scenario['data']['Road_traffic_density'].iloc[0]} traffic"
    ]
    
    for insight in insights:
        st.info(f"💡 {insight}")