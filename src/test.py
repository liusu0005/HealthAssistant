from .app import app, db

def get_user(user_id):
    # Query the database for the user's data
    user = db.session.execute(
            """
            SELECT id, name, age, gender, blood_pressure_high, blood_pressure_low, BMI, weight,
                   height, temperature, pulse, oxygen_saturation, diagnosis, history,
                   drink_wine, smoke, drug
            FROM patients
            WHERE id = :id
            """,
            {"id": user_id}
        ).fetchone()

    # Check if the user was found
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Convert the query result to a dictionary
    user_data = dict(user)

    # Return the user data as JSON
    return jsonify(user_data)


get_user(1)
