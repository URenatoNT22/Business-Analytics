import streamlit as st
import Controller.clienteController as clienteController
from Controller.models.Cliente import Cliente
from datetime import datetime
import Pages.Cliente.Analisis as PageAnalisis 
from ml import (
    preprocess_and_predict,
    entrenar
    )
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import Controller.resultController as resultController

def Listagem():
    # Verificar o modo atual de visualização
    mode = st.session_state.get('mode', 'list')
    
    if mode == 'list':
        # Mostrar lista de clientes
        st.title("Lista de clientes :clipboard:")
        if st.button('Nuevo'):
            st.session_state.mode = 'create'
            st.experimental_rerun()

        columns = st.columns((1, 1, 1, 1, 1, 1, 1))
        attributes = [':file_folder: ID', ':page_facing_up: Nombre', ':email: age', ':email: sex', ':email: Email', ':calendar: date created', ':x: Opciones']
        
        for col, attr_name in zip(columns, attributes):
            col.write(attr_name)

        clientes = clienteController.read_clientes()
        for cliente in clientes:
            col1, col2, col3, col4, col5, col6, col7 = st.columns((1, 1, 1, 1, 1, 1, 1))
            col1.write(cliente.id)
            col2.write(f"{cliente.first_name} {cliente.last_name}")
            col3.write(str(cliente.age))
            col4.write(cliente.sex)
            col5.write(cliente.email)
            col6.write(cliente.date_created)
            
            buttonDelete = col7.empty()
            editClick = buttonDelete.button('Editar', key='buttonDelete' + str(cliente.id))
            buttonChange = col7.empty()
            deleteClick = buttonChange.button('Eliminar', key='buttonEdit' + str(cliente.id))
            buttonAnalysis = col7.empty()
            analysisClick = buttonAnalysis.button('Analisis', key='buttonAnalysis' + str(cliente.id))

            if editClick:
                st.session_state.mode = 'edit'
                st.session_state.client_id = cliente.id
                st.experimental_rerun()  # Reload para atualizar os parâmetros

            if deleteClick:
                st.session_state.mode = 'delete'
                st.session_state.client_id = cliente.id
                st.experimental_rerun()

            if analysisClick:
                st.session_state.mode = 'analysis'
                st.session_state.client_id = cliente.id
                st.experimental_rerun()

        

    elif mode == 'create':
        # Formulário de criação de novo cliente
        st.title("Crear nuevo cliente :sparkles:")

        if st.button('Regresar'):
            st.session_state.mode = 'list'
            st.experimental_rerun()

        with st.form(key='form_create_cliente'):
            input_first_name = st.text_input(label='Nombres:')
            input_last_name = st.text_input(label='Apellidos:')
            input_DNI = st.text_input(label='DNI:')
            input_email = st.text_input(label='Correo electrónico:')
            input_age = st.number_input(label='Edad:', format='%i', step=1, min_value=18, max_value=120)
            input_gender = st.selectbox('Sexo:', options={'M': 0, 'F': 1})
            input_date_created = st.date_input('Fecha de creación:', value=datetime.datetime.today())

            input_button_submit = st.form_submit_button("Submit")

            if input_button_submit:
                clienteController.create_cliente(Cliente(None, input_first_name, input_last_name, input_DNI, input_email, input_age, input_gender, input_date_created))
                st.success("Sucesso! Cliente cadastrado!")
                st.session_state.mode = 'list'  # Voltar ao modo de lista
                st.experimental_rerun()  # Atualizar a página para mostrar o novo cliente

    elif mode == 'edit':
        client_id = st.session_state.get('client_id')
        cliente = clienteController.select_cliente_by_id(client_id)
        if cliente:
            st.title("Alterar cliente :pencil2:")
            
            with st.form(key='form_edit_cliente'):
                input_first_name = st.text_input(label='Nombres:', value=cliente.first_name)
                input_last_name = st.text_input(label='Apellidos:', value=cliente.last_name)
                input_DNI = st.text_input(label='DNI:', value=cliente.DNI)
                input_email = st.text_input(label='Correo electrónico:', value=cliente.email)
                input_age = st.number_input(label='Edad:', format='%i', step=1, min_value=18, max_value=120, value=cliente.age)
                input_gender = st.selectbox('Sexo:', options=['M', 'F'], index=['M', 'F'].index(cliente.sex))
                input_date_created = st.date_input('Fecha de creación:', value=cliente.date_created)

                input_button_submit = st.form_submit_button("Salvar Alterações")

                

                if input_button_submit:
                    clienteController.update_cliente(Cliente(cliente.id, input_first_name, input_last_name, input_DNI, input_email, input_age, input_gender, input_date_created))
                    st.success("Sucesso! Cliente alterado!")
                    st.session_state.mode = 'list'  # Voltar ao modo de lista
                    st.experimental_rerun()  # Atualizar a página para mostrar as alterações
                if st.form_submit_button('Voltar'):
                    st.session_state.mode = 'list'
                    st.experimental_rerun()
        
    elif mode == 'delete':
        # Confirmar eliminación de cliente
        client_id = st.session_state.get('client_id')
        cliente = clienteController.select_cliente_by_id(client_id)
        if cliente:
            st.title("Eliminar cliente :warning:")
            st.write(f"¿Está seguro de que desea eliminar el cliente {cliente.first_name} {cliente.last_name}? Esta acción no se puede deshacer.")

            if st.button('Confirmar eliminación'):
                clienteController.delete_cliente(client_id)
                st.success("Cliente eliminado exitosamente.")
                st.session_state.mode = 'list'
                st.experimental_rerun()
            
            if st.button('Cancelar'):
                st.session_state.mode = 'list'
                st.experimental_rerun()
    
    elif mode == 'analysis':
        def is_valid_bmi(bmi):
            return 10 <= bmi <= 50

        def is_valid_integer(value, min_value, max_value):
            return min_value <= value <= max_value
        
        client_id = st.session_state.get('client_id')
        cliente = clienteController.select_cliente_by_id(client_id)
        st.title("Hospital Form")
        
        # Asignar los valores de sexo y edad del objeto cliente
        sex = cliente.sex  # Supongamos que 'sex' está en el cliente
        age = cliente.age  # Supongamos que 'age' está en el cliente
        
        # Mapear sexo a valores numéricos
        sex_dict = {"Male": 1, "Female": 2}
        sex_value = sex_dict.get(sex, 0)
        
        # Mapear edad a categorías
        if age >= 18 and age <= 24:
            age_category = "18-24"
        elif age >= 25 and age <= 29:
            age_category = "25-29"
        elif age >= 30 and age <= 34:
            age_category = "30-34"
        elif age >= 35 and age <= 39:
            age_category = "35-39"
        elif age >= 40 and age <= 44:
            age_category = "40-44"
        elif age >= 45 and age <= 49:
            age_category = "45-49"
        elif age >= 50 and age <= 54:
            age_category = "50-54"
        elif age >= 55 and age <= 59:
            age_category = "55-59"
        elif age >= 60 and age <= 64:
            age_category = "60-64"
        elif age >= 65 and age <= 69:
            age_category = "65-69"
        elif age >= 70 and age <= 74:
            age_category = "70-74"
        elif age >= 75 and age <= 79:
            age_category = "75-79"
        elif age >= 80:
            age_category = "80 or older"
        else:
            age_category = "Select..."
        
        # General Health
        gen_health = st.selectbox("General Health:", ["Select...", "Excellent", "Very Good", "Good", "Fair", "Poor"])
        if gen_health == "Select...":
            st.error("Please select an option for general health.")
        
        # BMI
        bmi = st.number_input("BMI (10-50):", min_value=10.0, max_value=50.0, step=0.1)
        if not is_valid_bmi(bmi):
            st.error("Invalid BMI. Please enter a number between 10 and 50.")

        # Smoking
        smoking = st.selectbox("Do you smoke?", ["Select...", "Yes", "No"])
        if smoking == "Select...":
            st.error("Please select an option for smoking.")

        # Alcohol Drinking
        alcohol_drinking = st.selectbox("Do you drink alcohol?", ["Select...", "Yes", "No"])
        if alcohol_drinking == "Select...":
            st.error("Please select an option for alcohol drinking.")

        # Stroke
        stroke = st.selectbox("Have you ever had a stroke?", ["Select...", "Yes", "No"])
        if stroke == "Select...":
            st.error("Please select an option for stroke.")

        # Physical Health
        physical_health = st.number_input("Days of bad physical health in the past month (0-30):", min_value=0, max_value=30, step=1)
        if not is_valid_integer(physical_health, 0, 30):
            st.error("Invalid number. Please enter an integer between 0 and 30.")

        # Mental Health
        mental_health = st.number_input("Days of bad mental health in the past month (0-30):", min_value=0, max_value=30, step=1)
        if not is_valid_integer(mental_health, 0, 30):
            st.error("Invalid number. Please enter an integer between 0 and 30.")

        # Difficulty Walking
        diff_walking = st.selectbox("Do you have difficulty walking?", ["Select...", "Yes", "No"])
        if diff_walking == "Select...":
            st.error("Please select an option for difficulty walking.")

        """ # Sex
        sex = st.selectbox("Sex:", ["Select...", "Male", "Female"])
        if sex == "Select...":
            st.error("Please select an option for sex.")

        # Age Category
        age_category = st.selectbox("Age Category:", ["Select...", "18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
        if age_category == "Select...":
            st.error("Please select an age category.") """

        # Race
        race = st.selectbox("Race:", ["Select...", "White", "Black", "Asian", "Other"])
        if race == "Select...":
            st.error("Please select a race.")

        # Diabetic
        diabetic = st.selectbox("Are you diabetic?", ["Select...", "Yes", "No"])
        if diabetic == "Select...":
            st.error("Please select an option for diabetic.")

        # Physical Activity
        physical_activity = st.selectbox("Do you engage in physical activity?", ["Select...", "Yes", "No"])
        if physical_activity == "Select...":
            st.error("Please select an option for physical activity.")

        # Sleep Time
        sleep_time = st.number_input("Hours of sleep per night (0-24):", min_value=0, max_value=24, step=1)
        if not is_valid_integer(sleep_time, 0, 24):
            st.error("Invalid number. Please enter an integer between 0 and 24.")

        # Asthma
        # asthma = st.selectbox("Do you have asthma?", ["Select...", "Yes", "No"])
        # if asthma == "Select...":
        #     st.error("Please select an option for asthma.")

        # Kidney Disease
        kidney_disease = st.selectbox("Do you have kidney disease?", ["Select...", "Yes", "No"])
        if kidney_disease == "Select...":
            st.error("Please select an option for kidney disease.")

        # Skin Cancer
        cholesterol = st.selectbox("Do you have High Cholesterol?", ["Select...", "Yes", "No"])
        if cholesterol == "Select...":
            st.error("Please select an option for cholesterol.")

        if st.button("Enviar Form"):
            # Convert categorical data to numerical for the DataFrame
            smoking = 1 if smoking == "Yes" else 0
            alcohol_drinking = 1 if alcohol_drinking == "Yes" else 0
            stroke = 1 if stroke == "Yes" else 0
            diff_walking = 1 if diff_walking == "Yes" else 0
            # sex = 1 if sex == "Male" else 2
            sex = sex_value
            age_category_dict = {"18-24": 1, "25-29": 2, "30-34": 3, "35-39": 4, "40-44": 5, "45-49": 6, "50-54": 7, "55-59": 8, "60-64": 9, "65-69": 10, "70-74": 11, "75-79": 12, "80 or older": 13}
            age_category = age_category_dict.get(age_category, 0)
            race_dict = {"White": 1, "Black": 2, "Other race only": 3, "Multiracial": 4,"Hispanic": 5}
            race = race_dict.get(race, 0)
            diabetic_dict = {"Yes": 1, "No": 3, "Borderline diabetes": 4, "During pregnancy": 2}
            diabetic = diabetic_dict.get(diabetic, 0)
            physical_activity = 1 if physical_activity == "Yes" else 0
            gen_health_dict = {"Excellent": 1, "Very Good": 2, "Good": 3, "Fair": 4, "Poor": 5}
            gen_health = gen_health_dict.get(gen_health, 0)
            # asthma = 1 if asthma == "Yes" else 0
            kidney_disease = 1 if kidney_disease == "Yes" else 0
            cholesterol = 1 if cholesterol == "Yes" else 0

            # Create the DataFrame
            new_data = pd.DataFrame({
                'Sex': [sex],
                'GeneralHealth': [gen_health],
                'PhysicalHealthDays': [physical_health],
                'MentalHealthDays': [mental_health],
                'PhysicalActivities': [physical_activity],
                'SleepHours': [sleep_time],
                'HadStroke': [stroke],
                'HadKidneyDisease': [kidney_disease],
                'HadDiabetes': [diabetic],
                'DifficultyWalking': [diff_walking],
                'SmokerStatus': [smoking],
                'RaceEthnicityCategory': [race],
                'AgeCategory': [age_category],
                'BMI': [bmi],
                'AlcoholDrinkers': [alcohol_drinking],
                
                'HadHighBloodCholesterol': [cholesterol]
                # 'SkinCancer': [cholesterol]
            })

            # Realizar la predicción
            result, impacto_df, resultInt = preprocess_and_predict(new_data)
            st.write(result)

            # Crear la figura y el eje
            fig, ax = plt.subplots(figsize=(10, 6))

            # Crear el gráfico de barras
            ax.barh(impacto_df['Feature'], impacto_df['Impact'], color='#4C72B0')
            ax.set_xlabel('Importance')
            ax.set_title('Feature Impact')
            ax.invert_yaxis()
            st.pyplot(fig)
            date_registration = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            resultController.create_result_data(new_data,resultInt,date_registration,client_id)

        if st.button('Cancelar'):
            st.session_state.mode = 'list'
            st.experimental_rerun()
