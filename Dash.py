
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Matrix Clean View", layout="wide")

df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Mapping abbreviazioni
COLUMN_ABBR = {
    "Region": "Reg",
    "Country": "Ctry",
    "Effective Time": "EffT",
    "Style of Play": "Style",
    "Game Fragmentation": "Frag",
    "End-game Behavior": "EndG",
    "Over 2nd Half Propensity": "Ov2H",
    "Strong Start 1H": "1HSt",
    "Push to Extend Lead": "Push+",
    "Late Corners Tendency": "LCorn",
    "Notes": "Notes",
    "Inverted Wingers Usage": "IW",
    "Hidden Tactical Behaviors": "TactX",
    "Betting Profile": "BetP"
}

# Applica abbreviazioni
abbr_rename = {k: v for k, v in COLUMN_ABBR.items() if k in df.columns}
df = df.rename(columns=abbr_rename)

# Tooltip per abbreviazioni
column_tooltips = {abbr: full for full, abbr in abbr_rename.items()}

st.title("📊 Football Matrix Explorer")
st.caption("Filtra per nazione o regione. Passa il mouse sulle intestazioni per leggere le abbreviazioni.")

# Filtri
col1, col2 = st.columns(2)
with col1:
    selected_region = st.multiselect("🌍 Region", sorted(df["Reg"].dropna().unique()), default=None)
with col2:
    selected_country = st.multiselect("🇨🇴 Country", sorted(df["Ctry"].dropna().unique()), default=None)

if selected_region:
    df = df[df["Reg"].isin(selected_region)]
if selected_country:
    df = df[df["Ctry"].isin(selected_country)]

# Ricerca testuale
search = st.text_input("🔍 Search in table (partial match, any column)")
if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# Selezione colonne
available_cols = df.columns.tolist()
selected_cols = st.multiselect("📌 Columns to display", available_cols, default=available_cols)

# Tooltip con markdown simulato
def render_tooltip_header(col):
    return f"<span title='{column_tooltips.get(col, col)}'>{col}</span>"

# Mostra tabella con tooltip simulati (HTML workaround)
styled_header = [render_tooltip_header(c) for c in selected_cols]
st.markdown(
    "<style>th div[data-testid='stMarkdownContainer']{white-space:nowrap;}</style>", unsafe_allow_html=True
)
st.dataframe(df[selected_cols], use_container_width=True, hide_index=True)

# Download
csv = df[selected_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="football_matrix_filtered.csv", mime="text/csv")
