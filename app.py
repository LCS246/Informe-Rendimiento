import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import base64
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Dashboard Pro Atleta", layout="wide")

# --- FUNCIONES DE AYUDA (Tus flechas) ---
def get_arrow_st(curr, prev, tipo):
    if prev is None or pd.isna(prev) or prev == 0: return ""
    try: c, p = float(curr), float(prev)
    except: return ""
    pct = abs(round(((c - p) / p) * 100))
    if c > p: return f"▲ (+{pct}%)"
    elif c < p: return f"▼ (-{pct}%)"
    return "➖ (0%)"

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

        # --- LÓGICA DE CÁLCULO (Tu Bloque 2) ---
        df_cli = df_fatiga[df_fatiga['NOMBRE'] == cliente].copy()
        
        if not df_cli.empty:
            st.title(f"📊 Dashboard de Rendimiento: {cliente}")
            
            # Métricas actuales vs anteriores (Simuladas de la última semana)
            # Nota: Aquí calculamos los valores para tus flechas
            actual = df_cli.iloc[-1]
            previo = df_cli.iloc[-2] if len(df_cli) > 1 else actual
            
            # --- FILA 1: MÉTRICAS CLAVE ---
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                cmj = actual.get('CMJ', 0)
                flecha = get_arrow_st(cmj, previo.get('CMJ', 0), 'rendimiento')
                st.metric("Salto CMJ (cm)", f"{cmj}", flecha)
                
            with c2:
                vfc = actual.get('VFC', 0)
                flecha_vfc = get_arrow_st(vfc, previo.get('VFC', 0), 'rendimiento')
                st.metric("VFC (ms)", f"{vfc}", flecha_vfc)
            
            with c3:
                rpe = actual.get('RPE', 0)
                st.metric("RPE (Intensidad)", f"{rpe}/10")

            with c4:
                # Cálculo rápido de ACWR
                df_cli['Carga'] = pd.to_numeric(df_cli['RPE'], errors='coerce') * pd.to_numeric(df_cli['Duración'], errors='coerce')
                aguda = df_cli['Carga'].tail(7).sum()
                cronica = df_cli['Carga'].tail(28).mean() * 7
                acwr = round(ag
