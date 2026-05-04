from services.groq_client import GroqClient

client = GroqClient()

# 10 NEW inputs (different from Day 6)
test_inputs = [
    "What is a phishing email?",
    "How to detect a fake website?",
    "Explain cyber attack in simple words",
    "What is password hygiene?",
    "Why should we not share OTP?",
    "Explain identity theft",
    "What is secure browsing?",
    "How do hackers use social media?",
    "What is data privacy?",
    "Tips to avoid online scams"
]


# Better scoring (out of 5)
def score_response(response):
    score = 0
    text = response.lower()

    # clarity
    if len(response.split()) <= 60:
        score += 1

    # relevance
    if any(word in text for word in ["security", "attack", "safe", "protect"]):
        score += 1

    # actionable advice
    if any(word in text for word in ["avoid", "check", "use", "never", "enable"]):
        score += 1

    # structured (bullet or newline)
    if "-" in response or "\n" in response:
        score += 1

    # meaningful
    if len(response) > 25:
        score += 1

    return score


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
            print("Score:", score, "/5")

            if score < 4:
                print("⚠ Needs improvement")
                

        else:
            print("Error:", res["error"])

    avg = total / len(test_inputs)
    print("\nAverage Score:", round(avg, 2), "/5")


if __name__ == "__main__":
    run_tests()