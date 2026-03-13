import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import io

st.set_page_config(page_title="Dashboard Pro", layout="wide")

# --- FUNCIÓN GENERAR PDF PROFESIONAL ---
def generar_pdf_carta(nombre, cmj, vfc, rpe, fecha):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFillColor(HexColor("#1f77b4"))
    c.rect(0, height-100, width, 100, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height-65, "INFORME DE RENDIMIENTO")
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height-150, f"Atleta: {nombre}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height-175, f"Fecha: {fecha}")
    c.setStrokeColor(HexColor("#1f77b4"))
    c.rect(40, height-400, width-80, 200, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, height-250, "Métricas registradas:")
    c.setFont("Helvetica", 12)
    c.drawString(80, height-280, f"Salto CMJ: {cmj} cm")
    c.drawString(80, height-310, f"VFC: {vfc} ms")
    c.drawString(80, height-340, f"RPE: {rpe} / 10")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFAZ ---
st.title("📊 Dashboard Profesional")
archivo = st.sidebar.file_uploader("Sube tu Excel", type=['xlsx'])

if archivo:
    df_fatiga = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
    df_fatiga.columns = df_fatiga.columns.str.strip()
    
    # Selector de atleta simple para el ejemplo
    nombre = st.selectbox("Selecciona Atleta", df_fatiga['NOMBRE'].unique())
    datos = df_fatiga[df_fatiga['NOMBRE'] == nombre].iloc[-1]
    
    st.metric("Salto CMJ", f"{datos['CMJ']} cm")
    
    # Botón PDF con los datos reales
    pdf_data = generar_pdf_carta(nombre, datos['CMJ'], datos['VFC'], datos['RPE'], "13/03/2026")
    st.download_button("📥 Descargar Informe PDF", pdf_data, f"Informe_{nombre}.pdf", "application/pdf")
else:
    st.info("Sube el archivo Excel para empezar.")
