import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Betting Matrix", layout="wide")
st.title("🏟️ Global Football Betting Matrix Dashboard")

# Carica il file Excel
df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

# Dizionario: NomeColonnaOriginale -> (Etichetta corta, Tooltip)
col_labels = {
    "Region": ("Reg", "Geographical region"),
    "Country": ("Ctry", "Country name"),
    "League": ("Lg", "Full league name"),
    "Over 2nd Half Propensity": ("O2H", "Over 2nd Half Propensity"),
    "Final Minutes Corner Intensity": ("FMC", "Corner volume in final 10 minutes"),
    "Favorite Starts Strong (1H)": ("FS1H", "Strong first halves from favorites"),
    "Inverted Winger Usage": ("IW", "Inverted wingers reduce cross/corner frequency"),
    "Tactical Width": ("TW", "Typical width of play: narrow vs wide"),
    "Common Formation": ("Form", "Most used tactical formation"),
    "Betting Profile": ("BP", "Betting angles & tendencies"),
    "Notes": ("Note", "Additional tactical/structural info")
}

# Riduci nomi colonne
df_short = df.rename(columns={original: short for original, (short, _) in col_labels.items() if original in df.columns})

# Sidebar per i filtri
st.sidebar.header("🔍 Filters")
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
country = st.sidebar.multiselect("Country", sorted(df["Country"].unique()))
over2h = st.sidebar.selectbox("Over 2nd Half", ["All"] + sorted(df["Over 2nd Half Propensity"].dropna().unique()))

# Applica i filtri
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if country:
    filtered_df = filtered_df[filtered_df["Country"].isin(country)]
if over2h != "All":
    filtered_df = filtered_df[filtered_df["Over 2nd Half Propensity"] == over2h]

# Riduci anche il DataFrame filtrato
filtered_short = filtered_df.rename(columns={original: short for original, (short, _) in col_labels.items() if original in filtered_df.columns})

# Costruisci intestazioni con tooltip HTML
def hover_header(short, tooltip):
    return f'<abbr title="{tooltip}">{short}</abbr>'

headers_html = [hover_header(short, tooltip) for original, (short, tooltip) in col_labels.items() if original in filtered_df.columns]

# Riorganizza le colonne nell'ordine del dizionario
ordered_cols = [short for _, (short, _) in col_labels.items() if _ in filtered_df.columns]
filtered_short = filtered_short[[col for col in ordered_cols if col in filtered_short.columns]]

# Mostra la tabella con stile compatto e descrizione al passaggio del mouse
st.markdown("""
<style>
    table { font-size: 13px; }
    abbr { text-decoration: none; border-bottom: 1px dotted #888; cursor: help; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"### ✅ {len(filtered_short)} leagues found")
st.markdown(filtered_short.to_html(index=False, escape=False), unsafe_allow_html=True)

# Pulsante per scaricare il CSV
st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_betting_matrix.csv")

# Betting Profile dettagliato se una sola lega
if len(filtered_df) == 1:
    st.subheader(":dart: Betting Profile")
    st.markdown(filtered_df.iloc[0]["Betting Profile"])
