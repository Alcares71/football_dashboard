
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Matrix Tooltip View", layout="wide")

df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")
df = df.rename(columns={"Country": "League"})

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

abbr_rename = {k: v for k, v in COLUMN_ABBR.items() if k in df.columns}
df = df.rename(columns=abbr_rename)

# Inverti dict per tooltip
TOOLTIPS = {v: k for k, v in abbr_rename.items()}

st.title("📊 Football Matrix Explorer")
st.caption("Con tooltip visibili sulle intestazioni (🛈 passa il mouse per dettagli)")

# Filtri base
col1, col2 = st.columns(2)
with col1:
    selected_region = st.multiselect("🌍 Region", sorted(df["Reg"].dropna().unique()), default=None)
with col2:
    selected_league = st.multiselect("🏆 League", sorted(df["League"].dropna().unique()), default=None)

if selected_region:
    df = df[df["Reg"].isin(selected_region)]
if selected_league:
    df = df[df["League"].isin(selected_country)]

# Ricerca testuale
search = st.text_input("🔍 Search in table (any column)")
if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# Mostra tabella

# Tooltip mapping per abbreviazioni
TOOLTIPS = {
    "Reg": "Region",
    "League": "League name (includes 2nd tiers)",
    "EffT": "Effective Time (actual minutes of play)",
    "Style": "Style of Play (direct vs possession)",
    "Frag": "Game Fragmentation",
    "EndG": "End-game Behavior",
    "Ov2H": "Over 2nd Half Propensity",
    "1HSt": "Strong Start in 1st Half",
    "Push+": "Push to Extend Lead",
    "LCorn": "Late Corners Tendency",
    "Notes": "Tactical notes and quirks",
    "IW": "Inverted Wingers Usage",
    "TactX": "Hidden Tactical Behaviors",
    "BetP": "Betting Profile"
}

col_cfg = {
    col: st.column_config.TextColumn(label=col, help=TOOLTIPS.get(col, ""))
    for col in df.columns if col in TOOLTIPS
}


st.data_editor(
    df,
    column_config=col_cfg,
    use_container_width=True,
    hide_index=True
    df,
    
    disabled=True,
    use_container_width=True,
    hide_index=True,
)

# Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="football_matrix_filtered.csv", mime="text/csv")
