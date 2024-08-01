import sqlite3

def create_database():
    # Conectar a la base de datos (se creará si no existe)
    conn = sqlite3.connect('data_recovery.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            HeartDisease INTEGER,
            Sex INTEGER,
            GeneralHealth INTEGER,
            PhysicalHealthDays INTEGER,
            MentalHealthDays INTEGER,
            PhysicalActivities INTEGER,
            SleepHours INTEGER,
            HadStroke INTEGER,
            HadKidneyDisease INTEGER,
            HadDiabetes INTEGER,
            DifficultyWalking INTEGER,
            SmokerStatus INTEGER,
            RaceEthnicityCategory INTEGER,
            AgeCategory INTEGER,
            BMI REAL,
            AlcoholDrinkers INTEGER,
            HadHighBloodCholesterol INTEGER,
            dateRegistration DATE
        )
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and table created successfully.")
