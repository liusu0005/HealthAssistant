import sqlite3

# Connect to the database file
conn = sqlite3.connect("src/patients.db")
cursor = conn.cursor()

# Step 1: Create a table for patient information if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    blood_pressure_high INTEGER,
    blood_pressure_low INTEGER,
    BMI REAL,
    weight REAL,
    height REAL,
    temperature REAL,
    pulse INTEGER,
    oxygen_saturation INTEGER,
    diagnosis TEXT,
    history TEXT,
    drink_wine TEXT,
    smoke TEXT,
    drug TEXT
)
""")
print("Table created or already exists.")

# Step 2: Insert patient data into the table
patients_data = [
    ("John Doe", 45, "Male", 140, 90, 25.4, 80, 175, 98.6, 72, 98, "Hypertension", "Family history of hypertension", "Yes", "No", "No"),
    ("Jane Smith", 32, "Female", 120, 80, 22.3, 65, 165, 98.7, 75, 99, "Diabetes", "No significant history", "No", "No", "No"),
    ("Michael Brown", 60, "Male", 150, 95, 27.8, 85, 180, 99.0, 70, 97, "Heart Disease", "Smoker for 20 years", "Yes", "Yes", "No"),
    ("Emily White", 28, "Female", 110, 70, 20.5, 55, 160, 98.5, 78, 99, "Anxiety", "No significant history", "Occasionally", "No", "No"),
    ("Robert Johnson", 50, "Male", 135, 85, 30.1, 95, 170, 99.2, 68, 96, "Obesity", "Family history of obesity", "No", "No", "No"),
    ("Sarah Davis", 40, "Female", 125, 80, 23.7, 60, 167, 98.6, 76, 98, "Asthma", "Asthma since childhood", "No", "No", "Yes"),
    ("Chris Wilson", 35, "Male", 130, 85, 24.5, 78, 175, 98.4, 80, 99, "Healthy", "No significant history", "Occasionally", "No", "No"),
    ("Olivia Martinez", 55, "Female", 145, 90, 26.2, 70, 162, 98.8, 74, 97, "Arthritis", "Family history of arthritis", "Yes", "No", "No")
]

cursor.executemany("""
INSERT INTO patients (
    name, age, gender, blood_pressure_high, blood_pressure_low, BMI, weight, height, 
    temperature, pulse, oxygen_saturation, diagnosis, history, drink_wine, smoke, drug
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", patients_data)

# Commit the changes and close the connection
conn.commit()
print("Patient data inserted successfully!")

conn.close()