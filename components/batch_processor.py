import streamlit as st
import pandas as pd
import numpy as np
from utils.data_handler import process_batch_data, create_sample_batch_data
from utils.visualizations import create_batch_analysis_chart
import base64
from io import StringIO

def render_batch_processor(encoder, scaler, model):
    """Render the batch processing interface"""
    
    st.markdown("### 📊 Batch Processing")
    st.info("Upload a CSV file with multiple orders for batch prediction")
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📤 Upload Data")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload a CSV file with delivery order data"
        )
        
        # Sample data download
        if st.button("📥 Download Sample Template"):
            sample_data = create_sample_batch_data()
            csv = sample_data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="sample_batch_template.csv">Download Sample CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Sample template ready for download!")
        
        # Show required columns
        with st.expander("📋 Required Columns"):
            required_cols = [
                "Delivery_person_Age", "Delivery_person_Ratings", "Weatherconditions",
                "Road_traffic_density", "Vehicle_condition", "Type_of_order",
                "Type_of_vehicle", "multiple_deliveries", "Festival", "City",
                "distance_km", "prep_time_min", "order_hour", "order_day", "is_weekend"
            ]
            st.write("Your CSV must contain these columns:")
            for col in required_cols:
                st.write(f"• {col}")
    
    with col2:
        st.markdown("#### ⚙️ Processing Options")
        
        # Processing options
        include_confidence = st.checkbox("Include Confidence Intervals", value=True)
        include_insights = st.checkbox("Include AI Insights", value=True)
        
        # Export format
        export_format = st.selectbox("Export Format", ["CSV", "JSON", "Excel"])
        
        # Progress tracking
        show_progress = st.checkbox("Show Progress", value=True)
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            # Preview uploaded data
            preview_data = pd.read_csv(uploaded_file)
            st.markdown("#### 👀 Data Preview")
            st.dataframe(preview_data.head(), use_container_width=True)
            
            # Validation
            st.markdown("#### ✅ Validation")
            required_columns = [
                "Delivery_person_Age", "Delivery_person_Ratings", "Weatherconditions",
                "Road_traffic_density", "Vehicle_condition", "Type_of_order",
                "Type_of_vehicle", "multiple_deliveries", "Festival", "City",
                "distance_km", "prep_time_min", "order_hour", "order_day", "is_weekend"
            ]
            
            missing_columns = [col for col in required_columns if col not in preview_data.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {missing_columns}")
            else:
                st.success("✅ All required columns present")
                
                # Process button
                if st.button("🚀 Process Batch", type="primary"):
                    with st.spinner("Processing batch predictions..."):
                        # Reset file pointer
                        uploaded_file.seek(0)
                        
                        # Process data
                        try:
                            batch_results = process_batch_data(uploaded_file, encoder, scaler, model)
                            
                            # Store results in session state
                            st.session_state.batch_results = batch_results
                            
                            st.success(f"✅ Successfully processed {len(batch_results)} orders!")
                            
                            # Display results
                            display_batch_results(batch_results, include_confidence, include_insights)
                            
                        except Exception as e:
                            st.error(f"❌ Error processing batch: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    
    # Display stored results if available
    elif st.session_state.batch_results is not None:
        st.markdown("#### 📊 Previous Batch Results")
        display_batch_results(st.session_state.batch_results, include_confidence, include_insights)

def display_batch_results(batch_results, include_confidence, include_insights):
    """Display batch processing results"""
    
    # Summary statistics
    st.markdown("#### 📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(batch_results))
    
    with col2:
        avg_time = batch_results['Predicted_Delivery_Time'].mean()
        st.metric("Average Time", f"{avg_time:.1f} min")
    
    with col3:
        min_time = batch_results['Predicted_Delivery_Time'].min()
        st.metric("Fastest", f"{min_time:.1f} min")
    
    with col4:
        max_time = batch_results['Predicted_Delivery_Time'].max()
        st.metric("Slowest", f"{max_time:.1f} min")
    
    # Results table
    st.markdown("#### 📋 Detailed Results")
    
    # Add additional columns if requested
    display_columns = list(batch_results.columns)
    
    if include_confidence:
        # Add confidence intervals (simplified for demo)
        batch_results['Confidence_Lower'] = batch_results['Predicted_Delivery_Time'] * 0.85
        batch_results['Confidence_Upper'] = batch_results['Predicted_Delivery_Time'] * 1.15
        display_columns.extend(['Confidence_Lower', 'Confidence_Upper'])
    
    if include_insights:
        # Add simple insights
        insights = []
        for _, row in batch_results.iterrows():
            if row['distance_km'] > 10:
                insights.append("Long distance order")
            elif row['Road_traffic_density'] == 'Jam':
                insights.append("Traffic delay expected")
            elif row['Weatherconditions'] in ['Stormy', 'Sandstorms']:
                insights.append("Weather delay possible")
            else:
                insights.append("Normal delivery")
        
        batch_results['AI_Insights'] = insights
        display_columns.append('AI_Insights')
    
    # Display results
    st.dataframe(batch_results[display_columns], use_container_width=True)
    
    # Visualizations
    st.markdown("#### 📊 Analysis Charts")
    analysis_chart = create_batch_analysis_chart(batch_results)
    if analysis_chart:
        st.plotly_chart(analysis_chart, use_container_width=True)
    
    # Export functionality
    st.markdown("#### 📥 Export Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as CSV"):
            csv = batch_results.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="batch_results.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        if st.button("Export as JSON"):
            json_str = batch_results.to_json(orient='records', indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="batch_results.json">Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col3:
        if st.button("Export Summary"):
            summary_stats = {
                'Total_Orders': len(batch_results),
                'Average_Time': batch_results['Predicted_Delivery_Time'].mean(),
                'Median_Time': batch_results['Predicted_Delivery_Time'].median(),
                'Min_Time': batch_results['Predicted_Delivery_Time'].min(),
                'Max_Time': batch_results['Predicted_Delivery_Time'].max(),
                'Std_Deviation': batch_results['Predicted_Delivery_Time'].std()
            }
            
            summary_df = pd.DataFrame([summary_stats])
            csv = summary_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="batch_summary.csv">Download Summary</a>'
            st.markdown(href, unsafe_allow_html=True)

def render_scenario_comparison():
    """Render scenario comparison tool"""
    st.markdown("### 🔄 Scenario Comparison")
    st.info("Compare different delivery scenarios side by side")
    
    # This would integrate with the main prediction form
    # to allow users to create multiple scenarios and compare them
    pass
