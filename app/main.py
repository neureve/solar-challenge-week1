import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import load_data, get_top_regions  # assuming you moved data functions here

# Load data
df = load_data()


st.title("Solar Data Dashboard")

# --- Sidebar filters ---
countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect(
    "Select Countries", options=countries, default=countries.tolist()
)

metrics = ['GHI', 'DNI', 'Tamb', 'TModA', 'TModB'] # example metrics, replace as needed
selected_metric = st.sidebar.selectbox("Select Metric", metrics, index=0)

df_filtered = df[df['Country'].isin(selected_countries)]

# --- Tabs for layout organization ---
tab1, tab2, tab3 = st.tabs(["Boxplot", "Bar Chart", "Line Chart"])

with tab1:
    st.subheader(f"{selected_metric} Distribution by Country (Boxplot)")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df_filtered, x='Country', y=selected_metric, ax=ax)
    st.pyplot(fig)

with tab2:
    st.subheader(f"Average {selected_metric} by Country (Bar Chart)")
    bar_data = df_filtered.groupby('Country')[selected_metric].mean().reset_index()
    fig_bar = px.bar(bar_data, x='Country', y=selected_metric, color='Country', title=f"Average {selected_metric} by Country")
    st.plotly_chart(fig_bar)

with tab3:
    st.subheader(f"{selected_metric} Trends Over Time (Line Chart)")
    # Assuming your data has a 'Date' or similar column for time series
    if 'Date' in df_filtered.columns:
        df_filtered['Date'] = pd.to_datetime(df_filtered['Date'])
        line_data = df_filtered.groupby(['Date', 'Country'])[selected_metric].mean().reset_index()
        fig_line = px.line(line_data, x='Date', y=selected_metric, color='Country', title=f"{selected_metric} Trends Over Time")
        st.plotly_chart(fig_line)
    else:
        st.info("No 'Date' column found for line chart.")

# --- Top regions table ---
if 'Region' in df_filtered.columns:
    st.subheader("Top Regions by Average " + selected_metric)
    top_regions = df_filtered.groupby('Region')[selected_metric].mean().sort_values(ascending=False).reset_index()
    st.table(top_regions)
else:
    st.info("No 'Region' column found in data.")


