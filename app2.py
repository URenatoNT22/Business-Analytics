import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ml import preprocess_and_predict, entrenar
import joblib
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Configuration
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Chatbot Configuration
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Constants
SEX = {1: 'Male', 2: 'Female'}
GEN_HEALTH = {1: "Excellent", 2: "Very good", 3: "Good", 4: "Fair", 5: "Poor"}
PHYS_MEN_HEALTH = {77: np.nan, 88: 0, 99: np.nan}
YES_NO_QUESTIONS = {1: 'Yes', 2: 'No'}
SLEEP_TIME = lambda x: np.where(x > 24, np.nan, x)
DIABETES = {1: "Yes", 2: "Yes, but only during pregnancy (female)", 3: "No", 4: "No, pre-diabetes or borderline diabetes"}
SMOKER_STATUS = {1: "Current smoker - now smokes every day", 2: "Current smoker - now smokes some days", 3: "Former smoker", 4: "Never smoked"}
RACE = {1: "White only, Non-Hispanic", 2: "Black only, Non-Hispanic", 3: "Other race only, Non-Hispanic", 4: "Multiracial, Non-Hispanic", 5: "Hispanic"}
AGE_CATEGORY = {1: "Age 18 to 24", 2: "Age 25 to 29", 3: "Age 30 to 34", 4: "Age 35 to 39", 5: "Age 40 to 44", 6: "Age 45 to 49", 7: "Age 50 to 54", 8: "Age 55 to 59", 9: "Age 60 to 64", 10: "Age 65 to 69", 11: "Age 70 to 74", 12: "Age 75 to 79", 13: "Age 80 or older"}

def is_valid_bmi(bmi):
    return 10 <= bmi <= 50

def is_valid_integer(value, min_value, max_value):
    return min_value <= value <= max_value

