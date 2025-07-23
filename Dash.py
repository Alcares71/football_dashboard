
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Football Matrix", layout="wide")

df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Mapping: abbreviazione -> (nome completo, sezione)
COLUMN_SECTIONS = {
    "Region": ("Reg", "Region"),
    "Country": ("Ctry", "Region"),
    "Effective Time": ("EffT", "Style"),
    "Style of Play": ("Style", "Style"),
    "Game Fragmentation": ("Frag", "Style"),
    "End-game Behavior": ("EndG", "Style"),
    "Over 2nd Half Propensity": ("Ov2H", "Final"),
    "Strong Start 1H": ("1HSt", "Final"),
    "Push to Extend Lead": ("Push+", "Final"),
    "Late Corners Tendency": ("LCorn", "Final"),
    "Notes": ("Notes", "Tactic"),
    "Inverted Wingers Usage": ("IW", "Tactic"),
    "Hidden Tactical Behaviors": ("TactX", "Tactic"),
    "Betting Profile": ("BetP", "Profile")
}

# Ordine e separazione tra sezioni
SECTION_ORDER = ["Region", "Style", "Final", "Tactic", "Profile"]
section_columns = {s: [] for s in SECTION_ORDER}
for full_name, (abbr, section) in COLUMN_SECTIONS.items():
    if full_name in df.columns:
        section_columns[section].append((full_name, abbr))

# Costruzione DataFrame abbreviato + spaziature tra sezioni
columns_ordered = []
col_tooltips = {}
for section in SECTION_ORDER:
    if section_columns[section]:
        if columns_ordered:  # se non è la prima sezione, aggiungi colonna vuota separatrice
            spacer = f"__{section}__"
            df[spacer] = ""
            columns_ordered.append(spacer)
        for full, abbr in section_columns[section]:
            df[abbr] = df[full]
            columns_ordered.append(abbr)
            col_tooltips[abbr] = full

# Visualizzazione
st.title("📊 Global Football Matrix")
st.caption("Tutte le metriche sono in inglese. Passa il mouse sui nomi per leggere la descrizione.")

# Mostra la tabella
st.dataframe(df[columns_ordered], use_container_width=True)

# Download
csv = df[columns_ordered].to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name="football_matrix_filtered.csv", mime="text/csv")
