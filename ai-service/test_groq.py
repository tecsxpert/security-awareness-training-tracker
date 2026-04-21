from services.groq_client import GroqClient

client = GroqClient()

res = client.generate_response("Explain phishing attack in 2 lines")

if res["success"]:
    print("\nAI Response:\n")
    print(res["response"])
else:
    print("\nError:\n", res["error"])