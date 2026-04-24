import json
from services.groq_client import call_groq


def analyze_security_issue(user_input):
    # default safe values (used if anything fails)
    describe_data = {
        "description": "AI unavailable",
        "risk_level": "Unknown",
        "explanation": "Fallback response"
    }
    recommend_data = []

    try:
        # -------- DESCRIBE --------
        with open("prompts/describe_prompt.txt", "r") as f:
            describe_template = f.read()

        describe_prompt = describe_template.replace("{input}", user_input)
        describe_response = call_groq(describe_prompt)

        try:
            parsed = json.loads(describe_response)
            if isinstance(parsed, dict):
                describe_data = parsed
        except:
            pass

        # -------- RECOMMEND --------
        with open("prompts/recommend_prompt.txt", "r") as f:
            recommend_template = f.read()

        recommend_prompt = recommend_template.replace("{input}", user_input)
        recommend_response = call_groq(recommend_prompt)

        try:
            parsed = json.loads(recommend_response)
            if isinstance(parsed, list):
                recommend_data = parsed
        except:
            pass

    except Exception as e:
        # log error if needed
        print("Error in analyze_security_issue:", str(e))

    # -------- FINAL RESPONSE (ALWAYS SAFE) --------
    return {
        "description": describe_data.get("description"),
        "risk_level": describe_data.get("risk_level"),
        "explanation": describe_data.get("explanation"),
        "recommendations": recommend_data
    }