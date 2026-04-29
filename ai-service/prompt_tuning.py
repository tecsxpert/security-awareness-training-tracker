from services.groq_client import GroqClient

client = GroqClient()

test_inputs = [
    "What is phishing?",
    "How do hackers steal passwords?",
    "Explain malware in simple terms",
    "What is social engineering?",
    "How to identify fake emails?",
    "What is ransomware?",
    "How to stay safe online?",
    "Explain data breach",
    "What is two-factor authentication?",
    "How to avoid phishing attacks?"
]

def score_response(response):
    score = 0

    if len(response.split()) <= 50:
        score += 3  # concise

    if "password" in response.lower() or "security" in response.lower():
        score += 3  # relevant keywords

    if len(response) > 10:
        score += 2  # meaningful

    if "error" not in response.lower():
        score += 2  # valid

    return score  # out of 10


def run_tests():
    total = 0

    for i, inp in enumerate(test_inputs, 1):
        print(f"\nTest {i}: {inp}")

        res = client.generate_response(inp)

        if res["success"]:
            response = res["response"]
            score = score_response(response)
            total += score

            print("Response:", response)
            print("Score:", score)

            if score < 7:
                print("⚠ Needs improvement")

        else:
            print("Error:", res["error"])

    print("\nAverage Score:", total / len(test_inputs))


if __name__ == "__main__":
    run_tests()