import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from docxtpl import DocxTemplate
import io

# Configuración de página
st.set_page_config(page_title="App Entrenamiento Atletas", layout="wide")

# ==========================================
# 1. CONEXIÓN A DATOS (SIMULADA PARA WEB)
# ==========================================
# NOTA: Para producción real con Google Sheets, se usa st.connection("gsheets")
# Aquí adaptamos tu lógica de limpieza para que funcione con archivos subidos
st.sidebar.title("Configuración")
archivo_subido = st.sidebar.file_uploader("Sube tu Excel o CSV de entrenamiento", type=['xlsx', 'csv'])

if archivo_subido:
    # Leer datos (aquí asumimos que subes el Excel con las pestañas que mencionaste)
    @st.cache_data
    def cargar_datos(file):
        df_b = pd.read_excel(file, sheet_name='Base Clientes')
        df_e = pd.read_excel(file, sheet_name='Registro de entrenamiento')
        df_f = pd.read_excel(file, sheet_name='Fatiga y Bienestar')
        return df_b, df_e, df_f

    try:
        df_base, df_entreno, df_fatiga = cargar_datos(archivo_subido)
        
        # --- LIMPIEZA (Tu Bloque 1) ---
        for df in [df_base, df_entreno, df_fatiga]:
            df.columns = df.columns.str.strip()
        
        df_entreno['FECHA'] = pd.to_datetime(df_entreno['FECHA'], dayfirst=True, errors='coerce')
        df_fatiga['FECHA'] = pd.to_datetime(df_fatiga['FECHA'], dayfirst=True, errors='coerce')
        df_entreno = df_entreno.dropna(subset=['FECHA'])
        df_fatiga = df_fatiga.dropna(subset=['FECHA'])
        
        st.sidebar.success("✅ Datos cargados")

        # --- INTERFAZ (Tu Bloque 2) ---
        st.title("🏃‍♂️ Panel de Rendimiento y Fatiga")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            lista_clientes = sorted(df_base['NOMBRE'].dropna().unique())
            cliente = st.selectbox("👤 Selecciona Atleta:", lista_clientes)
        with col2:
            pestana = st.selectbox("📋 Tipo de Informe:", ['Fatiga y Bienestar', 'Registro de entrenamiento'])
        with col3:
            rango = st.selectbox("📅 Rango Temporal:", ['Todo el histórico', 'Última semana', 'Último mes'])

        # Filtrado
        df_f_cli = df_fatiga[df_fatiga['NOMBRE'] == cliente].copy().sort_values('FECHA')
        
        # --- CÁLCULOS (Tu Bloque 3) ---
        if not df_f_cli.empty:
            # Cálculos de Carga
            df_f_cli['RPE'] = pd.to_numeric(df_f_cli['RPE'], errors='coerce').fillna(0)
            df_f_cli['Duración'] = pd.to_numeric(df_f_cli['Duración'], errors='coerce').fillna(0)
            df_f_cli['Carga_Sesion'] = df_f_cli['RPE'] * df_f_cli['Duración']
            
            ultima_fecha = df_f_cli['FECHA'].max()
            carga_aguda = df_f_cli[df_f_cli['FECHA'] > ultima_fecha - timedelta(days=7)]['Carga_Sesion'].sum()
            carga_cronica = df_f_cli[df_f_cli['FECHA'] > ultima_fecha - timedelta(days=28)]['Carga_Sesion'].sum() / 4
            acwr = round(carga_aguda / carga_cronica, 2) if carga_cronica > 0 else 0
            
            # --- VISUALIZACIÓN ---
            tab1, tab2 = st.tabs(["📊 Gráficos en Pantalla", "📄 Exportar Reporte"])
            
            with tab1:
                st.metric("Ratio ACWR (Carga)", acwr)
                if acwr > 1.5: st.error("⚠️ Riesgo de lesión alto")
                elif acwr >= 0.8: st.success("🟢 Zona segura")
                
                var_grafica = st.selectbox("Ver evolución de:", ['RPE', 'CMJ', 'VFC'])
                if var_grafica in df_f_cli.columns:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(df_f_cli['FECHA'], pd.to_numeric(df_f_cli[var_grafica], errors='coerce'), marker='o', color='green')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

            with tab2:
                st.info("Para generar el Word, asegúrate de tener la plantilla.")
                plantilla_file = st.file_uploader("Sube tu plantilla Word (.docx)", type=['docx'])
                if plantilla_file and st.button("Generar y Descargar Word"):
                    doc = DocxTemplate(plantilla_file)
                    # Aquí usamos tus cálculos
                    contexto = {
                        'nombre_cliente': cliente,
                        'acwr': acwr,
                        'carga_aguda': carga_aguda,
                        'vfc_actual': df_f_cli['VFC'].iloc[-1] if 'VFC' in df_f_cli.columns else "N/A"
                    }
                    doc.render(contexto)
                    bio = io.BytesIO()
                    doc.save(bio)
                    st.download_button(label="📥 Descargar Informe", data=bio.getvalue(), file_name=f"Informe_{cliente}.docx")
        else:
            st.warning("No hay datos para este atleta.")

    except Exception as e:
        st.error(f"Error leyendo el archivo: {e}. Revisa que las pestañas se llamen igual que en el código.")
else:
    st.info("👋 ¡Bienvenido! Por favor, sube el archivo Excel con los datos de entrenamiento en la barra lateral.")
