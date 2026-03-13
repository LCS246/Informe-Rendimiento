import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
import io

st.set_page_config(page_title="Dashboard Pro", layout="wide")

# --- FUNCIÓN PDF PROFESIONAL ---
def generar_pdf_completo(nombre, datos):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFillColor(HexColor("#1f77b4"))
    c.rect(0, height-80, width, 80, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height-50, f"INFORME DE RENDIMIENTO: {nombre.upper()}")
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica", 12)
    y = height - 120
    for col in datos.index:
        c.drawString(50, y, f"{col}: {datos[col]}")
        y -= 20
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- INTERFAZ WEB ---
st.title("🏆 PLAYER PERFORMANCE DASHBOARD")
archivo = st.sidebar.file_uploader("Sube tu Excel", type=['xlsx'])

if archivo:
    df = pd.read_excel(archivo, sheet_name='Fatiga y Bienestar')
    df.columns = df.columns.str.strip()
    nombre = st.sidebar.selectbox("Selecciona Atleta", df['NOMBRE'].unique())
    datos = df[df['NOMBRE'] == nombre].iloc[-1]
    
    # Diseño de "Tarjeta" en pantalla
    with st.container():
        st.markdown(f"## 👤 {nombre}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Salto (CMJ)", f"{datos['CMJ']} cm")
        c2.metric("VFC", f"{datos['VFC']} ms")
        c3.metric("RPE", f"{datos['RPE']}/10")
        # Aquí puedes añadir más métricas según tu Excel
        
    st.divider()
    st.subheader("📋 Datos Completos")
    st.dataframe(datos.to_frame(), use_container_width=True)
    
    # PDF
    pdf_data = generar_pdf_completo(nombre, datos)
    st.download_button("📥 Descargar Informe Completo PDF", pdf_data, f"Informe_{nombre}.pdf", "application/pdf")
else:
    st.info("Sube tu archivo para ver el panel de control.")

