from datetime import datetime
from anthropic import Anthropic

client = Anthropic(
    base_url="*****",
    api_key="*****"
)

prompt = """"You will be acting as a health monitoring request classification system. Your task is to analyze user health-related requests and output the appropriate classification intent, along with your reasoning.

Here is the health request you need to classify:

<request>{user_request}</request>

Please carefully analyze the above request to determine the user's core health needs and concerns.

First, write out your reasoning and analysis of how to classify this request inside <reasoning> tags.

Then, output the appropriate classification label for the request inside an <intent> tag. The valid intents are:
<intents>
<intent>Health Monitoring: Track vital signs, steps, sleep patterns, and blood sugar levels via wearables</intent>
<intent>Medication Management: Medication reminders and interaction alerts</intent>
<intent>Diet and Nutrition: Food tracking, meal planning, and dietary recommendations</intent>
<intent>Appointment Scheduling: Medical appointment scheduling and calendar integration</intent>
<intent>Health Insights and Alerts: Health reports and anomaly detection</intent>
<intent>Fitness Guidance: Personalized workout plans and exercise feedback</intent>
<intent>Mental Health Support: Meditation, mindfulness, and therapy resources</intent>
</intents>

A request may have ONLY ONE applicable intent. Choose the intent that best addresses the user's primary need.

Example classification:
<request>I need help tracking my daily blood sugar readings and getting alerts if they go too high.</request>

<reasoning>
The user is specifically asking about monitoring blood sugar levels and receiving alerts based on those readings. While this could involve health insights, the primary focus is on ongoing health monitoring of a specific vital sign.</reasoning>

<intent>Health Monitoring</intent>"""

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
    now = datetime.now()
    message = client.messages.create(
        # https://docs.anthropic.com/en/docs/about-claude/use-case-guides/ticket-routing
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt.format(user_request=query)
                    }
                ],
            }
        ],
    )
    print(message)
    intent = message.content[0].text.split("<intent>")[1].split("</intent>")[0]
    print(f"Query: {query}: {intent}")
    print("Time taken:", (datetime.now() - now).total_seconds())
    print("--------------------------------------------------")
    print("--------------------------------------------------")
