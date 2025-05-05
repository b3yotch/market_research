import os
import requests
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

# Load your .env file
load_dotenv()

# ---------- Serper API Check ----------
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if SERPER_API_KEY:
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": "Tata Motors latest news"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Serper API Key is valid!")
        print("Sample result:", response.json()["organic"][0]["title"])
    else:
        print(f"❌ Serper failed with status {response.status_code}: {response.text}")
else:
    print("⚠️ SERPER_API_KEY not found in .env")


# ---------- Groq API Check ----------
groq_api_key = "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"
if groq_api_key:
    print("✅ GROQ_API_KEY loaded successfully.")
else:
    print("❌ GROQ_API_KEY not found.")


# ---------- GitHub API Check ----------
github_token = "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"
if github_token:
    gh_headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    gh_params = {"q": "Tata Motors", "sort": "stars", "order": "desc"}
    gh_response = requests.get("https://api.github.com/search/repositories", headers=gh_headers, params=gh_params)
    if gh_response.status_code == 200:
        top_repo = gh_response.json()["items"][0]
        print("✅ GitHub API Key is valid!")
        print("Top repo:", top_repo["full_name"])
    else:
        print(f"❌ GitHub API failed with status {gh_response.status_code}: {gh_response.text}")
else:
    print("⚠️ GIT_HUB_API not found in .env")


# ---------- Kaggle API Check ----------
'''kaggle_user = os.getenv("KAGGLE_USERNAME")
kaggle_key = os.getenv("KAGGLE_KEY")
if kaggle_user and kaggle_key:
    try:
        os.environ["KAGGLE_USERNAME"] = kaggle_user
        os.environ["KAGGLE_KEY"] = kaggle_key
        kaggle_api = KaggleApi()
        kaggle_api.authenticate()
        datasets = kaggle_api.dataset_list(search="electric vehicle")
        if datasets:
            print("✅ Kaggle API credentials are valid!")
            print("Sample dataset:", datasets[0].title)
        else:
            print("⚠️ Kaggle API worked but no datasets found.")
    except Exception as e:
        print("❌ Kaggle API error:", str(e))
else:
    print("⚠️ KAGGLE_USERNAME or KAGGLE_KEY not found in .env")'''
