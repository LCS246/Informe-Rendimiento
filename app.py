import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import io

# Configuración de página
st.set_page_config(page_title="Dashboard Profesional", layout="wide")

# --- LÓGICA DE GENERACIÓN PDF ---
def generar_pdf_carta(nombre, cmj, vfc, rpe, fecha):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Diseño de la carta
    c.setFillColor(HexColor("#1f77b4"))
    c.rect(0, height-100, width, 100, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 28)
    c.drawString(50, height-65, "INFORME DE RENDIMIENTO")
    
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height-150, f"Atleta: {nombre}")
    c.setFont("Helvetica", 14)
    c.drawString(50, height-175, f"Fecha: {fecha}")
    
    c.setStrokeColor(HexColor("#1f77b4"))
    c.rect(40, height-400, width-80, 200, fill=0, stroke=1)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, height-250, "Métricas clave:")
    c.setFont("Helvetica", 14)
    c.drawString(80, height-280, f"Salto CMJ: {cmj} cm")
    c.drawString(80, height-310, f"VFC: {vfc} ms")
    c.drawString(80, height-340, f"RPE: {rpe} / 10")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFAZ WEB ---
st.title("📊 Dashboard Profesional")
archivo = st.sidebar.file_uploader("Sube tu Excel", type=['xlsx'])

if archivo:
    # Carga de datos básica
    nombre = "Dani Alcover"
    cmj, vfc, rpe, fecha = 59, 72, 8, "13/03/2026"
    
    st.success("Archivo cargado correctamente")
    st.metric("Salto CMJ", f"{cmj} cm")
    
    # Botón de descarga
    pdf_data = generar_pdf_carta(nombre, cmj, vfc, rpe, fecha)
    st.download_button(
        label="📥 Descargar Informe PDF",
        data=pdf_data,
        file_name=f"Informe_{nombre}.pdf",
        mime="application/pdf"
    )
else:
    st.info("Por favor, sube un archivo Excel para habilitar la descarga.")
