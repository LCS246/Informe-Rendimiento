import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Player Infographic", layout="wide")

# CSS para el look llamativo
st.markdown("""
    <style>
    .metric-card { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #1f77b4; }
    .stApp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PLAYER INFOGRAPHIC DASHBOARD")

archivo = st.sidebar.file_uploader("Sube Excel", type=['xlsx'])

if archivo:
    df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
    df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
    
    nombre = st.sidebar.selectbox("Selecciona Atleta", df_base['NOMBRE'].unique())
    datos_fatiga = df_fatiga[df_fatiga['NOMBRE'] == nombre].iloc[-1]
    datos_base = df_base[df_base['NOMBRE'] == nombre].iloc[0]

    # --- LAYOUT DE LA FICHA ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Aquí intentamos cargar la foto
        foto_path = f"fotos/{nombre.lower().replace(' ', '_')}.jpg"
        if os.path.exists(foto_path):
            st.image(foto_path, width=250)
        else:
            st.warning("Foto no encontrada en carpeta /fotos")
        
        st.write(f"### {nombre}")
        st.info(f"**Historial Lesiones:** {datos_base.get('HISTORIAL DE LESIONES', 'Ninguna')}")

    with col2:
        st.subheader("📊 Métricas de Rendimiento")
        m1, m2, m3 = st.columns(3)
        m1.metric("CMJ", f"{datos_fatiga['CMJ']} cm")
        m2.metric("VFC", f"{datos_fatiga['VFC']} ms")
        m3.metric("RPE", f"{datos_fatiga['RPE']}/10")
        
        st.subheader("📋 Datos Completos")
        st.table(datos_fatiga.to_frame())

    # Botón PDF (usando la lógica anterior)
    if st.button("📥 Generar Informe PDF"):
        st.success("PDF Generado (puedes añadir aquí la función de descarga)")

else:
    st.info("Sube tu archivo para ver el Dashboard.")


