# AI Security Awareness Service

##  Overview

This service analyzes user-reported security incidents and generates
structured AI-powered reports.

It uses: - Groq API (LLM) - Flask backend - Fallback handling for
invalid/failed responses

------------------------------------------------------------------------

##  Setup Instructions

### 1. Clone the repository

``` bash
git clone <your-repo-url>
cd Security_Awareness_Training_Tracker/ai-service
```

### 2. Create virtual environment

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file:

    GROQ_API_KEY=your_api_key_here

    Never commit this file to GitHub.

### 5. Run the service

``` bash
python app.py
```

Server runs on: http://127.0.0.1:5000

------------------------------------------------------------------------

## API Endpoints

### Health Check

GET `/health`

Response:

``` json
{
  "status": "healthy"
}
```

------------------------------------------------------------------------

### Analyze Security Issue

POST `/analyze`

Request:

``` json
{
  "text": "User received a suspicious email and clicked the link"
}
```

Response:

``` json
{
  "description": "Phishing attempt",
  "risk_level": "High",
  "explanation": "User interacted with a malicious link",
  "recommendations": [
    "Change passwords",
    "Run antivirus scan"
  ]
}
```

------------------------------------------------------------------------

### Generate Report 

POST `/generate-report`

Request:

``` json
{
  "text": "User clicked suspicious email link"
}
```

Success Response:

``` json
{
  "is_fallback": false,
  "title": "Phishing Incident",
  "summary": "User clicked suspicious link",
  "overview": "Detailed explanation...",
  "key_items": [
    "Suspicious link clicked",
    "Possible malware"
  ],
  "recommendations": [
    "Change password",
    "Scan system"
  ]
}
```

Fallback Response:

``` json
{
  "is_fallback": true,
  "title": "Invalid Input",
  "summary": "Input is too weak or not meaningful",
  "overview": "",
  "key_items": [],
  "recommendations": []
}
```

------------------------------------------------------------------------

## Features

-   AI-powered analysis (Groq)
-   Structured JSON output
-   Fallback system (`is_fallback`)
-   Input validation
-   Error handling
-   Caching support (Redis optional)

------------------------------------------------------------------------
## Day-14 Update (AI Service Validation)

The AI service was successfully tested on a demo machine using Docker.

### Endpoints Tested
- `/generate-report`
- `/analyze`
- `/describe`
- `/health`

All endpoints are live and returning valid structured JSON responses.

---

### Performance Observations
- AI endpoints take a few seconds due to model processing
- Health endpoint responds instantly (~ms)
- System handles fallback scenarios when dependencies are unavailable

---

### Key Highlights
- Dockerized Flask service running successfully
- AI-powered threat analysis working correctly
- Structured outputs include risk level, explanation, and recommendations
- Health endpoint provides uptime and performance metrics

## Screenshots

### Generate Report
![Generate Report](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\generate-report.jpeg)

### Analyze Endpoint
![Analyze](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\analyze.jpeg)

### Describe Endpoint
![Describe](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\describe.jpeg)

### Health Check
![Health-1](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\health-1.jpeg)
![Health-2](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\health-2.jpeg)

### Docker & Flask Running
![Terminal](C:\Security_Awareness_Training_Tracker\Security_Awareness_Training_Tracker\ai-service\backup_screenshots\terminal.jpeg)

## Security

- API keys are stored in `.env`
- `.env` is excluded using `.gitignore`
- No sensitive data is committed to the repository

### Response Time Observations

- /generate-report → ~9–20 seconds (AI processing)
- /analyze → ~1–2 seconds
- /describe → <1 second
- /health → ~40 ms

Note: AI endpoints take longer due to model inference.

### Day-15 Final AI Service Submission

- Docker build verified successfully
- All endpoints tested and working
- README fully updated with screenshots and response times
- Environment variables secured
- Project ready for submission

## Day-16 Validation

### Performance
- Initial AI response: ~10–20 seconds
- Cached responses: ~1–2 seconds

### Cache
- Redis cache tested
- Repeated requests return faster responses

### Fallback
- System returns fallback response when AI is unavailable
- Ensures reliability and no crashes

### Status
- All endpoints verified and within acceptable performance limits

## Day-17 Verification

- Groq API key validated and active
- All endpoints tested successfully:
  - /generate-report
  - /analyze
  - /describe
- No fallback triggered
- Responses are meaningful and correct
- System running successfully via Docker