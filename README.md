# Caption_Crafter_AI

A small Flask web app that generates short Instagram captions using Google's Gemini API. You enter a description of your post and choose a mood, and the app returns one clean caption. It also includes a mock fallback mode so it keeps working even when the API key is missing.

## Features

* Simple web form for description and mood
* Uses the Gemini `gemini-2.0-flash` REST endpoint
* Built-in request delay to reduce rate-limit errors
* Mock caption generator for offline use or missing API key
* Clean text parsing so you get only one caption without extra formatting

## How it works

1. You submit a description and mood through the homepage.
2. Flask builds a short prompt and prepares the JSON payload.
3. The app calls:
   `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`
4. It extracts the first usable line of text from the response.
5. If the API key is missing or something goes wrong, the app returns a mock caption.

## Installation

Install the required packages:

```
pip install flask requests python-dotenv
```

## Environment variables

Create a `.env` file (or set these in your system):

```
GEMINI_API_KEY=your_api_key_here
MOCK_FALLBACK=1   # optional; enables mock captions when no key is present
FLASK_ENV=development
```

If you don’t set `GEMINI_API_KEY`, the app will still run. With fallback enabled, it returns mock captions.

## Running the app

Start the server:

```
python app.py
```

Open the app in your browser:

```
http://127.0.0.1:5000/
```

## Project structure

* **app.py** – Flask server and Gemini API logic
* **templates/index.html** – HTML form and output page
* **.env** – optional environment configuration

## Notes

* Don’t commit your API key to GitHub.
* Debug logs can reveal parts of prompts and responses. Keep debug mode off in production.
* You can adjust `REQUEST_DELAY` in the code if you run into rate-limit errors.

## Future improvements

* Better frontend styling
* Separate Gemini client module
* Stronger rate limiting or caching
* Optional authentication before generating captions
