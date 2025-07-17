import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.visualizations import create_time_series_chart, create_comparison_chart
from utils.analytics import calculate_delivery_statistics, analyze_prediction_trends

def render_dashboard():
    """Render the analytics dashboard"""
    
    st.markdown("### 📈 Analytics Dashboard")
    
    # Check if we have data
    if not st.session_state.prediction_history:
        st.info("No prediction data available yet. Make some predictions to see analytics!")
        return
    
    # Calculate statistics
    stats = calculate_delivery_statistics(st.session_state.prediction_history)
    trends = analyze_prediction_trends(st.session_state.prediction_history)
    
    # Key metrics
    st.markdown("#### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Predictions", 
            stats['total_predictions'],
            help="Total number of predictions made"
        )
    
    with col2:
        st.metric(
            "Average Time", 
            f"{stats['average_time']:.1f} min",
            help="Average predicted delivery time"
        )
    
    with col3:
        st.metric(
            "Fastest Delivery", 
            f"{stats['min_time']:.1f} min",
            help="Shortest predicted delivery time"
        )
    
    with col4:
        st.metric(
            "Slowest Delivery", 
            f"{stats['max_time']:.1f} min",
            help="Longest predicted delivery time"
        )
    
    # Time series chart
    st.markdown("#### 📈 Prediction Trends")
    time_series_chart = create_time_series_chart(st.session_state.prediction_history)
    if time_series_chart:
        st.plotly_chart(time_series_chart, use_container_width=True)
    
    # Analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Delivery Performance")
        render_performance_analysis(stats)
    
    with col2:
        st.markdown("#### 🔍 Pattern Analysis")
        render_pattern_analysis()
    
    # Detailed analytics
    st.markdown("#### 📊 Detailed Analytics")
    render_detailed_analytics()

def render_performance_analysis(stats):
    """Render performance analysis section"""
    
    # Performance gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = stats['average_time'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Average Delivery Time"},
        delta = {'reference': 25},  # Reference: 25 minutes
        gauge = {
            'axis': {'range': [None, 60]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': "lightgray"},
                {'range': [20, 40], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance insights
    if stats['average_time'] < 25:
        st.success("🎉 Excellent performance! Average delivery time is below 25 minutes.")
    elif stats['average_time'] < 35:
        st.warning("⚠️ Good performance, but room for improvement.")
    else:
        st.error("🚨 Performance needs attention. Average delivery time is high.")

def render_pattern_analysis():
    """Render pattern analysis section"""
    
    # Extract patterns from history
    history_data = st.session_state.prediction_history
    
    # Weather pattern analysis
    weather_data = {}
    distance_data = []
    time_data = []
    
    for record in history_data:
        weather = record['input_data']['Weatherconditions'].iloc[0]
        distance = record['input_data']['distance_km'].iloc[0]
        prediction = record['prediction']
        
        if weather not in weather_data:
            weather_data[weather] = []
        weather_data[weather].append(prediction)
        
        distance_data.append(distance)
        time_data.append(prediction)
    
    # Weather impact chart
    if weather_data:
        weather_df = pd.DataFrame([
            {'Weather': weather, 'Avg_Time': sum(times)/len(times)}
            for weather, times in weather_data.items()
        ])
        
        fig = px.bar(
            weather_df, 
            x='Weather', 
            y='Avg_Time',
            title='Average Delivery Time by Weather',
            color='Avg_Time',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Distance vs Time correlation
    if len(distance_data) > 1:
        fig = px.scatter(
            x=distance_data, 
            y=time_data,
            title='Distance vs Delivery Time',
            labels={'x': 'Distance (km)', 'y': 'Delivery Time (min)'},
            trendline='ols'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def render_detailed_analytics():
    """Render detailed analytics section"""
    
    # Tabs for different analysis types
    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "🔗 Correlations", "📈 Trends"])
    
    with tab1:
        render_distribution_analysis()
    
    with tab2:
        render_correlation_analysis()
    
    with tab3:
        render_trend_analysis()

def render_distribution_analysis():
    """Render distribution analysis"""
    
    history_data = st.session_state.prediction_history
    predictions = [record['prediction'] for record in history_data]
    
    # Distribution histogram
    fig = px.histogram(
        x=predictions,
        nbins=20,
        title='Distribution of Predicted Delivery Times',
        labels={'x': 'Delivery Time (minutes)', 'y': 'Frequency'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Box plot for outlier detection
    fig = px.box(
        y=predictions,
        title='Delivery Time Distribution (Box Plot)',
        labels={'y': 'Delivery Time (minutes)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def render_correlation_analysis():
    """Render correlation analysis"""
    
    history_data = st.session_state.prediction_history
    
    # Extract features for correlation analysis
    features_data = []
    for record in history_data:
        features = {
            'Prediction': record['prediction'],
            'Distance': record['input_data']['distance_km'].iloc[0],
            'Prep_Time': record['input_data']['prep_time_min'].iloc[0],
            'Age': record['input_data']['Delivery_person_Age'].iloc[0],
            'Rating': record['input_data']['Delivery_person_Ratings'].iloc[0],
            'Vehicle_Condition': record['input_data']['Vehicle_condition'].iloc[0],
            'Multiple_Deliveries': record['input_data']['multiple_deliveries'].iloc[0],
            'Hour': record['input_data']['order_hour'].iloc[0],
            'Is_Weekend': record['input_data']['is_weekend'].iloc[0]
        }
        features_data.append(features)
    
    if len(features_data) > 5:  # Need sufficient data for correlation
        features_df = pd.DataFrame(features_data)
        
        # Correlation matrix
        corr_matrix = features_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Feature Correlation Matrix",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlations with prediction
        pred_corr = corr_matrix['Prediction'].abs().sort_values(ascending=False)[1:]  # Exclude self-correlation
        
        st.markdown("#### 🔍 Top Factors Affecting Delivery Time")
        for feature, correlation in pred_corr.head(5).items():
            st.write(f"**{feature}**: {correlation:.3f}")
    else:
        st.info("Need more prediction data for correlation analysis.")

def render_trend_analysis():
    """Render trend analysis"""
    
    history_data = st.session_state.prediction_history
    
    if len(history_data) < 5:
        st.info("Need more prediction history for trend analysis.")
        return
    
    # Time-based trends
    timestamps = [record['timestamp'] for record in history_data]
    predictions = [record['prediction'] for record in history_data]
    
    # Create time-based DataFrame
    trend_df = pd.DataFrame({
        'Timestamp': timestamps,
        'Prediction': predictions
    })
    
    # Resample by hour if we have enough data
    if len(trend_df) > 10:
        trend_df.set_index('Timestamp', inplace=True)
        hourly_trend = trend_df.resample('H').mean()
        
        fig = px.line(
            hourly_trend,
            title='Hourly Prediction Trends',
            labels={'value': 'Average Delivery Time (min)', 'index': 'Time'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Moving average
    if len(predictions) >= 5:
        moving_avg = pd.Series(predictions).rolling(window=5).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=predictions,
            mode='lines+markers',
            name='Predictions',
            line=dict(color='lightblue')
        ))
        fig.add_trace(go.Scatter(
            y=moving_avg,
            mode='lines',
            name='Moving Average (5)',
            line=dict(color='red', width=3)
        ))
        
        fig.update_layout(
            title='Prediction Trend with Moving Average',
            xaxis_title='Prediction Number',
            yaxis_title='Delivery Time (minutes)'
        )
        st.plotly_chart(fig, use_container_width=True)
