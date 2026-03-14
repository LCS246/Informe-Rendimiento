import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página para que sea ancha y profesional
st.set_page_config(page_title="Player Performance Pro", layout="wide")

# Estilo CSS personalizado para que sea MUY llamativo (estilo oscuro y neón)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 15px; }
    .info-box { background-color: #1f2937; color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; }
    h1, h2, h3 { color: #f0f6fc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PLAYER INFOGRAPHIC DASHBOARD")

archivo = st.sidebar.file_uploader("📂 Sube tu archivo Excel", type=['xlsx'])

if archivo:
    try:
        # Cargamos las hojas
        df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
        df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        
        # --- SOLUCIÓN AL ERROR DE COLUMNAS ---
        # Limpiamos nombres de columnas (quitar espacios y poner en mayúsculas)
        df_base.columns = df_base.columns.str.strip().str.upper()
        df_fatiga.columns = df_fatiga.columns.str.strip().str.upper()
        
        # Filtro de Atleta en la barra lateral
        if 'NOMBRE' in df_base.columns:
            atleta = st.sidebar.selectbox("👤 Selecciona Atleta", df_base['NOMBRE'].unique())
            
            # Obtener datos del atleta seleccionado
            datos_base = df_base[df_base['NOMBRE'] == atleta].iloc[0]
            datos_fatiga = df_fatiga[df_fatiga['NOMBRE'] == atleta].iloc[-1] # Último registro
            
            # --- DISEÑO TIPO INFOGRAFÍA ---
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Espacio para "Foto" y Datos Base
                st.markdown(f"""
                <div class="info-box">
                    <h2 style='text-align: center;'>{atleta}</h2>
                    <p><b>EDAD:</b> {datos_base.get('EDAD', 'N/A')}</p>
                    <p><b>PESO:</b> {datos_base.get('PESO', 'N/A')} kg</p>
                    <p><b>ALTURA:</b> {datos_base.get('ALTURA', 'N/A')} cm</p>
                    <hr>
                    <p style='color: #ef4444;'><b>⚠️ HISTORIAL MÉDICO:</b><br>{datos_base.get('HISTORIAL DE LESIONES', 'Ninguno')}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.subheader("🚀 Métricas de Rendimiento")
                # Tarjetas grandes y coloridas
                m1, m2, m3 = st.columns(3)
                m1.metric("SALTO CMJ", f"{datos_fatiga.get('CMJ', 0)} cm", delta="Pro")
                m2.metric("VFC (Salud)", f"{datos_fatiga.get('VFC', 0)} ms", delta="Estable")
                m3.metric("RPE (Carga)", f"{datos_fatiga.get('RPE', 0)}/10", delta="-1", delta_color="inverse")
                
                # Gráfico de evolución rápido
                st.markdown("---")
                st.subheader("📈 Tendencia de Salto (CMJ)")
                df_atleta = df_fatiga[df_fatiga['NOMBRE'] == atleta]
                if not df_atleta.empty:
                    st.line_chart(df_atleta.set_index(df_atleta.columns[0])['CMJ'])

            # Tabla completa al final
            st.markdown("---")
            with st.expander("📝 Ver todos los datos del Excel"):
                st.dataframe(df_atleta.style.highlight_max(axis=0, color='#1f2937'))
                
        else:
            st.error("❌ No se encontró la columna 'NOMBRE'. Revisa tu Excel.")
            st.write("Columnas detectadas:", list(df_base.columns))

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
else:
    st.info("👋 Por favor, sube tu archivo Excel para generar la infografía.")
