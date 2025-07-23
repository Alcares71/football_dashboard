import streamlit as st
import pandas as pd

st.set_page_config(page_title="Men's Football Matrix", layout="wide")

df = pd.read_excel("football_betting_matrix_GLOBAL_FULL_ALL_REGIONS.xlsx", sheet_name="League Data")

st.title("⚽ Men's Football - Global Betting Matrix")

st.dataframe(df, use_container_width=True)
