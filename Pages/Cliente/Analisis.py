import streamlit as st
import Controller.clienteController as clienteController
import Controller.resultController as resultController
from datetime import datetime

def Resultados():
    # Verificar el modo actual de visualización
    mode = st.session_state.get('mode', 'result')
    
    if mode == 'result':
        # Mostrar lista de resultados de datos
        st.title("Lista de resultados de datos :clipboard:")
        results = resultController.read_results_data()
        columns = st.columns((1, 1, 1, 1, 1))
        result_attributes = ['ID', 'HeartDisease', 'Sex', 'Client', 'dateRegistration']
        
        for col, attr_name in zip(columns, result_attributes):
            col.write(attr_name)

        for result in results:
            """ st.write(f"Tipo de result.client_id: {type(result.client_id)}")
            st.write(f"Valor de result.client_id: {result.client_id}") """
            client = clienteController.select_cliente_by_id(int(result.client_id))
            col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 1, 1))
            col1.write(result.id)
            col2.write("Yes" if result.HeartDisease == 1 else "No")
            col3.write("M" if result.Sex == 1 else "F")
            
            if client:
                col4.write(client.first_name)
            else:
                col4.write("Cliente no encontrado")
                
            col5.write(result.dateRegistration)
