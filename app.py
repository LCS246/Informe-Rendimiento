import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
import io

# Configuración inicial
st.set_page_config(page_title="Dashboard Pro", layout="wide")

# --- FUNCIÓN PDF PROFESIONAL ---
def generar_pdf_profesional(nombre, datos):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Diseño de Cabecera
    c.setFillColor(HexColor("#1f77b4"))
    c.rect(0, height-80, width, 80, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30, height-55, "INFORME DE RENDIMIENTO")
    
    # Detalles del atleta
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, height-130, f"ATLETA: {nombre.upper()}")
    c.line(30, height-135, 550, height-135)
    
    # Cuerpo de datos
    c.setFont("Helvetica-Bold", 14)
    y = height - 170
    for col, val in datos.items():
        c.setFillColor(HexColor("#1f77b4"))
        c.drawString(50, y, f"{str(col).upper()}:")
        c.setFillColor(black)
        c.setFont("Helvetica", 14)
        c.drawString(200, y, f"{val}")
        c.setFont("Helvetica-Bold", 14)
        y -= 30
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFAZ ---
st.title("🏆 PLAYER PERFORMANCE DASHBOARD")

archivo = st.sidebar.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if archivo:
    try:
        # Cargar datos
        df = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        df.columns = df.columns.str.strip()
        
        # Selección
        nombre = st.sidebar.selectbox("Selecciona Atleta", df['NOMBRE'].unique())
        datos = df[df['NOMBRE'] == nombre].iloc[-1]
        
        # Visualización de Tarjetas (estilo profesional)
        st.subheader(f"📊 Ficha de: {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Salto (CMJ)", f"{datos['CMJ']} cm")
        c2.metric("VFC", f"{datos['VFC']} ms")
        c3.metric("RPE", f"{datos['RPE']}/10")
        
        st.markdown("---")
        st.subheader("📋 Datos Técnicos Completos")
        st.table(datos.to_frame(name="Valor"))
        
        # Descarga
        pdf_data = generar_pdf_profesional(nombre, datos)
        st.download_button("📥 Descargar Informe Profesional", pdf_data, f"Informe_{nombre}.pdf", "application/pdf")
        
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
else:
    st.info("👋 Por favor, sube tu archivo Excel en la barra lateral.")

