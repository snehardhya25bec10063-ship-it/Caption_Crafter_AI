📸 Caption Crafter AI

A simple web application that creates Instagram-style captions using Google’s Gemini API. You describe your post, pick a mood, and the app generates a short caption for you.

👉 Live Demo:
https://caption-crafter-ai-1.onrender.com/

📱 Demo Preview

Here’s how the app looks when generating a caption:

(If you want, I can crop or enhance this screenshot and upload a cleaner version.)

⭐ What this app does

Caption Crafter AI takes a short description of your post and the mood you want. It sends this to the Gemini API and returns a clean, ready-to-use caption. The interface is a single responsive HTML page with a smooth gradient design and subtle animations.

🔧 Tech stack

Python 3.11

Flask

Google Gemini API (REST)

HTML + CSS

Gunicorn for production

🚀 Features

Clean and modern UI

One-click caption generation

Multiple moods like funny, romantic, casual, inspirational and more

Handles API rate limits safely

Works locally and on cloud platforms

Deployment-ready for Render, Railway, ngrok, and Heroku

🛠 How it works

You type what your post is about.

You choose a mood.

The server sends a simple prompt to Gemini.

Gemini returns a caption.

The backend extracts one short line and shows it.

Everything runs through app.py.

📁 Project structure
/
│ app.py
│ requirements.txt
│ runtime.txt
│ Procfile
│ README.md
│ DEPLOYMENT.md
│ .gitignore
│
└── templates/
    └── index.html

▶️ Run the app locally

Install dependencies

pip install -r requirements.txt


Create a .env file

GEMINI_API_KEY=your_key_here


Start the server

python app.py


Visit:

http://localhost:5000

🌍 Deployment

A full guide for deploying the app is included in DEPLOYMENT.md.

🔒 Environment variables

Set these before deploying:

GEMINI_API_KEY=your_api_key_here
FLASK_ENV=production
