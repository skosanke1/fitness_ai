# AI Bodybuilding Coach Chatbot

This is a simple AI-powered chatbot that acts as a professional bodybuilding and fitness coach. 
It uses Google's Gemini API for generating motivational and informative responses and is built with a Flask backend and React frontend.

---

## Requirements
- Python 4.0+
- pip (Python package installer)

### React Frontend
- Node.js and npm `sudo apt install nodejs npm`

---

## Setup Instructions

### 1. Clone the Repository
`git clone https://github.com/skosanke1/fitness_ai`
`cd fitness_ai`

## 2. Backend Setup (Flask + Gemini AI)
`cd server`<br>
### First ensure that .env file has been setup by pasting in your Gemini API key.
Windows Setup: <br>
`python -m venv venv`<br>
`venv\Scripts\activate`<br>
`pip install -r requirements.txt`
`flask run`

Ubuntu Setup:<br>
`python -m venv venv`<br>
`source venv/bin/activate`<br>
`pip install -r requirements.txt`
<br>
Run the app:<br>
`python app.py`

## 3. Frontend Setup (React)
`cd server`<br>
Windows: 
Ensure dependencies are added <br>
`npm install`<br>
`npm start`