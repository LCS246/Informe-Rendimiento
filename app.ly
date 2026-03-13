import streamlit as st
st.title("🏃‍♂️ Mi Primer Informe de Atleta")
nombre = st.text_input("Nombre del atleta:")
if nombre:
    st.write(f"Generando informe para: {nombre}")
