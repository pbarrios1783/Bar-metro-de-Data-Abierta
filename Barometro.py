import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar el CSV preprocesado
df_final = pd.read_xls("final_merged_data.xls")

# Título de la aplicación
st.title("Barómetro de Data Abierta")

# Barra lateral para seleccionar la capa
st.sidebar.title("Selecciona una capa")
capa = st.sidebar.selectbox("Elige un dataset para mostrar", ['Capacidades', 'Gobernanza', 'Integridad Política'])

# Filtrar los datos según la capa seleccionada
df_filtrado = df_final[df_final['capa'] == capa]

# Barra lateral para deslizador de filtrado de puntuaciones
min_score, max_score = st.sidebar.slider("Selecciona el rango de puntuación", float(df_filtrado['score'].min()), float(df_filtrado['score'].max()), (float(df_filtrado['score'].min()), float(df_filtrado['score'].max())))
datos_filtrados = df_filtrado[(df_filtrado['score'] >= min_score) & (df_filtrado['score'] <= max_score)]

# Crear el mapa coroplético de Plotly basado en la capa seleccionada y el rango de puntuaciones
fig = px.choropleth(datos_filtrados, 
                    geojson="https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson", 
                    locations='iso3',  
                    color='score',  
                    hover_name='country',  
                    color_continuous_scale="Viridis", 
                    range_color=(min_score, max_score),  
                    labels={'score': "Puntuación"},  
                    featureidkey="properties.ISO_A3"  
                   )

# Mostrar el mapa de Plotly en Streamlit
st.plotly_chart(fig, use_container_width=True)
