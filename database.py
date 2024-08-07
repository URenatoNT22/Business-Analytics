import mysql.connector

# Establecer la conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="heartDiseaseApp"
)
cursor = conn.cursor()

# Crear tabla de clientes en la base de datos heartDiseaseApp
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    DNI VARCHAR(8),
                    email VARCHAR(255),
                    age INT,
                    sex char(1),
                    date_created DATE
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS results_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    client_id INT,
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
                    dateRegistration DATE,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Tabla de clientes creada en la base de datos heartDiseaseApp exitosamente.")