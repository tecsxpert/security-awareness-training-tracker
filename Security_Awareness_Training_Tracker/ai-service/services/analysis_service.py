import json
from services.groq_client import call_groq
from services.cache_service import generate_key, get_cache, set_cache

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

def generate_report(user_input):
    import json
    import re

    
    key = generate_key(user_input)

    # 🔹 Check cache
    cached = get_cache(key)
    if cached:
        return cached

    try:
        with open("prompts/report_prompt.txt", "r") as f:
            template = f.read()

        final_prompt = template.replace("{input}", user_input)

        
        response = call_groq(final_prompt)

        if not response:
            return {
                "is_fallback": True,
                "title": "AI Unavailable",
                "summary": "Failed to fetch AI response",
                "overview": "",
                "key_items": [],
                "recommendations": []
            }

        
        # 🔹 Extract JSON safely
        json_match = re.search(r'\{.*\}', response, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found")

        data = json.loads(json_match.group())

        result = {
        "title": data.get("title", "Security Report"),
        "summary": data.get("summary", ""),
        "overview": data.get("overview", ""),
        "key_items": data.get("key_items", []),
        "recommendations": data.get("recommendations", []),
        "is_fallback": False   
    }

        set_cache(key, result)

        return result

    except Exception as e:
        print(" ERROR:", str(e))
        return {
        "title": "Report unavailable",
        "summary": "AI service failed, using fallback response",
        "overview": "",
        "key_items": [],
        "recommendations": [],
        "is_fallback": True   
    }