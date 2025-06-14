# AI Bodybuilding Coach Chatbot

This is a simple AI-powered chatbot that acts as a professional bodybuilding and fitness coach. 
It uses Google's Gemini API for generating motivational and informative responses and is built with a Flask backend and React frontend.

---

## Requirements
- Windows (Host) or Ubuntu VM (Tested on Ubuntu 24.04)
- Python 4.0+
- pip (Python package installer)
- Node.js and npm https://nodejs.org/en/download or ` sudo apt install nodejs`
- Google Gemini API key (receive one from https://developers.google.com/profile)
- Create a .env file to hold the API keys

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
`py init_db.py`<br>

Ubuntu Setup:<br>
`python -m venv venv`<br>
`source venv/bin/activate`<br>
`pip install -r requirements.txt`
`python init_db.py`<br>
<br>
`flask run`

## 3. Frontend Setup (React)
`cd client`<br>
 
Ensure IPv6 is disabled (for Ubuntu) <br>
`sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1`

Windows & Ububtu: <br>
`npm install`<br>
`npm start`