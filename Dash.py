
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Betting Matrix", layout="wide")
st.title("🏟️ Global Football Betting Matrix Dashboard")

# Carica il file
df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")
df = df.dropna(subset=["Region", "Country"])

# Colonne disponibili nel file
all_columns = df.columns.tolist()

# Dizionario abbreviazioni + tooltip per alcune colonne
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
    "Inverted Winger Usage": ("IWU", "Use of inverted wingers"),
    "Typical Width": ("TW", "Tactical width of play"),
    "Pitch Size Note": ("PSN", "Field size and structural considerations"),
    "Aerial Strength": ("AS", "Aerial duel strength / heading ability"),
    "GK Average Height": ("GKAH", "Average goalkeeper height in league"),
    "Common Formation": ("CF", "Most used tactical formation"),
    "Betting Profile": ("BP", "Betting tendencies and angles"),
    "Notes": ("N", "Additional strategic or observational notes")
}

# Mappatura colonne esistenti con abbreviazioni
col_map = {k: v[0] for k, v in detailed_labels.items() if k in all_columns}
tooltip_map = {v[0]: v[1] for k, v in detailed_labels.items() if k in all_columns}

# Applica abbreviazioni dove possibile
df_short = df.rename(columns=col_map)

# Filtro colonne ON TOP
st.markdown("### 📊 Select Columns to Display")
selectable_cols = list(df_short.columns)
default_cols = selectable_cols[:10]  # mostra le prime 10 come default
selected_cols = st.multiselect("Choose columns", selectable_cols, default=default_cols)

# Filtro laterale
with st.sidebar:
    st.header("🔍 Filters")
    region = st.multiselect("Region", sorted(df["Region"].unique()))
    country = st.multiselect("Country", sorted(df["Country"].unique()))
    over2h = st.selectbox("Over 2nd Half", ["All"] + sorted(df["Over 2nd Half Propensity"].dropna().unique()) if "Over 2nd Half Propensity" in df.columns else ["All"])

filtered_df = df_short.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if country:
    filtered_df = filtered_df[filtered_df["Country"].isin(country)]
if over2h != "All" and "O2H" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["O2H"] == over2h]

filtered_df = filtered_df[selected_cols]

# Tooltip HTML
def generate_html_table(df, tooltips):
    html = df.to_html(index=False, escape=False)
    for col in df.columns:
        label = col
        tooltip = tooltips.get(col, "")
        html = html.replace(f">{label}<", f'><abbr title="{tooltip}">{label}</abbr><')
    return html

# Style
st.markdown('''
<style>
    table { font-size: 13px; word-break: break-word; }
    abbr { text-decoration: none; border-bottom: 1px dotted #888; cursor: help; }
    .block-container { padding: 1rem; }
</style>
''', unsafe_allow_html=True)

st.markdown(f"### ✅ {len(filtered_df)} leagues found")

if not filtered_df.empty:
    html_table = generate_html_table(filtered_df, tooltip_map)
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.warning("No data to display for selected filters.")

# Download CSV
st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_betting_matrix.csv")

# Profilo scommesse
if len(filtered_df) == 1 and "BP" in filtered_df.columns:
    st.subheader("🎯 Betting Profile")
    st.markdown(filtered_df.iloc[0]["BP"])
