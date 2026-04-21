from flask import Flask, jsonify
from dotenv import load_dotenv
import os

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
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "AI Service",
        "port": 5000
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)