# Project Statement: Caption Crafter AI

## Overview

Caption Crafter AI is a simple and clean web application built with Flask. It creates short Instagram-style captions using Google’s Gemini API. You type a short description, choose a mood, and the app returns one caption. The goal is to keep the tool lightweight, fast, and easy to use.

This project also includes a fallback mode. If the API key is missing or the AI service fails, the app can still generate a basic mock caption so it never breaks.

## What the Application Does

* Accepts a short description and mood from the user
* Sends the request to Gemini’s `gemini-2.0-flash` model
* Returns a single clean caption without extra formatting
* Falls back to a local mock caption when needed
* Avoids rate‑limit issues with a small built‑in delay between requests

## How It Works Internally

1. The user fills the form on the home page.
2. The server builds a simple, direct prompt for the model.
3. A request is sent to the Gemini REST endpoint.
4. The response is parsed and the first meaningful caption line is selected.
5. If the call fails, the fallback generator creates a basic caption instead.

## Technologies Used

* **Flask** for the backend
* **HTML + Jinja** for templates
* **Requests library** for API calls
* **python-dotenv** for managing environment variables
* **Render** for deployment
* **Gemini API** as the caption engine

## Deployment Notes

This application is hosted on Render’s free tier. Free instances shut down after 15 minutes of inactivity. When they restart, the first request can take around **40–60 seconds** to load. After that, everything works normally.

## Project Structure

* `app.py` – main application logic
* `templates/index.html` – user interface
* `requirements.txt` – dependencies
* `Procfile` (optional for deployment)
* `.env` (not included in the repo) – stores the API key

## Key Strengths of the Project

* Complete end‑to‑end development: backend, AI integration, and deployment
* Clean, readable code
* Good handling of errors and missing API keys
* Simple and user‑friendly interface
* Great starter AI project for building your GitHub portfolio

## Purpose of This Statement

This document summarizes how the project works, the technologies used, and how the app behaves in real-world usage. It provides a high‑level, human‑readable explanation of the application for documentation or academic submission.