def main():
    st.title("Heart Disease Prediction Form")

    image = Image.open("./LogoForm.png")
    resized_image = image.resize((300, 200))
    st.image(resized_image, caption="Hospital Form", use_column_width=False)

    # Form Inputs
    sex = st.selectbox("Sex:", ["Select..."] + list(SEX.values()))
    if sex == "Select...":
        st.error("Please select an option for sex.")
    
    gen_health = st.selectbox("General Health:", ["Select..."] + list(GEN_HEALTH.values()))
    if gen_health == "Select...":
        st.error("Please select an option for general health.")
    
    physical_health = st.number_input("Days of bad physical health in the past month (0-30):", min_value=0, max_value=30, step=1)
    if not is_valid_integer(physical_health, 0, 30):
        st.error("Invalid number. Please enter an integer between 0 and 30.")
    
    mental_health = st.number_input("Days of bad mental health in the past month (0-30):", min_value=0, max_value=30, step=1)
    if not is_valid_integer(mental_health, 0, 30):
        st.error("Invalid number. Please enter an integer between 0 and 30.")
    
    physical_activity = st.selectbox("Do you engage in physical activity?", ["Select...", "Yes", "No"])
    if physical_activity == "Select...":
        st.error("Please select an option for physical activity.")
    
    sleep_time = st.number_input("Hours of sleep per night (0-24):", min_value=0, max_value=24, step=1)
    if not is_valid_integer(sleep_time, 0, 24):
        st.error("Invalid number. Please enter an integer between 0 and 24.")
    
    stroke = st.selectbox("Have you ever had a stroke?", ["Select...", "Yes", "No"])
    if stroke == "Select...":
        st.error("Please select an option for stroke.")
    
    kidney_disease = st.selectbox("Do you have kidney disease?", ["Select...", "Yes", "No"])
    if kidney_disease == "Select...":
        st.error("Please select an option for kidney disease.")
    
    diabetic = st.selectbox("Are you diabetic?", ["Select..."] + list(DIABETES.values()))
    if diabetic == "Select...":
        st.error("Please select an option for diabetic.")
    
    diff_walking = st.selectbox("Do you have difficulty walking?", ["Select...", "Yes", "No"])
    if diff_walking == "Select...":
        st.error("Please select an option for difficulty walking.")
    
    smoking = st.selectbox("Do you smoke?", ["Select..."] + list(SMOKER_STATUS.values()))
    if smoking == "Select...":
        st.error("Please select an option for smoking.")
    
    race = st.selectbox("Race:", ["Select..."] + list(RACE.values()))
    if race == "Select...":
        st.error("Please select a race.")
    
    age_category = st.selectbox("Age Category:", ["Select..."] + list(AGE_CATEGORY.values()))
    if age_category == "Select...":
        st.error("Please select an age category.")
    
    bmi = st.number_input("BMI (10-50):", min_value=10.0, max_value=50.0, step=0.1)
    if not is_valid_bmi(bmi):
        st.error("Invalid BMI. Please enter a number between 10 and 50.")
    
    alcohol_drinking = st.selectbox("Do you drink alcohol?", ["Select...", "Yes", "No"])
    if alcohol_drinking == "Select...":
        st.error("Please select an option for alcohol drinking.")
    
    skin_cancer = st.selectbox("Do you have High Cholesterol?", ["Select...", "Yes", "No"])
    if skin_cancer == "Select...":
        st.error("Please select an option for skin cancer.")

    if st.button("Submit Form"):
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
        skin_cancer = 1 if skin_cancer == "Yes" else 0

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
        })

        result, impacto_df = preprocess_and_predict(new_data)
        st.write(result)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(impacto_df['Feature'], impacto_df['Impact'], color='#4C72B0')
        ax.set_xlabel('Importance')
        ax.set_title('Feature Impact')
        ax.invert_yaxis()
        st.pyplot(fig)

        # Create and send message to chatbot
        chatbot_message = (
            f"Toma el rol de un médico especializado, tienes un paciente "
            f"que te entrega la siguiente información\n"
            f"Sex: {SEX.get(sex, 'Unknown')}\n"
            f"General Health: {GEN_HEALTH.get(gen_health, 'Unknown')}\n"
            f"Days of bad physical health in the past month (0-30): {physical_health}\n"
            f"Days of bad mental health in the past month (0-30): {mental_health}\n"
            f"Do you engage in physical activity?: {'Yes' if physical_activity == 1 else 'No'}\n"
            f"Hours of sleep per night (0-24):: {sleep_time}\n"
            f"Have you ever had a stroke?: {'Yes' if stroke == 1 else 'No'}\n"
            f"Do you have kidney disease?: {'Yes' if kidney_disease == 1 else 'No'}\n"
            f"Are you diabetic?: {DIABETES.get(diabetic, 'Unknown')}\n"
            f"Do you have difficulty walking?: {'Yes' if diff_walking == 1 else 'No'}\n"
            f"Do you smoke?: {SMOKER_STATUS.get(smoking, 'Unknown')}\n"
            f"Race: {RACE.get(race, 'Unknown')}\n"
            f"Age Category: {AGE_CATEGORY.get(age_category, 'Unknown')}\n"
            f"BMI: {bmi}\n"
            f"Do you drink alcohol?: {'Yes' if alcohol_drinking == 1 else 'No'}\n"
            f"Do you have High Cholesterol?: {'Yes' if skin_cancer == 1 else 'No'}\n"
            f"Con está información dame indicadores de riesgo y también recomendaciones "
            f"que ayudarian a mejorar la salud del paciente (responde todo en español)"
        )
        
        # Send the chatbot message without showing it in the chat history
        chat_session = st.session_state.chat_session
        chat_session.send_message(chatbot_message)

        # Display chatbot's response
        st.session_state.chat_history = []
        for message in chat_session.history:
            if message.role == "model":
                st.session_state.chat_history.append(message)

        st.title("🤖 Gemini Pro - ChatBot")
        for message in st.session_state.chat_history:
            if message.role == "user":
                with st.chat_message("user"):
                    st.markdown(message.parts[0].text)
            elif message.role == "model":
                with st.chat_message("assistant"):
                    st.markdown(message.parts[0].text)

        user_prompt = st.chat_input("Ask Gemini-Pro...")
        if user_prompt:
            st.chat_message("user").markdown(user_prompt)
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)

if __name__ == "__main__":
    main()
