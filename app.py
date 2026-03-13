import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="Dashboard Pro Atleta", layout="wide")

# --- FUNCIONES ---
def get_arrow_st(curr, prev):
    if prev is None or pd.isna(prev) or prev == 0: return ""
    try:
        c, p = float(curr), float(prev)
        pct = abs(round(((c - p) / p) * 100))
        if c > p: return f"▲ (+{pct}%)"
        elif c < p: return f"▼ (-{pct}%)"
        return "➖ (0%)"
    except: return ""

# --- INTERFAZ ---
st.title("📊 Dashboard de Rendimiento")
archivo = st.sidebar.file_uploader("Sube tu Excel 'App_Entrenamiento'", type=['xlsx'])

if archivo:
    try:
        df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
        df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        
        # Limpieza
        df_fatiga['FECHA'] = pd.to_datetime(df_fatiga['FECHA'], dayfirst=True, errors='coerce')
        df_fatiga = df_fatiga.sort_values('FECHA')
        
        lista_clientes = sorted(df_base['NOMBRE'].dropna().unique())
        cliente = st.sidebar.selectbox("👤 Selecciona Atleta:", lista_clientes)
        df_cli = df_fatiga[df_fatiga['NOMBRE'] == cliente].copy()
        
        if not df_cli.empty:
            actual = df_cli.iloc[-1]
            previo = df_cli.iloc[-2] if len(df_cli) > 1 else actual
            
            # Métricas
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Salto CMJ (cm)", f"{actual.get('CMJ', 0)}", get_arrow_st(actual.get('CMJ', 0), previo.get('CMJ', 0)))
            c2.metric("VFC (ms)", f"{actual.get('VFC', 0)}", get_arrow_st(actual.get('VFC', 0), previo.get('VFC', 0)))
            c3.metric("RPE (Intensidad)", f"{actual.get('RPE', 0)}/10")
            
            # ACWR
            df_cli['Carga'] = pd.to_numeric(df_cli.get('RPE', 0), errors='coerce') * pd.to_numeric(df_cli.get('Duración', 0), errors='coerce')
            aguda = df_cli['Carga'].tail(7).mean()
            cronica = df_cli['Carga'].tail(28).mean()
            acwr = round(aguda / cronica, 2) if cronica > 0 else 0
            c4.metric("Ratio ACWR", acwr)

            # Gráficos
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📈 Evolución CMJ")
                fig, ax = plt.subplots()
                ax.plot(df_cli['FECHA'], df_cli['CMJ'], marker='o')
                st.pyplot(fig)
            with col2:
                st.subheader("🩹 Notas")
                perfil = df_base[df_base['NOMBRE'] == cliente].iloc[0]
                st.write(f"**Historial:** {perfil.get('HISTORIAL DE LESIONES', 'Sin datos')}")
                st.write(f"**Precauciones:** {perfil.get('PRECAUCIONES', 'Sin datos')}")
        else:
            st.warning("No hay datos para este atleta.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👋 Sube tu archivo Excel para comenzar.")

