from ml import (
    preprocess_and_predict,
    entrenar
)
import streamlit as st
import pandas as pd
import joblib


# scaler = joblib.load('scaler.joblib')
# xgb = joblib.load('xgb_model.joblib')

def is_valid_bmi(bmi):
    return 10 <= bmi <= 50

def is_valid_integer(value, min_value, max_value):
    return min_value <= value <= max_value

def main():
   
    st.title("Hospital Form")
    # entrenar()
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

    # Sex
    sex = st.selectbox("Sex:", ["Select...", "Male", "Female"])
    if sex == "Select...":
        st.error("Please select an option for sex.")

    # Age Category
    age_category = st.selectbox("Age Category:", ["Select...", "18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
    if age_category == "Select...":
        st.error("Please select an age category.")

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

    # General Health
    gen_health = st.selectbox("General Health:", ["Select...", "Excellent", "Very Good", "Good", "Fair", "Poor"])
    if gen_health == "Select...":
        st.error("Please select an option for general health.")

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
    skin_cancer = st.selectbox("Do you have High Cholesterol?", ["Select...", "Yes", "No"])
    if skin_cancer == "Select...":
        st.error("Please select an option for skin cancer.")

    if st.button("Enviar Form"):
        # Convert categorical data to numerical for the DataFrame
        smoking = 1 if smoking == "Yes" else 0
        alcohol_drinking = 1 if alcohol_drinking == "Yes" else 0
        stroke = 1 if stroke == "Yes" else 0
        diff_walking = 1 if diff_walking == "Yes" else 0
        sex = 1 if sex == "Male" else 2
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
        skin_cancer = 1 if skin_cancer == "Yes" else 0

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
            
            'HadHighBloodCholesterol': [skin_cancer]
            # 'SkinCancer': [skin_cancer]
        })

        # Realizar la predicción
        result = preprocess_and_predict(new_data)
        st.write(result)
    

if __name__ == "__main__":
    main()
