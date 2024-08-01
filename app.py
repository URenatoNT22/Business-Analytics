import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ml import preprocess_and_predict, entrenar
import joblib
from PIL import Image
from datetime import datetime

# scaler = joblib.load('scaler.joblib')
# xgb = joblib.load('xgb_model.joblib')

SEX = {1: 'Male', 2: 'Female'}

GEN_HEALTH = {
    1: "Excellent",
    2: "Very good",
    3: "Good",
    4: "Fair",
    5: "Poor"
}

PHYS_MEN_HEALTH = {77: np.nan, 88: 0, 99: np.nan}

YES_NO_QUESTIONS = {1: 'Yes', 2: 'No'}

SLEEP_TIME = lambda x: np.where(x > 24, np.nan, x)

DIABETES = {
    1: "Yes",
    2: "Yes, but only during pregnancy (female)",
    3: "No",
    4: "No, pre-diabetes or borderline diabetes",
}

SMOKER_STATUS = {
    1: "Current smoker - now smokes every day",
    2: "Current smoker - now smokes some days",
    3: "Former smoker",
    4: "Never smoked"
}

RACE = {
    1: "White only, Non-Hispanic",
    2: "Black only, Non-Hispanic",
    3: "Other race only, Non-Hispanic",
    4: "Multiracial, Non-Hispanic",
    5: "Hispanic"
}

AGE_CATEGORY = {
    1: "Age 18 to 24",
    2: "Age 25 to 29",
    3: "Age 30 to 34",
    4: "Age 35 to 39",
    5: "Age 40 to 44",
    6: "Age 45 to 49",
    7: "Age 50 to 54",
    8: "Age 55 to 59",
    9: "Age 60 to 64",
    10: "Age 65 to 69",
    11: "Age 70 to 74",
    12: "Age 75 to 79",
    13: "Age 80 or older"
}

def is_valid_bmi(bmi):
    return 10 <= bmi <= 50

def is_valid_integer(value, min_value, max_value):
    return min_value <= value <= max_value

