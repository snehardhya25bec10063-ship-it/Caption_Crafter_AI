from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests
import json
import time

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Rate limit throttling - store last request time
last_request_time = 0
REQUEST_DELAY = 1.5  # seconds between requests to avoid rate limiting

# Enable a mock fallback when no API key is present
MOCK_FALLBACK = os.getenv("MOCK_FALLBACK", "0").lower() in ("1", "true", "yes")

# Use REST API directly instead of SDK
# Use gemini-2.0-flash which is more reliable for text generation
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash"

app = Flask(__name__)

def generate_mock_caption(description: str, mood: str) -> str:
    """Return a simple mock caption for offline/testing when no API key is present."""
    desc = description.strip() or "your post"
    mood_clean = (mood or "Casual").strip().capitalize()
    return f"{mood_clean} vibe: {desc}. #mockcaption"


def _is_rate_or_quota_error(exc: Exception) -> bool:
    """Return True if exception appears to be a rate/quota/limit error."""
    txt = str(exc).lower()
    return any(keyword in txt for keyword in (
        "rate limit", "rate_limit", "429", "quota", 
        "too many requests", "requests per minute", "resource_exhausted"
    ))

@app.route("/", methods=["GET", "POST"])
def index():
    caption = ""
    if request.method == "POST":
        description = request.form.get("description")
        mood = request.form.get("mood")
        prompt = f"Create a short, catchy and {mood.lower()} Instagram caption for this post: '{description}'"
        
        if not gemini_api_key:
            if MOCK_FALLBACK:
                caption = generate_mock_caption(description or "", mood or "Casual")
            else:
                caption = "Error: GEMINI_API_KEY not set. Please add it to your environment or .env file."
        else:
            try:
                # Use REST API directly
                simple_prompt = f"Generate ONE short Instagram caption for: '{description}'. Mood: {mood}. Return ONLY the caption text, nothing else. No intro, no bullet points, just one caption."
                
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": simple_prompt
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 150,
                    }
                }
                
                url = f"{GEMINI_API_ENDPOINT}:generateContent?key={gemini_api_key}"
                print(f"\n[DEBUG] Making REST call to Gemini API")
                print(f"[DEBUG] Prompt: {simple_prompt}")
                
                # Throttle requests to avoid rate limiting
                global last_request_time
                time_since_last = time.time() - last_request_time
                if time_since_last < REQUEST_DELAY:
                    wait_time = REQUEST_DELAY - time_since_last
                    print(f"[DEBUG] Rate throttling: waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                last_request_time = time.time()
                
                response = requests.post(url, json=payload, timeout=30)
                print(f"[DEBUG] HTTP Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"[DEBUG] Response data keys: {data.keys()}")
                    print(f"[DEBUG] Full response: {json.dumps(data, indent=2)[:500]}")
                    
                    # Extract text from response
                    if "candidates" in data and data["candidates"]:
                        for candidate in data["candidates"]:
                            if caption:  # Already found caption
                                break
                            print(f"[DEBUG] Candidate keys: {candidate.keys()}")
                            if "content" in candidate and "parts" in candidate["content"]:
                                for part in candidate["content"]["parts"]:
                                    print(f"[DEBUG] Part: {part}")
                                    if "text" in part:
                                        text = part["text"].strip()
                                        if text:
                                            # Extract only the first caption/line, not all options
                                            lines = [line.strip() for line in text.split('\n') if line.strip()]
                                            if lines:
                                                # Take first non-empty, non-heading line
                                                for line in lines:
                                                    if line and not line.startswith('**') and not line.startswith('#'):
                                                        caption = line.replace('*   "', '').replace('"', '').strip()
                                                        if len(caption) > 5:  # Make sure it's a real caption
                                                            print(f"[DEBUG] Got caption: {caption[:100]}")
                                                            break
                                            if caption:
                                                break
                    
                    if caption == "":
                        print("[DEBUG] No text in response, using mock")
                        caption = generate_mock_caption(description or "", mood or "Casual")
                else:
                    error_msg = response.text
                    print(f"[ERROR] API returned {response.status_code}: {error_msg}")
                    caption = generate_mock_caption(description or "", mood or "Casual")
                    
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Request failed: {e}")
                caption = generate_mock_caption(description or "", mood or "Casual")
            except Exception as e:
                print(f"[ERROR] Exception: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                caption = generate_mock_caption(description or "", mood or "Casual")
    
    return render_template("index.html", caption=caption)

if __name__ == "__main__":
    # Use debug=True for development, debug=False for production
    debug_mode = os.getenv("FLASK_ENV", "development") == "development"
    app.run(debug=debug_mode)

