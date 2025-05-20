import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load combined cleaned data (adjust path as needed)
@st.cache_data
def load_data():
    df_benin = pd.read_csv("data/Benin_clean.csv")
    df_benin['Country'] = 'Benin'
    df_sierraleone = pd.read_csv("data/sierraleone_clean.csv")
    df_sierraleone['Country'] = 'Sierra Leone'
    df_togo = pd.read_csv("data/togo_clean.csv")
    df_togo['Country'] = 'Togo'
    df = pd.concat([df_benin, df_sierraleone, df_togo], ignore_index=True)
    return df

df = load_data()

st.title("Solar Data Dashboard")

# --- Widget: Country multiselect ---
countries = df['Country'].unique()
selected_countries = st.multiselect("Select countries", options=countries, default=countries.tolist())

# Filter data based on selection
df_filtered = df[df['Country'].isin(selected_countries)]

# --- Boxplot: GHI by country ---
st.subheader("GHI Distribution by Country")
fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(data=df_filtered, x='Country', y='GHI', ax=ax)
st.pyplot(fig)

# --- Table: Top Regions by average GHI ---
# Assuming you have a 'Region' column (replace or drop if not present)
if 'Region' in df_filtered.columns:
    st.subheader("Top Regions by Average GHI")
    top_regions = df_filtered.groupby('Region')['GHI'].mean().sort_values(ascending=False).head(10)
    st.table(top_regions)
else:
    st.info("No 'Region' column found in data.")


