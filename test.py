import os
import requests
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Get Serper API key
'''SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Check if key exists
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in .env file")

# Set the endpoint and headers
url = "https://google.serper.dev/search"
headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

# Set a simple query
payload = {
    "q": "Tata Motors latest news"
}

# Make the request
response = requests.post(url, headers=headers, json=payload)

# Check response
if response.status_code == 200:
    print("✅ Serper API Key is valid!")
    print("Sample result:", response.json())
else:
    print(f"❌ Failed. Status Code: {response.status_code}")
    print("Response:", response.text)'''

groq_api_key=os.getenv("GROQ_API_KEY")
print(groq_api_key)