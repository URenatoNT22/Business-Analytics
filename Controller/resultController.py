from services import database as db
from Controller.models.Result import Result
import streamlit as st

def create_result_data(new_data, resultInt, date_registration, client_id):
    db.cursor.execute('INSERT INTO results_data (HeartDisease, Sex, GeneralHealth, PhysicalHealthDays, MentalHealthDays, PhysicalActivities, SleepHours, HadStroke, HadKidneyDisease, HadDiabetes, DifficultyWalking, SmokerStatus, RaceEthnicityCategory, AgeCategory, BMI, AlcoholDrinkers, HadHighBloodCholesterol, dateRegistration, client_id) '
                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                      (int(resultInt), 
                       int(new_data['Sex'].values[0]), 
                       int(new_data['GeneralHealth'].values[0]), 
                       int(new_data['PhysicalHealthDays'].values[0]), 
                       int(new_data['MentalHealthDays'].values[0]), 
                       int(new_data['PhysicalActivities'].values[0]), 
                       int(new_data['SleepHours'].values[0]), 
                       int(new_data['HadStroke'].values[0]), 
                       int(new_data['HadKidneyDisease'].values[0]), 
                       int(new_data['HadDiabetes'].values[0]), 
                       int(new_data['DifficultyWalking'].values[0]), 
                       int(new_data['SmokerStatus'].values[0]), 
                       int(new_data['RaceEthnicityCategory'].values[0]), 
                       int(new_data['AgeCategory'].values[0]), 
                       float(new_data['BMI'].values[0]), 
                       int(new_data['AlcoholDrinkers'].values[0]), 
                       int(new_data['HadHighBloodCholesterol'].values[0]), 
                       date_registration, 
                       int(client_id)))
    db.bdConnection.commit()

def read_results_data():
    db.cursor.execute('SELECT * FROM results_data')
    resultsDataList = []
    
    for row in db.cursor.fetchall():
        try:
            result = Result(
                id=int(row[0]),  # id
                client_id=int(row[1]),  # client_id
                HeartDisease=int(row[2]),  # HeartDisease
                Sex=int(row[3]),  # Sex
                GeneralHealth=int(row[4]),  # GeneralHealth
                PhysicalHealthDays=int(row[5]),  # PhysicalHealthDays
                MentalHealthDays=int(row[6]),  # MentalHealthDays
                PhysicalActivities=int(row[7]),  # PhysicalActivities
                SleepHours=int(row[8]),  # SleepHours
                HadStroke=int(row[9]),  # HadStroke
                HadKidneyDisease=int(row[10]),  # HadKidneyDisease
                HadDiabetes=int(row[11]),  # HadDiabetes
                DifficultyWalking=int(row[12]),  # DifficultyWalking
                SmokerStatus=int(row[13]),  # SmokerStatus
                RaceEthnicityCategory=int(row[14]),  # RaceEthnicityCategory
                AgeCategory=int(row[15]),  # AgeCategory
                BMI=float(row[16]),  # BMI
                AlcoholDrinkers=int(row[17]),  # AlcoholDrinkers
                HadHighBloodCholesterol=int(row[18]),  # HadHighBloodCholesterol
                dateRegistration=row[19]  # dateRegistration (suponiendo que es datetime.date o similar)
            )
            resultsDataList.append(result)
        except ValueError as e:
            st.write(f"Error al procesar fila: {e}")
    
    return resultsDataList
