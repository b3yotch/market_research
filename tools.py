# tools.py (REFINED)
from dotenv import load_dotenv
import os
import requests
import time
from crewai_tools import SerperDevTool
from crewai.tools import tool

load_dotenv()

# Set API keys
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
github_token = os.getenv("GITHUB_API")  # Fixed typo
kaggle_user = os.getenv("KAGGLE_USERNAME")
kaggle_key = os.getenv("KAGGLE_KEY")

serper_tool = SerperDevTool()

# Helper Classes (keep these)
class KaggleDatasetSearchTool:
    def __init__(self, username, key):
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            self.api = KaggleApi()
            self.api.authenticate()
        except Exception as e:
            print(f"Kaggle authentication failed: {e}")
            self.api = None

    def search(self, query: str, max_results: int = 10):
        if not self.api:
            return [{"title": "Kaggle API not available", "ref": "authentication-failed"}]
        
        try:
            results = self.api.dataset_list(search=query, page_size=max_results)
            return [{"title": d.title, "ref": d.ref, "size": getattr(d, 'totalBytes', 'Unknown')} for d in results[:max_results]]
        except Exception as e:
            return [{"title": f"Search failed: {str(e)}", "ref": "error"}]

class GitHubSearchTool:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com/search/repositories"

    def search(self, query: str, max_results: int = 10):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": max_results}
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("items", [])[:max_results]
            elif response.status_code == 403:
                return [{"name": "Rate limited", "html_url": "https://github.com", "stargazers_count": 0}]
            else:
                return [{"name": f"API Error {response.status_code}", "html_url": "error", "stargazers_count": 0}]
        except Exception as e:
            return [{"name": f"Request failed: {str(e)}", "html_url": "error", "stargazers_count": 0}]

# Formatting functions (improved)
def format_kaggle_markdown(results):
    if not results:
        return "No Kaggle datasets found."
    
    formatted = "## Kaggle Datasets\n\n"
    for r in results:
        formatted += f"- **{r['title']}**\n"
        formatted += f"  - Link: https://www.kaggle.com/datasets/{r['ref']}\n"
        if 'size' in r:
            formatted += f"  - Size: {r['size']}\n"
        formatted += "\n"
    return formatted

def format_github_markdown(results):
    if not results:
        return "No GitHub repositories found."
    
    formatted = "## GitHub Repositories\n\n"
    for repo in results:
        if isinstance(repo, dict) and 'name' in repo:
            formatted += f"- **{repo['name']}**\n"
            formatted += f"  - URL: {repo['html_url']}\n"
            formatted += f"  - ⭐ Stars: {repo['stargazers_count']}\n"
            if 'description' in repo and repo['description']:
                formatted += f"  - Description: {repo['description'][:100]}...\n"
            formatted += "\n"
    return formatted

# CrewAI Tools (REMOVE DUPLICATES)
@tool("kaggle_search")
def kaggle_search(query: str) -> str:
    """Search Kaggle datasets related to a specific topic or use case"""
    tool_instance = KaggleDatasetSearchTool(kaggle_user, kaggle_key)
    results = tool_instance.search(query)
    return format_kaggle_markdown(results)

@tool("github_search")  
def github_search(query: str) -> str:
    """Search GitHub repositories related to a specific topic or technology stack"""
    tool_instance = GitHubSearchTool(github_token)
    results = tool_instance.search(query)
    return format_github_markdown(results)

@tool("huggingface_search")
def huggingface_search(query: str) -> str:
    """Search HuggingFace model hub for models or datasets related to a query."""
    base = "https://huggingface.co/api/models"
    try:
        resp = requests.get(base, params={"search": query, "limit": 10}, timeout=10)
        if resp.status_code != 200:
            return "HF search failed"
        items = resp.json()[:10]
        if not items:
            return "No HF models found."
        md = "## HuggingFace Models / Datasets\n\n"
        for m in items:
            md += f"- **{m.get('modelId','–')}**  \n"
            md += f"  - Link: https://huggingface.co/{m.get('modelId')}  \n"
            md += f"  - ⭐ {m.get('likes',0)}\n\n"
        return md
    except Exception as e:
        return f"HuggingFace error: {e}"