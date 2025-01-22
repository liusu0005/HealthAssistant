import json
from flask import Response, jsonify, render_template, request, stream_with_context

from .app import app, db
#from .chat_api import call_chat
from .chat_langchain import call_chat
from .db_utils import get_user_data

demo_name = "Your HeartCare Assistant"

greeting_message = "Hello, I’m Sopia, you HeartCare Assistant! I’m here to support you with personalized guidance and answers to your heart health questions. Whether you’re managing a condition or just seeking information, I’m here to help every step of the way. How can I assist you today?"

@app.route("/")
def index():
    return render_template("index.html", demo_name=demo_name)

@app.route("/chat", methods=["POST"])
def chat_handler():
    request_message = request.json["message"]

    @stream_with_context
    def response_stream():
        for chunk in call_chat(request_message):
            # returning a json format for easier encoding
            # each chunk {"token": "..."}
            yield json.dumps(chunk, ensure_ascii=False) + "\n"

    return Response(response_stream(), mimetype="text/event-stream")


@app.route("/user/<user_id>", methods=["GET"])
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

        
