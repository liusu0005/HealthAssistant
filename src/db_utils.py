from .app import db

def get_user_data(user_id):
    # Retrieve all columns from the patients table for the given user_id
    user = db.session.execute(
        """
        SELECT name, age, gender, blood_pressure_high, blood_pressure_low, BMI, weight, height,
               temperature, pulse, oxygen_saturation, diagnosis, history, drink_wine, smoke, drug
        FROM patients
        WHERE id = :id
        """,
        {"id": user_id}
    ).fetchone()

    if user:
        # Convert the query result to a dictionary
        return dict(user)
    return None