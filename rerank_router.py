import httpx
from datetime import datetime

# TEI endpoint (text-embeddings-router --model-id BAAI/bge-reranker-large --port 8080)
endpoint = "127.0.0.1:8080/rerank"

intents = [
    "Health Monitoring",
    "Medication Management",
    "Diet and Nutrition",
    "Appointment Scheduling",
    "Health Insights and Alerts",
    "Fitness Guidance",
    "Mental Health Support"
]

tasks = [
    f"{intents[0]}: Track daily steps, heart rate, sleep patterns, and other vital signs using wearable device data. Monitor blood sugar levels for diabetic users through connected glucose monitors.",
    f"{intents[1]}: Remind users when to take medications based on prescriptions or user input. Alert users about potential drug interactions or side effects.",
    f"{intents[2]}: Analyze food intake by integrating with dietary tracking apps. Suggest meal plans or recipes based on dietary restrictions, allergies, or health goals like weight loss or managing cholesterol.",
    f"{intents[3]}: Schedule, remind, and reschedule medical appointments. Integrate with calendar apps to ensure no conflicts with other commitments.",
    f"{intents[4]}: Generate health reports summarizing activity, diet, sleep, and health metrics. Alert users to any anomalies in health data that might require medical attention.",
    f"{intents[5]}: Recommend personalized workout plans based on fitness levels, goals, and past activity data. Provide real-time feedback during exercises or suggest modifications for injuries.",
    f"{intents[6]}: Offer meditation sessions or mindfulness exercises. Provide cognitive behavioral therapy techniques or connect users to mental health resources if needed."
]

queries = [
    "How many steps did I walk today?",
    "Can you remind me to take my blood pressure medication at 8 PM?",
    "What should I eat for dinner if I want to keep my cholesterol low?",
    "Can you book an appointment with my cardiologist next Thursday?",
    "Show me my sleep pattern from last week.",
    "What exercises can I do with my current back injury?",
    "Is there any interaction between my new allergy medication and my heart medication?",
    "I've been feeling stressed; can you suggest some relaxation techniques?"
]

for query in queries:
    payload_w_description = {
        "query": query,
        "texts": tasks
    }

    payload = {
        "query": query,
        "texts": tasks,
    }

    print("Payload with description:")
    now = datetime.now()
    response = httpx.post(f"http://{endpoint}", json=payload_w_description)
    intent = intents[response.json()[0]["index"]]
    print(f"Query: {query}: {intent}")
    for i, result in enumerate(response.json()):
        print(f"Rank {i + 1}: ({intents[result['index']]}, {result['score']})")
    print(f"Time taken: {(datetime.now() - now).total_seconds()} seconds")
    print()

    print("Payload (just tasks):")
    now = datetime.now()
    response = httpx.post(f"http://{endpoint}", json=payload)
    intent = intents[response.json()[0]["index"]]
    print(f"Query: {query}: {intent}")
    for i, result in enumerate(response.json()):
        print(f"Rank {i + 1}: ({intents[result['index']]}, {result['score']})")
    print(f"Time taken: {(datetime.now() - now).total_seconds()} seconds")
    print("--------------------------------------------------")
    print("--------------------------------------------------")
