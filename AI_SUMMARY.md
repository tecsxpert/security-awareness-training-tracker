# Security Awareness Training Tracker

## Overview
A secure AI-powered web application designed to educate users about cybersecurity threats such as phishing, malware, and social engineering. The system integrates an AI model with strong security controls to prevent misuse and ensure safe responses.

---

## Tech Stack

### Backend
- Java (Spring Boot)
- REST APIs
- RestTemplate (AI integration)

### AI Service
- Python (Flask)
- Groq API (LLaMA 3.1)
- Prompt tuning & validation

### Security
- JWT Authentication
- Rate Limiting (30 req/min)
- Input Sanitization
- Prompt Injection Detection
- PII Detection

### Infrastructure
- Docker & Docker Compose
- PostgreSQL
- Redis

---

## Key Endpoints

### 1️. Login
POST `/login`  
→ Returns JWT token  

---

### 2️. Generate AI Response
POST `/api/ai/generate`  
→ Requires JWT  
→ Returns secure AI-generated response  

---

### 3️. Health Check
GET `/health`  
→ Returns system status  

---

## Security Features

✔ Input validation & sanitization  
✔ Prompt injection protection  
✔ Rate limiting (30 req/min)  
✔ JWT-secured endpoints  
✔ PII detection & blocking  
✔ Secure environment variables (.env)  
✔ OWASP ZAP tested  

---

## Testing & Validation

- Unit testing using **pytest**
- Security testing:
  - Empty input validation
  - SQL injection protection
  - Prompt injection detection
- OWASP ZAP scan:
  - No critical vulnerabilities
  - Medium issues fixed
- End-to-end Docker testing

---

## Key Highlights

- Secure AI integration
- Microservices architecture
- Real-world cybersecurity use case
- Production-style deployment
- External API rate-limit handling

---

## GitHub Repository

👉 https://github.com/Shreevathsa-V/security-awareness-training-tracker/tree/shreevathsa-v

---

## Developed By

**Shreevathsa V**  
AI Developer-1  

---