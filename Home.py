
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Men's Football Matrix", layout="wide")

# Lettura dati
df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

st.title("⚽ Men's Football - Global Betting Matrix")

# Mappatura tooltip
tooltips = {
    "Region": "Continent or macro area of the league",
    "Country": "Country where the league is based",
    "Effective Time": "Average effective playing time",
    "Style of Play": "Typical pace and tactical approach",
    "Game Fragmentation": "Level of interruptions in the match",
    "End-game Behavior": "Typical behavior in final minutes",
    "Over 2nd Half Propensity": "Tendency for 2nd half goals",
    "Strong Start 1H": "How often teams push early in first half",
    "Push to Extend Lead": "Frequency of pushing after taking the lead",
    "Late Corners Tendency": "Number of corners late in match",
    "Notes": "Extra tactical/structural notes",
    "Inverted Wingers Usage": "Tendency to use wingers on opposite foot/side",
    "Hidden Tactical Behaviors": "Non-obvious tactical traits",
    "Betting Profile": "Strategic classification for betting"
}

# Selettore colonne
columns = df.columns.tolist()
selected_cols = st.multiselect("📊 Select columns to display", columns, default=columns)

# Applichiamo colore per sezioni
def color_background(col):
    if col in ["Region", "Country"]:
        return "background-color: #ffe599;"  # giallo
    elif col in ["Effective Time", "Style of Play", "Game Fragmentation", "End-game Behavior"]:
        return "background-color: #d9ead3;"  # verde chiaro
    elif col in ["Over 2nd Half Propensity", "Strong Start 1H", "Push to Extend Lead", "Late Corners Tendency"]:
        return "background-color: #c9daf8;"  # azzurro
    elif col in ["Notes", "Inverted Wingers Usage", "Hidden Tactical Behaviors"]:
        return "background-color: #f4cccc;"  # rosa
    elif col == "Betting Profile":
        return "background-color: #ead1dc;"  # lilla
    return ""

# Costruzione tabella HTML con tooltip e colori
def generate_html_table(df):
    styles = [color_background(col) for col in df.columns]
    html = "<table><thead><tr>"
    for col, style in zip(df.columns, styles):
        tooltip = tooltips.get(col, col)
        html += f'<th style="{style}" title="{tooltip}">{col}</th>'
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for val, style in zip(row, styles):
            html += f'<td style="{style}">{val}</td>'
        html += "</tr>"
    html += "</tbody></table>"
    return html

# Mostra la tabella con colonne selezionate
df_view = df[selected_cols]
html_table = generate_html_table(df_view)
st.markdown(html_table, unsafe_allow_html=True)