def save_to_database(data):
    conn = sqlite3.connect('data_recovery.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO patient_data (
            Sex, GeneralHealth, PhysicalHealthDays, MentalHealthDays, PhysicalActivities, 
            SleepHours, HadStroke, HadKidneyDisease, HadDiabetes, DifficultyWalking, 
            SmokerStatus, RaceEthnicityCategory, AgeCategory, BMI, AlcoholDrinkers, 
            HadHighBloodCholesterol, dateRegistration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
    ''', (
        data['Sex'][0], data['GeneralHealth'][0], data['PhysicalHealthDays'][0], data['MentalHealthDays'][0], data['PhysicalActivities'][0],
        data['SleepHours'][0], data['HadStroke'][0], data['HadKidneyDisease'][0], data['HadDiabetes'][0], data['DifficultyWalking'][0],
        data['SmokerStatus'][0], data['RaceEthnicityCategory'][0], data['AgeCategory'][0], data['BMI'][0], data['AlcoholDrinkers'][0],
        data['HadHighBloodCholesterol'][0]
    ))
    
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect('data_recovery.db')
    query = 'SELECT * FROM patient_data'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    tab1, tab2 = st.tabs(["Formulario de Predicción", "Datos Registrados"])

    with tab1:
        st.title("Heart Disease Prediction Form")

        image = Image.open("./LogoForm.png")
        resized_image = image.resize((300, 200))
        st.image(resized_image, caption="Hospital Form", use_column_width=False)
        # Sex
        sex = st.selectbox("Sex:", ["Select..."] + list(SEX.values()))
        if sex == "Select...":
            st.error("Please select an option for sex.")

        # General Health
        gen_health = st.selectbox("General Health:", ["Select..."] + list(GEN_HEALTH.values()))
        if gen_health == "Select...":
            st.error("Please select an option for general health.")

        # Physical Health Days
        physical_health = st.number_input("Days of bad physical health in the past month (0-30):", min_value=0, max_value=30, step=1)
        if not is_valid_integer(physical_health, 0, 30):
            st.error("Invalid number. Please enter an integer between 0 and 30.")

        # Mental Health Days
        mental_health = st.number_input("Days of bad mental health in the past month (0-30):", min_value=0, max_value=30, step=1)
        if not is_valid_integer(mental_health, 0, 30):
            st.error("Invalid number. Please enter an integer between 0 and 30.")

        # Physical Activities
        physical_activity = st.selectbox("Do you engage in physical activity?", ["Select...", "Yes", "No"])
        if physical_activity == "Select...":
            st.error("Please select an option for physical activity.")

        # Sleep Hours
        sleep_time = st.number_input("Hours of sleep per night (0-24):", min_value=0, max_value=24, step=1)
        if not is_valid_integer(sleep_time, 0, 24):
            st.error("Invalid number. Please enter an integer between 0 and 24.")

        # Had Stroke
        stroke = st.selectbox("Have you ever had a stroke?", ["Select...", "Yes", "No"])
        if stroke == "Select...":
            st.error("Please select an option for stroke.")

        # Had Kidney Disease
        kidney_disease = st.selectbox("Do you have kidney disease?", ["Select...", "Yes", "No"])
        if kidney_disease == "Select...":
            st.error("Please select an option for kidney disease.")

        # Diabetic
        diabetic = st.selectbox("Are you diabetic?", ["Select..."] + list(DIABETES.values()))
        if diabetic == "Select...":
            st.error("Please select an option for diabetic.")

        # Difficulty Walking
        diff_walking = st.selectbox("Do you have difficulty walking?", ["Select...", "Yes", "No"])
        if diff_walking == "Select...":
            st.error("Please select an option for difficulty walking.")

        # Smoker Status
        smoking = st.selectbox("Do you smoke?", ["Select..."] + list(SMOKER_STATUS.values()))
        if smoking == "Select...":
            st.error("Please select an option for smoking.")

        # Race Ethnicity Category
        race = st.selectbox("Race:", ["Select..."] + list(RACE.values()))
        if race == "Select...":
            st.error("Please select a race.")

        # Age Category
        age_category = st.selectbox("Age Category:", ["Select..."] + list(AGE_CATEGORY.values()))
        if age_category == "Select...":
            st.error("Please select an age category.")

        # BMI
        bmi = st.number_input("BMI (10-50):", min_value=10.0, max_value=50.0, step=0.1)
        if not is_valid_bmi(bmi):
            st.error("Invalid BMI. Please enter a number between 10 and 50.")

        # Alcohol Drinking
        alcohol_drinking = st.selectbox("Do you drink alcohol?", ["Select...", "Yes", "No"])
        if alcohol_drinking == "Select...":
            st.error("Please select an option for alcohol drinking.")

        # Had High Blood Cholesterol
        cholesterol = st.selectbox("Do you have High Cholesterol?", ["Select...", "Yes", "No"])
        if cholesterol == "Select...":
            st.error("Please select an option for skin cancer.")

        if st.button("Submit Form"):
            # Convert categorical data to numerical for the DataFrame
            smoking_num = {v: k for k, v in SMOKER_STATUS.items()}
            sex_num = {v: k for k, v in SEX.items()}
            age_category_num = {v: k for k, v in AGE_CATEGORY.items()}
            race_num = {v: k for k, v in RACE.items()}
            diabetic_num = {v: k for k, v in DIABETES.items()}
            gen_health_num = {v: k for k, v in GEN_HEALTH.items()}
            
            smoking = smoking_num.get(smoking, 0)
            alcohol_drinking = 1 if alcohol_drinking == "Yes" else 0
            stroke = 1 if stroke == "Yes" else 0
            diff_walking = 1 if diff_walking == "Yes" else 0
            sex = sex_num.get(sex, 0)
            age_category = age_category_num.get(age_category, 0)
            race = race_num.get(race, 0)
            diabetic = diabetic_num.get(diabetic, 0)
            physical_activity = 1 if physical_activity == "Yes" else 0
            gen_health = gen_health_num.get(gen_health, 0)
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
    

            conexion = sqlite3.connect('data_recovery.db')
            df = pd.DataFrame(new_data)

            # Save the data in the database
            cursor = conexion.cursor()
            date_registration = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """INSERT INTO patient_data (
                HeartDisease, SmokerStatus, AlcoholDrinkers, HadStroke, DifficultyWalking, Sex,
                AgeCategory, RaceEthnicityCategory, HadDiabetes, PhysicalActivities, GeneralHealth,
                SleepHours, PhysicalHealthDays, MentalHealthDays, BMI, HadKidneyDisease, HadHighBloodCholesterol, dateRegistration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            values = (
                resultInt ,smoking, alcohol_drinking, stroke, diff_walking, sex,
                age_category, race, diabetic, physical_activity, gen_health,
                sleep_time, physical_health, mental_health, bmi, kidney_disease, cholesterol, date_registration
            )
            
            cursor.execute(query, values)
            conexion.commit()
            cursor.close()
            st.success("Form submitted successfully!")

    with tab2:
        st.header("Datos Registrados")
        df = load_data()
        st.dataframe(df)

if __name__ == "__main__":
    main()
