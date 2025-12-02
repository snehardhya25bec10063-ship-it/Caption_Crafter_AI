# 📘 Project Statement: Caption Crafter AI

## Summary

A small Flask web app that generates short Instagram captions using the Gemini (Generative Language) REST API. The app accepts a post description and a mood, then requests a single catchy caption from the model. If the Gemini API key is missing or calls fail, the app falls back to a lightweight local mock generator so the user still gets a usable caption.

## Key features

* Minimal Flask app with a single `index` route that displays and returns captions.
* Uses Google’s Generative Language `gemini-2.0-flash` model via the REST `generateContent` endpoint.
* Simple rate-throttling to avoid hitting API limits (configurable delay).
* Config-driven mock fallback for offline development or when the API key is absent.
* Defensive parsing of API responses and robust error handling to avoid crashing the UI.

## Files of interest

* `app.py` (or whatever you named the file): main Flask application and API client logic.
* `templates/index.html`: Jinja template that presents the form and shows the generated caption.
* `.env` (optional): contains `GEMINI_API_KEY` and optional `MOCK_FALLBACK` flag.

## How it works (high level)

1. User submits a short description and selects a mood on the web form.
2. The server builds a short prompt and calls the Gemini REST endpoint with a generation configuration.
3. The app enforces a small delay between requests (`REQUEST_DELAY`) to reduce the chance of rate-limit errors.
4. On success the app extracts the first sensible text part from the response and returns it to the template.
5. If anything goes wrong — no key, network error, unexpected response, or non-200 status — the code uses a deterministic `generate_mock_caption` so the user still sees a caption.

## Configuration and environment

* `GEMINI_API_KEY` (recommended): the Google API key used for the `generateContent` call. Set this in your environment or in a `.env` file.
* `MOCK_FALLBACK` (optional): `1`, `true`, or `yes` will enable the local fallback when the API key is missing. Default is off.
* `REQUEST_DELAY` (constant in the file): number of seconds the app waits between requests to avoid hitting rate limits. Adjust as needed.

## Running locally

1. Create a virtual environment and install required packages, e.g. `pip install flask requests python-dotenv`.
2. Add environment variables:

   * `GEMINI_API_KEY` (optional if you want actual Gemini output)
   * `MOCK_FALLBACK=1` if you want the app to produce mock captions offline.
3. Run the app: `python app.py`. By default it uses `FLASK_ENV=development` to enable debug mode.
4. Open `http://127.0.0.1:5000/` and try the form.

## Important implementation details

* **REST usage**: The app calls `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=<API_KEY>` with a simple JSON payload. The payload includes `contents` and a `generationConfig` (temperature, token limit).
* **Response parsing**: The app looks for `candidates -> content -> parts -> text`. It picks the first reasonable non-heading non-empty line and strips excess characters.
* **Rate-limit detection**: A helper `_is_rate_or_quota_error` looks for common keywords in exception messages to detect quota/rate issues. The code also enforces a minimum request spacing (`REQUEST_DELAY`).
* **Fallback strategy**: If the API is unavailable, the code logs debug/error messages and generates a human-friendly mock caption instead of failing.

## Error handling & troubleshooting

* If the app prints `Error: GEMINI_API_KEY not set...` you either need to add the key or enable `MOCK_FALLBACK` for offline testing.
* If the API returns non-200 statuses, the app logs the response body and returns the mock caption.
* If you receive 429s or `resource_exhausted`, consider increasing `REQUEST_DELAY`, batching requests more sparsely, or upgrading quota with the provider.
* Use the debug log lines that were included in the code (`[DEBUG]` / `[ERROR]`) to inspect payloads, HTTP status codes, and partial responses.

## Security and privacy notes

* Never commit `GEMINI_API_KEY` or any credentials to public version control. Keep them in environment variables or a private secrets store.
* The code prints debug output which can include portions of the prompt and returned content — avoid enabling debug logs in a production environment where sensitive content may be processed.
* Limit token size and user-supplied prompt length if you expect large or untrusted inputs.
