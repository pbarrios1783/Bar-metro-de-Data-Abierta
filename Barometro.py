import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar el CSV preprocesado
df_final = pd.read_csv("final_merged_data.csv")

# Título de la aplicación
st.title("Barómetro de Data Abierta")

st.write(df_final.columns)
