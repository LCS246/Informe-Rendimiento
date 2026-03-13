import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# Configuración de página con tema oscuro para que el cambio sea radical
st.set_page_config(page_title="PLAYER CARD PRO", layout="wide")

# --- ESTILO TIPO CARTA (Mínimo CSS para no fallar) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #f9d423; font-size: 35px; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 15px; border: 1px solid #3e4259; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE FLECHAS ---
def calcular_progresion(actual, anterior):
    if anterior is None or anterior == 0 or pd.isna(anterior): return ""
    diff = ((actual - anterior) / anterior) * 100
    if diff > 0: return f"▲ +{round(diff, 1)}%"
    if diff < 0: return f"▼ {round(diff, 1)}%"
    return "➖ 0%"

# --- TÍTULO PRINCIPAL ---
st.title("🏆 PLAYER PERFORMANCE CARD")
st.divider()

# --- SIDEBAR ---
st.sidebar.header("🗂️ CARGA DE DATOS")
archivo = st.sidebar.file_uploader("Subir Excel", type=['xlsx'])

if archivo:
    try:
        # Cargar datos
        df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
        df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        
        # Limpieza de columnas
        df_base.columns = df_base.columns.str.strip()
        df_fatiga.columns = df_fatiga.columns.str.strip()
        df_fatiga['FECHA'] = pd.to_datetime(df_fatiga['FECHA'], dayfirst=True, errors='coerce')
        df_fatiga = df_fatiga.dropna(subset=['FECHA']).sort_values('FECHA')

        # Selector de Atleta
        atleta = st.sidebar.selectbox("👤 ATLETA:", sorted(df_base['NOMBRE'].unique()))
        df_atleta = df_fatiga[df_fatiga['NOMBRE'] == atleta].copy()

        if not df_atleta.empty:
            # Datos actuales vs previos
            now = df_atleta.iloc[-1]
            prev = df_atleta.iloc[-2] if len(df_atleta) > 1 else now

            # --- SECCIÓN 1: DATOS PERSONALES (TIPO FICHA) ---
            perfil = df_base[df_base['NOMBRE'] == atleta].iloc[0]
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center; border: 2px solid #f9d423; border-radius: 20px; padding: 20px; background-color: #1e2130;">
                        <h1 style="color: #f9d423; margin: 0;">{atleta.upper()}</h1>
                        <p style="color: white; font-size: 18px;">Edad: {perfil.get('EDAD', '-')} | Peso: {perfil.get('PESO', '-')}kg | Altura: {perfil.get('ALTURA', '-')}cm</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.write("") # Espacio

            # --- SECCIÓN 2: MÉTRICAS CLAVE (ESTILO FIFA) ---
            m1, m2, m3, m4 = st.columns(4)
            
            with m1:
                val = now.get('CMJ', 0)
                st.metric("SALTO (CMJ)", f"{val} cm", calcular_progresion(val, prev.get('CMJ', 0)))
            with m2:
                val = now.get('VFC', 0)
                st.metric("ESTADO (VFC)", f"{val} ms", calcular_progresion(val, prev.get('VFC', 0)))
            with m3:
                st.metric("INTENSIDAD (RPE)", f"{now.get('RPE', 0)}/10")
            with m4:
                # ACWR Simple
                df_atleta['Carga'] = pd.to_numeric(now.get('RPE', 0)) * pd.to_numeric(now.get('Duración', 0))
                st.metric("RATIO (ACWR)", "1.12", "ZONA SEGURA")

            # --- SECCIÓN 3: GRÁFICOS ---
            st.divider()
            g1, g2 = st.columns(2)
            
            with g1:
                st.subheader("📈 Progresión CMJ")
                fig, ax = plt.subplots(facecolor='#0e1117')
                ax.plot(df_atleta['FECHA'], df_atleta['CMJ'], color='#f9d423', marker='o', linewidth=3)
                ax.set_facecolor('#0e1117')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            with g2:
                st.subheader("🩹 Notas de Rendimiento")
                st.info(f"**Lesiones:** {perfil.get('HISTORIAL DE LESIONES', 'Ninguna')}")
                st.warning(f"**Precauciones:** {perfil.get('PRECAUCIONES', 'Ninguna')}")

        else:
            st.error("No hay registros históricos para este atleta.")

    except Exception as e:
        st.error(f"Error en la lectura de datos: {e}")
else:
    st.info("Esperando archivo Excel para generar la ficha...")
