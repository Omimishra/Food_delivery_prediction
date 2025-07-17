import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
import base64
from io import StringIO

# Import custom components
from components.prediction_form import render_prediction_form
from components.scenario_comparison import render_scenario_comparison
from components.dashboard import render_dashboard
from utils.data_handler import load_models, prepare_input_data, make_prediction
from utils.visualizations import create_prediction_charts, create_factor_analysis
from utils.analytics import generate_prediction_insights, calculate_confidence_interval
from utils.theme_manager import initialize_theme, render_theme_toggle, get_dynamic_css

# Page configuration
st.set_page_config(
    page_title="🚚 Smart Delivery Time Predictor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme
initialize_theme()

# Load custom CSS and dynamic theme CSS
# --- app.py ---
def load_css():
    with open("styles/custom.css", "r", encoding="utf-8") as f:   # 👈 add encoding
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    
    # Apply dynamic theme CSS
    st.markdown(get_dynamic_css(), unsafe_allow_html=True)

load_css()

# Initialize session state
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []

# Load models
@st.cache_resource
def load_ml_models():
    return load_models()

try:
    encoder, scaler, model = load_ml_models()
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Please ensure encoder.pkl, scaler.pkl, and rf_model.pkl are in the current directory.")
    st.stop()

# Theme toggle
#render_theme_toggle()

# Header with animation
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🚚 Smart Delivery Time Predictor</h1>
    <p class="subtitle">AI-powered delivery time estimation with advanced analytics</p>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
tabs = st.tabs(["🎯 Single Prediction", "🔄 Scenario Comparison", "📈 Analytics Dashboard", "📋 History"])
st.markdown('</div>', unsafe_allow_html=True)

# Tab 1: Single Prediction
with tabs[0]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        #st.markdown('<div class="form-container">', unsafe_allow_html=True)
        prediction_data = render_prediction_form()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        #st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        if st.button("🔍 Predict Delivery Time", key="single_predict", help="Click to generate prediction"):
            with st.spinner("🤖 AI is analyzing your delivery parameters..."):
                # Add loading animation
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Make prediction
                final_input = prepare_input_data(prediction_data, encoder, scaler)
                prediction = make_prediction(model, final_input)
                confidence = calculate_confidence_interval(model, final_input)
                
                # Store prediction
                prediction_record = {
                    'timestamp': datetime.now(),
                    'prediction': prediction,
                    'confidence': confidence,
                    'input_data': prediction_data.copy()
                }
                st.session_state.prediction_history.append(prediction_record)
                st.session_state.current_prediction = prediction_record
                
                # Clear progress bar
                progress_bar.empty()
                
                # Display results with animation
                st.markdown(f"""
                <div class="prediction-result">
                    <div class="prediction-card">
                        <h3>⏱️ Estimated Delivery Time</h3>
                        <div class="prediction-value">{prediction:.1f} minutes</div>
                        <div class="confidence-range">
                            Confidence: {confidence[0]:.1f} - {confidence[1]:.1f} minutes
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Success animation
                st.balloons()
                
                # Insights
                insights = generate_prediction_insights(prediction_data, prediction)
                st.markdown('<div class="insights-container">', unsafe_allow_html=True)
                st.markdown("### 🧠 AI Insights")
                for insight in insights:
                    st.info(f"💡 {insight}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display current prediction charts
        if st.session_state.current_prediction:
            st.markdown("### 📊 Prediction Analysis")
            charts = create_prediction_charts(st.session_state.current_prediction)
            st.plotly_chart(charts['factor_impact'], use_container_width=True)
            
            # Factor analysis
            factor_chart = create_factor_analysis(prediction_data)
            st.plotly_chart(factor_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Scenario Comparison
with tabs[1]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    render_scenario_comparison(encoder, scaler, model)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Analytics Dashboard
with tabs[2]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    render_dashboard()
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: History
with tabs[3]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### 📋 Prediction History")
    
    if st.session_state.prediction_history:
        # Display history in a nice format
        history_df = pd.DataFrame([
            {
                'Timestamp': record['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'Predicted Time (min)': f"{record['prediction']:.1f}",
                'Confidence Range': f"{record['confidence'][0]:.1f} - {record['confidence'][1]:.1f}",
                'Distance (km)': record['input_data']['distance_km'].iloc[0],
                'Weather': record['input_data']['Weatherconditions'].iloc[0],
                'Traffic': record['input_data']['Road_traffic_density'].iloc[0]
            }
            for record in st.session_state.prediction_history
        ])
        
        st.dataframe(history_df, use_container_width=True)
        
        # Export functionality
        if st.button("📥 Export History"):
            csv = history_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="prediction_history.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ History exported successfully!")
        
        # Clear history
        if st.button("🗑️ Clear History"):
            st.session_state.prediction_history = []
            st.rerun()
    else:
        st.info("No predictions made yet. Use the Single Prediction tab to start!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using Streamlit | AI-Powered Delivery Time Prediction</p>
</div>
""", unsafe_allow_html=True)
