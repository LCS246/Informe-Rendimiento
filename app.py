import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white, gray
import io

st.set_page_config(page_title="Informe Pro", layout="wide")

# --- FUNCIÓN PDF ESTILO "CARTA DE JUGADOR" ---
def generar_pdf_profesional(nombre, datos):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # 1. Fondo de la "Carta"
    c.setFillColor(HexColor("#f4f4f4"))
    c.rect(50, 400, 500, 350, fill=1, stroke=0)
    
    # 2. Encabezado Azul Profesional
    c.setFillColor(HexColor("#1f77b4"))
    c.rect(50, 700, 500, 50, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(70, 715, "FICHA TÉCNICA DE RENDIMIENTO")
    
    # 3. Nombre del Atleta
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(70, 660, f"ATLETA: {nombre.upper()}")
    c.line(70, 650, 500, 650)
    
    # 4. Datos organizados en columnas
    c.setFont("Helvetica-Bold", 12)
    y = 610
    for col, val in datos.items():
        c.setFillColor(HexColor("#555555"))
        c.drawString(70, y, f"{str(col).upper()}")
        c.setFillColor(black)
        c.setFont("Helvetica", 12)
        c.drawString(250, y, f": {val}")
        c.setFont("Helvetica-Bold", 12)
        y -= 25
        
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFAZ WEB ---
st.title("🏆 PLAYER PERFORMANCE DASHBOARD")
archivo = st.sidebar.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if archivo:
    try:
        df = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
        df.columns = df.columns.str.strip()
        nombre = st.sidebar.selectbox("Selecciona Atleta", df['NOMBRE'].unique())
        datos = df[df['NOMBRE'] == nombre].iloc[-1]
        
        # Diseño en pantalla (Web)
        st.subheader(f"📊 Ficha de: {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Salto (CMJ)", f"{datos['CMJ']} cm")
        c2.metric("VFC", f"{datos['VFC']} ms")
        c3.metric("RPE", f"{datos['RPE']}/10")
        
        st.divider()
        st.table(datos.to_frame(name="Valor"))
        
        # Descarga
        pdf_data = generar_pdf_profesional(nombre, datos)
        st.download_button("📥 Descargar Ficha PDF Pro", pdf_data, f"Ficha_{nombre}.pdf", "application/pdf")
        
    except Exception as e:
        st.error(f"Error: {e}")

