import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Set page configuration
st.set_page_config(
    page_title="Simple Data Explorer",
    page_icon="📊"
)

# Add a title and description
st.title("📊 Simple Data Explorer")
st.markdown("Upload your CSV file or generate simple data")

# Function to display dataframe as HTML (avoids PyArrow)
def display_dataframe(df, max_rows=10):
    """Display dataframe as HTML with a max of `max_rows`."""
    # Convert all columns to strings to avoid any serialization issues
    df_html = df.astype(str).head(max_rows).to_html(index=False)
    st.write(df_html, unsafe_allow_html=True)

# File upload option
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Load and display file content
if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded!")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Try uploading a different file or generate simple data below.")
        df = None
else:
    df = None

# Simple data generation option
if df is None and st.button("Generate Simple Data"):
    # Create simple numeric data with meaningful column names
    data = {
        "time_period": list(range(1, 101)),  # x -> time period or index
        "sales": [i * 2 + np.random.randint(0, 10) for i in range(1, 101)],  # y1 -> sales
        "profit": [i * 1.5 + np.random.randint(0, 15) for i in range(1, 101)],  # y2 -> profit
        "category": [("A" if i % 3 == 0 else "B" if i % 3 == 1 else "C") for i in range(1, 101)]  # Category
    }
    
    df = pd.DataFrame(data)
    st.success("Simple data generated!")

# Check if data exists
if df is not None:
    # Display data as HTML
    st.subheader("Data Preview (First 10 rows)")
    display_dataframe(df, 10)
    
    # Display basic statistics
    st.subheader("Data Summary")
    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")

    # Display column types
    col_types = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    st.write("**Column Types:**")
    for col, dtype in col_types.items():
        st.write(f"- {col}: {dtype}")
    
    # Create a simple visualization
    st.subheader("Data Visualization")
    
    # Get numeric columns
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    
    if len(numeric_columns) > 0:
        # Select columns for visualization
        y_column = st.selectbox("Select column to visualize", numeric_columns)
        
        # Select chart type
        chart_type = st.radio(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Histogram"]
        )
        
        # Create the selected chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == "Line Chart":
            ax.plot(df.index, df[y_column])
            ax.set_xlabel('Index')
            ax.set_ylabel(y_column)
            ax.set_title(f'Line Chart: {y_column}')
            
        elif chart_type == "Bar Chart":
            ax.bar(df.index, df[y_column])
            ax.set_xlabel('Index')
            ax.set_ylabel(y_column)
            ax.set_title(f'Bar Chart: {y_column}')
            
        elif chart_type == "Histogram":
            bins = st.slider("Number of bins", min_value=5, max_value=50, value=20)
            ax.hist(df[y_column], bins=bins)
            ax.set_xlabel(y_column)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Histogram: {y_column}')
        
        ax.grid(True)
        st.pyplot(fig)
        
        # Download data option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv",
        )
    else:
        st.warning("No numeric columns found for visualization.")
else:
    st.info("Please upload a CSV file or generate simple data to begin.")

# Add a footer
st.markdown("---")
st.markdown("Built with Streamlit! 🚀")
