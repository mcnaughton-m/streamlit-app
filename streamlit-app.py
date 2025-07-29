import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import time

# Set page configuration
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="📊",
    layout="wide"
)

def main():
    # 1. HEADER SECTION
    st.title("📊 My Interactive Streamlit Dashboard")
    st.markdown("---")
    
    # 2. SIDEBAR FOR CONTROLS
    st.sidebar.header("🎛️ Controls")
    
    # Sidebar controls
    chart_type = st.sidebar.selectbox(
        "Choose Chart Type:",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"]
    )
    
    data_points = st.sidebar.slider(
        "Number of Data Points:",
        min_value=10,
        max_value=100,
        value=50,
        step=10
    )
    
    # 3. MAIN CONTENT AREA
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📈 Data Visualization")
        
        # Generate sample data
        dates = pd.date_range('2024-01-01', periods=data_points, freq='D')
        values = np.random.randn(data_points).cumsum()
        
        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        
        # Create different charts based on selection
        if chart_type == "Line Chart":
            fig = px.line(df, x='Date', y='Value', title='Time Series Data')
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x='Date', y='Value', title='Bar Chart Data')
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x='Date', y='Value', title='Scatter Plot')
        else:  # Histogram
            fig = px.histogram(df, x='Value', title='Value Distribution')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.header("📊 Statistics")
        
        # Display statistics
        st.metric("Mean", f"{df['Value'].mean():.2f}")
        st.metric("Std Dev", f"{df['Value'].std():.2f}")
        st.metric("Min", f"{df['Value'].min():.2f}")
        st.metric("Max", f"{df['Value'].max():.2f}")
    
    # 4. INTERACTIVE FEATURES
    st.markdown("---")
    st.header("🎯 Interactive Features")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a CSV file:",
        type=['csv'],
        help="Upload your own data to analyze"
    )
    
    if uploaded_file is not None:
        try:
            user_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(user_df.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # 5. FORM INPUT
    with st.expander("📝 Add Custom Data"):
        with st.form("custom_data_form"):
            name = st.text_input("Name:")
            age = st.number_input("Age:", min_value=0, max_value=120, value=25)
            city = st.selectbox("City:", ["New York", "London", "Tokyo", "Paris", "Berlin"])
            
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                st.success(f"Data submitted: {name}, {age} years old, from {city}")
    
    # 6. PROGRESS AND STATUS
    st.markdown("---")
    st.header("⚡ Progress Tracking")
    
    if st.button("Run Simulation"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i+1}%")
        
        status_text.text("✅ Simulation complete!")
        st.balloons()
    
    # 7. DATA TABLE
    st.markdown("---")
    st.header("📋 Data Table")
    
    # Create sample table data
    table_data = pd.DataFrame({
        'Product': ['Laptop', 'Phone', 'Tablet', 'Watch'],
        'Price': [999, 699, 399, 299],
        'Sales': [150, 300, 100, 200],
        'Rating': [4.5, 4.2, 4.0, 4.8]
    })
    
    st.dataframe(table_data, use_container_width=True)
    
    # 8. FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    