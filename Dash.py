
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Betting Matrix", layout="wide")
st.title("🏟️ Global Football Betting Matrix Dashboard")

# Carica il file Excel
df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Dizionario colonne abbreviate + tooltip
detailed_labels = {
    "Region": ("R", "Region"),
    "Country": ("C", "Country"),
    "Effective Time": ("ET", "Effective playing time"),
    "Style of Play": ("SP", "Style of Play"),
    "Game Fragmentation": ("GF", "Game Fragmentation (interruptions, fouls, etc.)"),
    "Final Minutes Behavior": ("FMB", "Team behavior in final minutes of the match"),
    "Over 2nd Half Propensity": ("O2H", "Propensity for over 0.5 goals in 2nd half"),
    "Strong Start by Favorites": ("FS1H", "Favorites starting strong in 1st half"),
    "Lead Extension Tendency": ("LET", "Teams' tendency to extend their lead"),
    "Late Corners": ("LC", "High number of corners in final minutes"),
    "Wing Play Style": ("WPS", "Tendency to use wing play"),
    "Inverted Winger Usage": ("IWU", "Use of inverted wingers (left-footed on right, etc.)"),
    "Typical Width": ("TW", "Tactical width of play"),
    "Pitch Size Note": ("PSN", "Field size and structural considerations"),
    "Aerial Strength": ("AS", "Aerial duel strength / heading ability"),
    "GK Average Height": ("GKAH", "Average goalkeeper height in league"),
    "Common Formation": ("CF", "Most used tactical formation"),
    "Betting Profile": ("BP", "Betting tendencies and angles"),
    "Notes": ("N", "Additional strategic or observational notes")
}

# Applica abbreviazioni
df_short = df.rename(columns={k: v[0] for k, v in detailed_labels.items() if k in df.columns})

# Tooltip HTML generator
def hover_header(short, tooltip):
    return f'<abbr title="{tooltip}">{short}</abbr>'

headers_html = [hover_header(short, tooltip) for _, (short, tooltip) in detailed_labels.items() if _ in df.columns]
ordered_cols = [short for _, (short, _) in detailed_labels.items() if _ in df_short.columns]
df_short = df_short[[col for col in ordered_cols if col in df_short.columns]]

# Sidebar
df = df.dropna(subset=["Region", "Country"])
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
country = st.sidebar.multiselect("Country", sorted(df["Country"].unique()))
over2h = st.sidebar.selectbox("Over 2nd Half", ["All"] + sorted(df["Over 2nd Half Propensity"].dropna().unique()))

# Filtro
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if country:
    filtered_df = filtered_df[filtered_df["Country"].isin(country)]
if over2h != "All":
    filtered_df = filtered_df[filtered_df["Over 2nd Half Propensity"] == over2h]

filtered_short = filtered_df.rename(columns={k: v[0] for k, v in detailed_labels.items() if k in filtered_df.columns})
ordered_cols = [short for _, (short, _) in detailed_labels.items() if _ in filtered_short.columns]
filtered_short = filtered_short[[col for col in ordered_cols if col in filtered_short.columns]]

# Styling
st.markdown('''
<style>
    table { font-size: 13px; }
    abbr { text-decoration: none; border-bottom: 1px dotted #888; cursor: help; }
</style>
''', unsafe_allow_html=True)

st.markdown(f"### ✅ {len(filtered_short)} leagues found")

# Tabella con fallback
if not filtered_short.empty:
    st.markdown(filtered_short.to_html(index=False, escape=False), unsafe_allow_html=True)
else:
    st.warning("No data to display for selected filters.")

# Download CSV
st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_betting_matrix.csv")

# Betting profile
if len(filtered_df) == 1:
    st.subheader("🎯 Betting Profile")
    st.markdown(filtered_df.iloc[0]["Betting Profile"])
