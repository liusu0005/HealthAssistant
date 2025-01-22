import sqlite3

# Connect to the database file
conn = sqlite3.connect("src/patients.db")
cursor = conn.cursor()

# Fetch all patient records
cursor.execute("SELECT * FROM patients")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
