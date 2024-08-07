import streamlit as st
import Pages.Cliente.Analisis as PageAnalisis 
import Pages.Cliente.Listagem as PageListar 

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('Sistema de clientes :busts_in_silhouette:')
st.sidebar.title(':page_facing_up: Menu')
sidebarOptions = st.sidebar.selectbox('Cliente', ['Client','Result']) 

if sidebarOptions == 'Client':
    PageListar.Listagem()

if sidebarOptions == 'Result':
    PageAnalisis.Resultados()