from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv

# user model, save and load user data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# load environment variables from .env file (Check README.md)
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)

# endpoint to receive user query, generate response
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    prompt = f"You are a professional bodybuilding and fitness coach. Give helpful, motivational responses.\nUser: {user_input}"

    # Use Gemini to generate response
    try:
        client = genai.Client(api_key="AIzaSyCJykhYhpUiXm-LALLQaA7FYuI1eYCugUA")
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_input # Using the lighweight & free model
        )   
        print("Gemini response:", response.text)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
