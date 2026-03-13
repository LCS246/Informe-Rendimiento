import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# Configuración de página
st.set_page_config(page_title="Dashboard Pro Atleta", layout="wide")

# --- FUNCIONES DE AYUDA (Tus flechas) ---
def get_arrow_st(curr, prev):
    if prev is None or pd.isna(prev) or prev == 0: return ""
    try:
        c, p = float(curr), float(prev)
        pct = abs(round(((c - p) / p) * 100))
        if c > p: return f"▲ (+{pct}%)"
        elif c < p: return f"▼ (-{pct}%)"
        return "➖ (0%)"
    except: return ""

# --- INTERFAZ LATERAL ---
st.sidebar.title("🚀 Control de Datos")
archivo = st.sidebar.file_uploader("Sube tu Excel 'App_Entrenamiento'", type=['xlsx'])

if archivo:
    try:
        # Cargar pestañas
        df_base = pd.read_excel(archivo, sheet_name='Base Clientes')
        df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        
        # Limpieza básica
        df_base.columns = df_base.columns.str.strip()
        df_fatiga.columns = df_fatiga.columns.str.strip()
        df_fatiga['FECHA'] = pd.to_datetime(df_fatiga['FECHA'], dayfirst=True, errors='coerce')
        df_fatiga = df_fatiga.dropna(subset=['FECHA']).sort_values('FECHA')

        # Selector de Cliente
        lista_clientes = sorted(df_base['NOMBRE'].dropna().unique())
        cliente = st.sidebar.selectbox("👤 Selecciona Atleta:", lista_clientes)

        # Filtrar datos del cliente
        df_cli = df_fatiga[df_fatiga['NOMBRE'] == cliente].copy()
        
        if not df_cli.empty:
            st.title(f"📊 Dashboard de Rendimiento: {cliente}")
            
            # Datos actuales y previos
            actual = df_cli.iloc[-1]
            previo = df_cli.iloc[-2] if len(df_cli) > 1 else actual
            
            # --- FILA 1: RÉCORD DE DATOS (MÉTRICAS NATIVAS) ---
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                cmj = actual.get('CMJ', 0)
                flecha = get_arrow_st(cmj, previo.get('CMJ', 0))
                st.metric("Salto CMJ (cm)", f"{cmj}", flecha)
                
            with c2:
                vfc = actual.get('VFC', 0)
                flecha_vfc = get_arrow_st(vfc, previo.get('VFC', 0))
                st.metric("VFC (ms)", f"{vfc}", flecha_vfc)
            
            with c3:
                rpe = actual.get('RPE', 0)
                st.metric("RPE (Intensidad)", f"{rpe}/10")

            with c4:
                # Cálculo rápido de ACWR
                df_cli['Carga'] = pd.to_numeric(df_cli.get('RPE', 0), errors='coerce') * pd.to_numeric(df_cli.get('Duración', 0), errors='coerce')
                aguda = df_cli['Carga'].tail(7).sum()
                cronica = df_cli['Carga'].tail(28).mean() * 7
                acwr = round(aguda/cronica, 2) if cronica > 0 else 0
                st.metric("Ratio ACWR", acwr)

            # --- FILA 2: GRÁFICOS (EN COLUMNAS) ---
            st.markdown("---")
            col_izq, col_der = st.columns(2)
            
            with col_izq:
                st.subheader("📈 Evolución Longitudinal CMJ")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(df_cli['FECHA'], df_cli['CMJ'], marker='o', color='#1f77b4')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            with col_der:
                st.subheader("🎯 Cuadrante Readiness (Últimos 5 días)")
                # Gráfico de dispersión simple para la web
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                ax2.scatter(df_cli['VFC'].tail(5), df_cli['CMJ'].tail(5), s=100, color='orange')
                ax2.set_xlabel("VFC")
                ax2.set_ylabel("CMJ")
                ax2.grid(True, alpha=0.3)
                st.pyplot(fig2)

            # --- NOTAS MÉDICAS Y PRECAUCIONES ---
            perfil = df_base[df_base['NOMBRE'] == cliente].iloc[0]
            with st.expander("🩹 Ver Notas Médicas y Precauciones"):
                st.write(f"**Historial de Lesiones:** {perfil.get('HISTORIAL DE LESIONES', 'Ninguno')}")
                st.write(f"**Precauciones:** {perfil.get('PRECAUCIONES', 'Ninguna')}")

        else:
            st.warning("El atleta seleccionado no tiene registros en 'Fatiga y Bienestar'.")

    except Exception as e:
        st.error(f"Error al procesar el Excel: {e}")
else:
    st.info("Por favor, sube el archivo Excel para activar el Dashboard Pro.")
