import requests
import json

with open("demo_inputs.json") as f:
    data = json.load(f)

results = []

for item in data:
    response = requests.post(
        "http://127.0.0.1:5000/generate-report",
        json=item
    )

    results.append(response.json())

with open("demo_outputs.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Demo outputs generated")