# AI Bodybuilding Coach Chatbot

This is a simple AI-powered chatbot that acts as a professional bodybuilding and fitness coach. 
It uses Google's Gemini API for generating motivational and informative responses and is built with a Flask backend and React frontend.

---

## Requirements
- Python 4.0+
- pip (Python package installer)

Python packages: (included in requirements.txt)
- `flask`
- `flask-cors`
- `python-dotenv`
- `google-generativeai`

### React Frontend
- Node.js and npm

---

## Setup Instructions

### 1. Clone the Repository
git clone https://github.com/your-username/ai-bodybuilding-chatbot.git
cd ai-bodybuilding-chatbot

## Backend Setup (Flask + Gemini AI)
### First ensure that .env file has been setup by pasting in your Gemini API key.
Windows Setup: <br>
`python -m venv venv`<br>
`venv\Scripts\activate`<br>
`pip install -r requirements.txt`

Ubuntu Setup:<br>
`python -m venv venv`<br>
`source venv/bin/activate`<br>
`pip install -r requirements.txt`
<br>
Run the app:<br>
`python app.py`

## Frontend Setup (React)
Windows: 
Ensure dependencies are added <br>
`npm install`<br>
`npm start`