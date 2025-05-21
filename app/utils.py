import pandas as pd

# Load and combine data from CSVs
def load_data():
    df_benin = pd.read_csv("data/Benin_clean.csv")
    df_benin['Country'] = 'Benin'

    df_sierraleone = pd.read_csv("data/sierraleone_clean.csv")
    df_sierraleone['Country'] = 'Sierra Leone'

    df_togo = pd.read_csv("data/togo_clean.csv")
    df_togo['Country'] = 'Togo'

    df = pd.concat([df_benin, df_sierraleone, df_togo], ignore_index=True)

    # Add region mapping
    country_region_map = {
        'Benin': 'West Africa',
        'Sierra Leone': 'West Africa',
        'Togo': 'West Africa'
    }
    df['Region'] = df['Country'].map(country_region_map)

    return df

# (Optional) Top regions grouped by GHI
def get_top_regions(df, metric='GHI'):
    top = df.groupby('Region')[metric].mean().sort_values(ascending=False).reset_index()
    return top
