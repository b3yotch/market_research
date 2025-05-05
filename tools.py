from dotenv import load_dotenv
import os
import json
import requests
from crewai_tools import SerperDevTool
from crewai.tools import tool

# Load environment variables
load_dotenv()

# Set API keys from .env
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
github_token = os.getenv("GIT_HUB_API")
kaggle_user = os.getenv("KAGGLE_USERNAME")
kaggle_key = os.getenv("KAGGLE_KEY")

# Initialize Serper tool (optional fallback tool)
serper_tool = SerperDevTool()

# Kaggle Search Tool
class KaggleDatasetSearchTool:
    def __init__(self, username, key):
        from kaggle.api.kaggle_api_extended import KaggleApi
        self.username = username
        self.key = key
        self.api = KaggleApi()
        self.api.authenticate()

    def search(self, query: str):
        results = self.api.dataset_list(search=query)
        return [{"title": d.title, "ref": d.ref} for d in results]


# GitHub Search Tool
class GitHubSearchTool:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com/search/repositories"

    def search(self, query: str):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        params = {"q": query, "sort": "stars", "order": "desc"}
        response = requests.get(self.base_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            return f"GitHub API Error: {response.status_code} - {response.text}"


# Formatting helpers for markdown output
def format_kaggle_markdown(results):
    return "\n".join([f"- **{r['title']}**\n  - Link: https://www.kaggle.com/datasets/{r['ref']}" for r in results])

def format_github_markdown(results):
    return "\n".join([
        f"- **{repo['name']}**\n  - URL: {repo['html_url']}\n  - ⭐ {repo['stargazers_count']}"
        for repo in results if isinstance(repo, dict)
    ])

# CrewAI-compatible tool wrapper using Tool class
def kaggle_search(query: str):
    tool = KaggleDatasetSearchTool(kaggle_user, kaggle_key)
    results = tool.search(query)
    return format_kaggle_markdown(results)

def github_search(query: str):
    tool = GitHubSearchTool(github_token)
    results = tool.search(query)
    return format_github_markdown(results)

# Create custom tools for CrewAI by extending BaseTool
# Create custom tools using crewai's tool decorator
@tool("KaggleSearch")
def kaggle_search(query: str) -> str:
    """Search Kaggle datasets related to a given topic"""
    tool = KaggleDatasetSearchTool(kaggle_user, kaggle_key)
    results = tool.search(query)
    return format_kaggle_markdown(results)

@tool("GitHubSearch")
def github_search(query: str) -> str:
    """Search GitHub repositories related to a given topic"""
    search_tool = GitHubSearchTool(github_token)
    results = search_tool.search(query)
    return format_github_markdown(results)

# Export tools
__all__ = [
    "kaggle_search",
    "github_search",
    "serper_tool"
]