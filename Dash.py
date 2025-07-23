
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Football Matrix", layout="wide")

df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Mapping per nome abbreviato -> esteso + colore
COLUMN_CONFIG = {
    "Reg": ("Region", "#ffe599"),
    "Ctry": ("Country", "#ffe599"),
    "EffT": ("Effective Time", "#d9ead3"),
    "Style": ("Style of Play", "#d9ead3"),
    "Frag": ("Game Fragmentation", "#d9ead3"),
    "EndG": ("End-game Behavior", "#d9ead3"),
    "Ov2H": ("Over 2nd Half Propensity", "#c9daf8"),
    "1HSt": ("Strong Start 1H", "#c9daf8"),
    "Push+": ("Push to Extend Lead", "#c9daf8"),
    "LCorn": ("Late Corners Tendency", "#c9daf8"),
    "Notes": ("Notes", "#f4cccc"),
    "IW": ("Inverted Wingers Usage", "#f4cccc"),
    "TactX": ("Hidden Tactical Behaviors", "#f4cccc"),
    "BetP": ("Betting Profile", "#ead1dc")
}

# Mappo colonne originali su quelle abbreviate solo se esistono
available_cols = df.columns.tolist()
abbrev_map = {v[0]: k for k, v in COLUMN_CONFIG.items() if v[0] in available_cols}
reverse_map = {v: k for k, v in abbrev_map.items()}

# Ricostruisco DataFrame con colonne abbreviate
df_short = df.rename(columns=abbrev_map)
columns = df_short.columns.tolist()

# Selettore colonne con tutte selezionate di default
selected_cols = st.multiselect("📊 Select columns to display", columns, default=columns)

# Funzione per colorare header e tooltip
def make_table_html(df, columns):
    html = "<div style='overflow-x:auto'><table><thead><tr>"
    for col in columns:
        full_name = COLUMN_CONFIG.get(col, (col, ""))[0]
        color = COLUMN_CONFIG.get(col, (None, "#ffffff"))[1]
        html += f'<th style="background-color:{color}; padding:6px" title="{full_name}">{col}</th>'
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in columns:
            val = row[col]
            color = COLUMN_CONFIG.get(col, (None, "#ffffff"))[1]
            html += f'<td style="background-color:{color}; padding:6px">{val}</td>'
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

# Mostra la tabella
st.markdown(make_table_html(df_short[selected_cols], selected_cols), unsafe_allow_html=True)
