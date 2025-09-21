import streamlit as st
import json
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Incendios Asturias", layout="wide")

# --- Cargar GeoJSON ---
@st.cache_data
def load_concejos():
    with open("C:/Users/VStudioCode/Proyectos/Streamlit_app/data/capas/Concejos_SITPA_4326.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    return geojson

concejos_geojson = load_concejos()

# --- Extraer lista de concejos ---
lista_concejos = [f["properties"]["concejo"] for f in concejos_geojson["features"]]

# --- Sidebar ---
st.sidebar.title("Dashboard de Incendios en Asturias")
concejo_sel = st.sidebar.selectbox("Selecciona un concejo", lista_concejos)

# --- DataFrame con colores ---
df = pd.DataFrame({
    "concejo": lista_concejos,
    "color": ["#d3d3d3"] * len(lista_concejos),  # todos en gris
})
df.loc[df["concejo"] == concejo_sel, "color"] = "#ff5733"  # seleccionado en rojo

# --- Mapa con todos los concejos visibles ---
st.subheader(f"Mapa de concejos de Asturias (seleccionado: {concejo_sel})")

fig = px.choropleth_mapbox(
    df,
    geojson=concejos_geojson,
    locations="concejo",
    featureidkey="properties.concejo",  # unión por atributo
    color="color",
    color_discrete_map="identity",
    hover_data={"concejo": True},
    mapbox_style="carto-positron",
    center={"lat": 43.36, "lon": -5.85},
    zoom=7,
)

st.plotly_chart(fig, use_container_width=True)

# --- Propiedades del concejo seleccionado ---
st.markdown("### Propiedades del concejo seleccionado")
props = next(f["properties"] for f in concejos_geojson["features"] if f["properties"]["concejo"] == concejo_sel)

st.write(f"**Código INE:** {props['codigo_ine']}")
st.write(f"**Nombre (castellano):** {props['concejo']}")
st.write(f"**Nombre (asturiano):** {props['conceyu']}")
st.write(f"**Área (m²):** {props['shape_Area']:,}")
st.write(f"**Perímetro (m):** {props['shape_Leng']:,}")
