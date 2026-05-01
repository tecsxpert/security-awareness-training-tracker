from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()
import os


from services.groq_client import call_groq

from services.analysis_service import analyze_security_issue

from datetime import datetime
import json

from services.embedding_service import load_model

load_model()  

from services.embedding_service import get_embedding


import time
import werkzeug.serving

werkzeug.serving.WSGIRequestHandler.server_version = "SecureServer"
werkzeug.serving.WSGIRequestHandler.sys_version = ""
from werkzeug.serving import WSGIRequestHandler

class CustomHandler(WSGIRequestHandler):
    def version_string(self):
        return ""

START_TIME = time.time()
TOTAL_REQUESTS = 0
TOTAL_RESPONSE_TIME = 0
MODEL_NAME = "llama-3.3-70b-versatile"

# load environment variables
load_dotenv()

app = Flask(__name__)


# basic route
@app.route("/")
def home():
    return jsonify({
        "message": "AI Service Running "
    })

# health check (important for project)
@app.route("/health",methods=["GET"])
def health():
    return{"status":"ok"}
    uptime = time.time() - START_TIME
    avg_response_time = (
        TOTAL_RESPONSE_TIME / TOTAL_REQUESTS if TOTAL_REQUESTS > 0 else 0
    )

    return jsonify({
        "status": "UP",
        "model": MODEL_NAME,
        "uptime_seconds": round(uptime, 2),
        "total_requests": TOTAL_REQUESTS,
        "avg_response_time_seconds": round(avg_response_time, 4)
    })


@app.route("/test-prompt", methods=["POST"])
def test_prompt():
    data = request.json
    user_input = data.get("text")

    return jsonify({
        "input": user_input,
        "message": "Prompt ready (AI integration next step)"
    })



@app.route("/describe", methods=["POST"])
def describe():
    start = time.time()   

    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    

    user_input = data["text"]

    with open("prompts/describe_prompt.txt", "r") as f:
        template = f.read()

    final_prompt = template.replace("{input}", user_input)
    ai_response = call_groq(final_prompt)

    if not ai_response:
        return jsonify({
            "description": "AI unavailable",
            "risk_level": "Unknown",
            "explanation": "Fallback response"
        })

    import json
    try:
        parsed = json.loads(ai_response)
        response = jsonify(parsed)  
    except:
        response = jsonify({"raw": ai_response})   

    end = time.time()   

    print("Response Time:", end - start)

    global TOTAL_REQUESTS, TOTAL_RESPONSE_TIME
    TOTAL_REQUESTS += 1
    TOTAL_RESPONSE_TIME += (end - start)

    return response  

    
@app.route("/recommend", methods=["POST"])
def recommend():
    start = time.time()   

    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["text"]

    with open("prompts/recommend_prompt.txt", "r") as f:
        template = f.read()

    final_prompt = template.replace("{input}", user_input)
    ai_response = call_groq(final_prompt)

    import json
    try:
        parsed = json.loads(ai_response)
        response = jsonify(parsed)   
    except:
        response = jsonify({"raw": ai_response})  

    end = time.time()

    global TOTAL_REQUESTS, TOTAL_RESPONSE_TIME
    TOTAL_REQUESTS += 1
    TOTAL_RESPONSE_TIME += (end - start)

    return response
    
    
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["text"]

    result = analyze_security_issue(user_input)

    return jsonify(result)

from services.analysis_service import generate_report


@app.route("/generate-report", methods=["POST"])
def generate_report_route():
    start = time.time()

    data = request.json

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    text = data.get("text", "").strip()

    
    if not text or len(text.strip()) < 10 or text.isalpha() and len(text.split()) <= 2:
        return jsonify({
            "is_fallback": True,
            "title": "Invalid Input",
            "summary": "Input is too weak or not meaningful",
            "overview": "",
            "key_items": [],
            "recommendations": []
        }), 400

    result = generate_report(text)

    response = jsonify(result)

    end = time.time()

    global TOTAL_REQUESTS, TOTAL_RESPONSE_TIME
    TOTAL_REQUESTS += 1
    TOTAL_RESPONSE_TIME += (end - start)

    print("🔥 NEW CODE RUNNING")
    print(request.json)
    return response 

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "frame-ancestors 'none'; "
    "form-action 'self';"
)
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    response.headers.pop("Server", None)

    return response

@app.errorhandler(404)
def not_found(e):
    response = jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found"
    })
    response.status_code = 404
    return response

@app.route("/metrics", methods=["GET"])
def metrics():
    avg = 0
    if TOTAL_REQUESTS > 0:
        avg = TOTAL_RESPONSE_TIME / TOTAL_REQUESTS

    return jsonify({
        "total_requests": TOTAL_REQUESTS,
        "average_response_time": avg
    })

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, request_handler=CustomHandler)