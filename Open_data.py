import pandas as pd
import plotly.express as px
import json
import requests
import streamlit as st

# Cargar los datasets
df_capabilities = pd.read_csv("gdb-2021-capabilities-module-data.csv")
df_governance = pd.read_csv("gdb-2021-governance-module-data.csv")
df_integrity = pd.read_csv("gdb-2021-political-integrity-module-data.csv")

# Cargar el dataset de ciudades mundiales con latitud y longitud
df_cities = pd.read_csv("worldcities.csv")

# Cargar GeoJSON con las fronteras de los países desde la web
geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
response = requests.get(geojson_url)
geo_countries = response.json()

# Función para fusionar los datasets con las ciudades usando 'iso3'
def fusionar_con_ciudades(df_modulo, df_cities):
    df_fusionado = pd.merge(df_modulo, df_cities, how="inner", left_on="iso3", right_on="iso3")
    df_fusionado = df_fusionado.drop(columns=['country_x', 'admin_name', 'population', 'id'])  # Eliminar columnas innecesarias
    df_fusionado = df_fusionado.rename(columns={"country_y": "country"})  # Renombrar para mayor claridad
    return df_fusionado.groupby('country').first().reset_index()  # Agrupar por país

# Fusionar todos los datasets
df_capabilities_grouped = fusionar_con_ciudades(df_capabilities, df_cities)
df_governance_grouped = fusionar_con_ciudades(df_governance, df_cities)
df_integrity_grouped = fusionar_con_ciudades(df_integrity, df_cities)

# Título de la aplicación
st.title("Barómetro de Data Abierta")

# Barra lateral para seleccionar la capa
st.sidebar.title("Selecciona una capa")
capa = st.sidebar.selectbox("Elige un dataset para mostrar", ['Capacidades', 'Gobernanza', 'Integridad Política'])

# Barra lateral para deslizador de filtrado de puntuaciones
if capa == 'Capacidades':
    min_score, max_score = st.sidebar.slider("Selecciona el rango de puntuación", float(df_capabilities_grouped['score'].min()), float(df_capabilities_grouped['score'].max()), (float(df_capabilities_grouped['score'].min()), float(df_capabilities_grouped['score'].max())))
    datos_filtrados = df_capabilities_grouped[(df_capabilities_grouped['score'] >= min_score) & (df_capabilities_grouped['score'] <= max_score)]
    escala_color = "Viridis"
    etiqueta = "Puntuación de Capacidades"

elif capa == 'Gobernanza':
    min_score, max_score = st.sidebar.slider("Selecciona el rango de puntuación", float(df_governance_grouped['score'].min()), float(df_governance_grouped['score'].max()), (float(df_governance_grouped['score'].min()), float(df_governance_grouped['score'].max())))
    datos_filtrados = df_governance_grouped[(df_governance_grouped['score'] >= min_score) & (df_governance_grouped['score'] <= max_score)]
    escala_color = "Bluered"
    etiqueta = "Puntuación de Gobernanza"

elif capa == 'Integridad Política':
    min_score, max_score = st.sidebar.slider("Selecciona el rango de puntuación", float(df_integrity_grouped['score'].min()), float(df_integrity_grouped['score'].max()), (float(df_integrity_grouped['score'].min()), float(df_integrity_grouped['score'].max())))
    datos_filtrados = df_integrity_grouped[(df_integrity_grouped['score'] >= min_score) & (df_integrity_grouped['score'] <= max_score)]
    escala_color = "Portland"
    etiqueta = "Puntuación de Integridad Política"

else:
    st.error("Por favor, selecciona un dataset válido.")
    st.stop()  # Detener la ejecución si no se selecciona una capa válida

# Crear el mapa coroplético de Plotly basado en la capa seleccionada y el rango de puntuaciones
fig = px.choropleth(datos_filtrados, 
                    geojson=geo_countries, 
                    locations='iso3',  # Columna que contiene los códigos ISO3 de los países
                    color='score',  # Columna que contiene la puntuación
                    hover_name='country',  # Columna para mostrar al pasar el ratón
                    color_continuous_scale=escala_color,  # Escala de color según la capa seleccionada
                    range_color=(min_score, max_score),  # Rango para la escala de color basada en el deslizador
                    labels={'score': etiqueta},  # Etiquetas para la leyenda de color
                    featureidkey="properties.ISO_A3"  # Este es el identificador clave en el GeoJSON que coincide con el código ISO3
                   )

# Actualizar el diseño para hacer el mapa más grande y ajustar márgenes
fig.update_layout(
    margin={"r":10, "t":0, "l":10, "b":0},  # Márgenes ajustados para un mejor uso del espacio
)

# Mostrar el mapa de Plotly en Streamlit, asegurándose de usar todo el ancho del contenedor
st.plotly_chart(fig, use_container_width=False)
