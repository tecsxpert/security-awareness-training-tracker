# Security Awareness Training Tracker

## Overview
A secure AI-powered web application that educates users about cybersecurity threats like phishing, malware, and social engineering.

The system integrates AI with strong security controls to ensure safe and reliable responses.

---

## Tech Stack

### Backend
- Java (Spring Boot)
- REST APIs

### AI Service
- Python (Flask)
- Groq API (LLaMA 3.1)

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

- POST `/login` → Get JWT token  
- POST `/api/ai/generate` → AI response (secured)  
- GET `/health` → System status  

---

## Security Features

- Input validation & sanitization  
- Prompt injection protection  
- JWT-secured endpoints  
- Rate limiting  
- PII detection  
- OWASP ZAP tested  

---

## Testing

- Unit testing (pytest)  
- Injection testing  
- OWASP ZAP scan  
- End-to-end Docker testing  

---

## How to Run

```bash
docker-compose up --build
```

---

## Documentation

- Security Report → SECURITY.md
- AI Summary → AI_SUMMARY.md
- Talking Points → AI_TALKING_POINTS.md

---

## Team

|       Name        |       Role        |
|-------------------|-------------------|
| Bhagyashree Jakti | Java Developer 1  |
| Pretha S K        | Java Developer 2  |
| R Dhatri Urs      | AI Developer 1    |
| Shreevathsa V     | AI Developer 2    |
| Zoya Nigar        | Security Reviewer |

---

## Highlights

- Secure AI integration
- Microservices architecture
- Real-world cybersecurity use case
- Production-style deployment