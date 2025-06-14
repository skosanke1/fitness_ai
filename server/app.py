from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv
from flask_migrate import Migrate


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# load environment variables from .env file (Check README.md)
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# load API keys
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # change this in production
apikey = os.getenv("GEMINI_API_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#db setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login setup
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# user model, save and load user data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# preferences model, contains user's training preferences.
class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    weight = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    has_weights = db.Column(db.Boolean, default=False)
    has_cardio = db.Column(db.Boolean, default=False)
    has_home = db.Column(db.Boolean, default=False)
    user = db.relationship("User", backref="preferences", uselist=False)

# login function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# chat function
@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # get preferences from the preferences model
    pref = Preferences.query.filter_by(user_id=current_user.id).first()

    # load preferences
    if pref:
        preferences = "Details about client: "
        if pref.gender:
            preferences += f"Gender: {pref.gender}. "
        if pref.weight:
            preferences += f"Weight: {pref.weight} lbs. "
        if pref.has_weights:
            preferences += "Has access to weights. "
        if pref.has_cardio:
            preferences += "Has access to cardio machines. "
        if pref.has_home:
            preferences += "Has home workout equipment. "
    else:
        preferences = "Client has not set preferences. "

    # load prompt
    prompt = f"You are a professional bodybuilding and fitness coach. Use the client's profile below to fully tailor your response to their unique needs, body type, and available equipment. The response must reflect the client's gender, weight, and available equipment if provided..\n{preferences}\nClient's prompt: {user_input}"
    print("Gemini promot:", prompt)
    # send query
    try:
        client = genai.Client(api_key=apikey)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_input
        )

        # received query
        print("Gemini response:", response.text)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# register user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # duplicate email in db
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

# login user
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=True)  # enable long-term login
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"error": "Invalid email or password"}), 401

# logout user
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

# get session
@app.route("/session", methods=["GET"])
def session_check():
    return jsonify({"loggedIn": current_user.is_authenticated})

# get preferences
@app.route("/preferences", methods=["GET"])
@login_required
def get_preferences():
    pref = Preferences.query.filter_by(user_id=current_user.id).first()
    if pref:
        return jsonify({"preferences": {
            "weight": pref.weight,
            "gender": pref.gender,
            "equipment": {
                "weights": pref.has_weights,
                "cardio": pref.has_cardio,
                "home": pref.has_home
            }
        }})
    return jsonify({"preferences": {}})

# post preferences
@app.route("/preferences", methods=["POST"])
@login_required
def set_preferences():
    data = request.get_json()
    pref = Preferences.query.filter_by(user_id=current_user.id).first()
    if not pref:
        pref = Preferences(user_id=current_user.id)
        db.session.add(pref)
    
    pref.weight = data.get("weight")
    pref.gender = data.get("gender")
    pref.has_weights = data.get("equipment", {}).get("weights", False)
    pref.has_cardio = data.get("equipment", {}).get("cardio", False)
    pref.has_home = data.get("equipment", {}).get("home", False)
    db.session.commit()
    return jsonify({"message": "Preferences saved"})