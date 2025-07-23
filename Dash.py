import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Betting Matrix", layout="wide")
st.title("🏟️ Global Football Betting Matrix Dashboard")

# Carica il file Excel caricato in precedenza
df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Sidebar per i filtri
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
country = st.sidebar.multiselect("Country", sorted(df["Country"].unique()))
over2h = st.sidebar.selectbox("Over 2nd Half Propensity", ["All", "Poor", "OK", "Good"])

# Applica i filtri
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if country:
    filtered_df = filtered_df[filtered_df["Country"].isin(country)]
if over2h != "All":
    filtered_df = filtered_df[filtered_df["Over 2nd Half Propensity"] == over2h]

# Mostra i risultati
st.markdown(f"### ✅ {len(filtered_df)} leagues found")
st.dataframe(filtered_df, use_container_width=True)

# Extra: esportazione CSV
st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_betting_matrix.csv")

# Extra: mostra profilo betting se una sola lega selezionata
if len(filtered_df) == 1:
    st.subheader(":dart: Betting Profile")
    st.markdown(filtered_df.iloc[0]["Betting Profile"])
