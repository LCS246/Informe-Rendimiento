import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración visual estilo "Oscuro/Premium"
st.set_page_config(page_title="Apex Reports Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border: 1px solid #3b82f6; padding: 20px; border-radius: 15px; }
    .player-card { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 25px; border-radius: 20px; border: 1px solid #374151; }
    .injury-alert { background-color: #450a0a; border: 1px solid #f87171; padding: 10px; border-radius: 10px; color: #fca5a5; }
    h1, h2, h3 { font-family: 'Trebuchet MS'; }
    </style>
    """, unsafe_allow_html=True)

# 2. Título principal
st.title("🏆 APEX REPORTS: PLAYER INFOGRAPHIC")

archivo = st.sidebar.file_uploader("📂 Sube el Excel de Apex", type=['xlsx'])

if archivo:
    try:
        # Carga de datos (usando los nombres de tus hojas detectadas)
        df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
        # Usamos la hoja de bienestar que tu sistema detectó
        df_wellness = pd.read_excel(archivo, sheet_name='Respuestas de formulario 1')
        
        # Limpieza estándar
        df_base.columns = df_base.columns.str.strip().str.upper()
        df_wellness.columns = df_wellness.columns.str.strip().str.upper()
        
        # Selector de Atleta
        lista_atletas = sorted(df_base['NOMBRE'].dropna().unique())
        atleta_sel = st.sidebar.selectbox("👤 Seleccionar Atleta", lista_atletas)
        
        # Filtrar datos
        user_base = df_base[df_base['NOMBRE'] == atleta_sel].iloc[0]
        user_well = df_wellness[df_wellness['NOMBRE'] == atleta_sel].iloc[-1] # Último registro

        # --- DISEÑO DE INFOGRAFÍA ---
        col_foto, col_stats = st.columns([1, 2.5])

        with col_foto:
            # Placeholder de foto (aquí podrías poner una imagen real)
            st.markdown(f"""
            <div class="player-card">
                <div style="text-align: center;">
                    <img src="https://via.placeholder.com/200x200.png?text=FOTO" style="border-radius: 50%; border: 4px solid #3b82f6; margin-bottom: 15px;">
                    <h2 style="margin:0;">{atleta_sel}</h2>
                    <p style="color: #9ca3af;">Atleta Apex</p>
                </div>
                <hr style="border: 0.5px solid #374151;">
                <p><b>🎂 EDAD:</b> {user_base.get('EDAD', 'N/A')} años</p>
                <p><b>⚖️ PESO:</b> {user_base.get('PESO', 'N/A')} kg</p>
                <div class="injury-alert">
                    <b>⚠️ HISTORIAL:</b><br>{user_base.get('HISTORIAL DE LESIONES', 'Ninguno')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_stats:
            st.subheader("📊 Estado de Forma Actual")
            
            # Métricas estilo "Messi"
            m1, m2, m3 = st.columns(3)
            
            # Intentamos sacar datos de tu hoja de wellness (ajusta los nombres si cambian)
            m1.metric("ÍNDICE WELLNESS", f"{user_well.get('PUNTUACIÓN WELLNESS', 'N/A')}%", "Óptimo")
            m2.metric("SUEÑO (H)", f"{user_well.get('SUEÑO', 'N/A')}h", "Descanso")
            m3.metric("RPE MEDIO", f"{user_well.get('RPE', 'N/A')}/10", "-1.5", delta_color="inverse")

            st.markdown("---")
            
            # Gráfico de evolución (Si hay columna de fecha)
            col_fecha = 'MARCA TEMPORAL' if 'MARCA TEMPORAL' in df_wellness.columns else df_wellness.columns[0]
            df_hist = df_wellness[df_wellness['NOMBRE'] == atleta_sel]
            
            st.subheader("📈 Evolución Wellness (Últimos registros)")
            st.line_chart(df_hist.set_index(col_fecha).tail(10)[['SUEÑO']])

            # Tabla profesional
            with st.expander("📋 Ver Detalles Técnicos"):
                st.dataframe(df_hist.tail(5), use_container_width=True)

    except Exception as e:
        st.error(f"Error al procesar: {e}")
        st.info("Asegúrate de que las columnas 'NOMBRE', 'SUEÑO' y 'EDAD' existan.")
else:
    st.info("👋 Sube tu archivo Excel para generar la infografía automáticamente.")
