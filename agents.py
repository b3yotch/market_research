# agents.py (REFINED)
from crewai import Agent
from dotenv import load_dotenv
import os
from tools import serper_tool, kaggle_search, github_search
from rate_limiter import groq_call
load_dotenv()
from langchain_groq import ChatGroq

groq_api_key = os.getenv("GROQ_API_KEY")

# Use consistent model and enable memory for better context retention
llm = ChatGroq(
    temperature=0.4,
    model="groq/compound-beta",  # Use same model for consistency
    api_key=groq_api_key
)
llm1 = ChatGroq(
    temperature=0.4,
    model="groq/compound-beta-mini",  # Use same model for consistency
    api_key=groq_api_key
)
llm2 = ChatGroq(
    temperature=0.4,
    model="groq/llama-3.3-70b-versatile",  # Use same model for consistency
    api_key=groq_api_key
)

MarketResearchAgent = Agent(
    role="Market Research Analyst",
    goal="Conduct comprehensive market research and competitive analysis for {topic}",
    llm=llm1,
    verbose=True,
    memory=True,  # Enable memory for context retention
    backstory=(
        "You are a senior market research analyst with expertise in {topic} industry analysis. "
        "Your mission is to provide detailed insights into market positioning, competitive landscape, "
        "industry trends, and business opportunities. You excel at identifying key players, "
        "market dynamics, and strategic initiatives in operations, supply chain, and customer experience."
    ),
    tools=[serper_tool],
    allow_delegation=False,  # Keep focused on research
    max_iter=2  # Limit iterations to prevent infinite loops
)

UseCaseAgent = Agent(
    role="AI Strategy Consultant",
    goal="Generate actionable GenAI/LLM/ML use cases based on market research for {topic}",
    llm=llm,
    verbose=True,
    memory=True,
    backstory=(
        "You are an AI strategy consultant ... "
        "For EVERY use-case you output you MUST:\n"
        "• Cite one concrete research insight (with ref #)\n"
        "• Provide ImpactScore(1-5) and FeasibilityScore(1-5)\n"
        "• Higher-score ideas will appear first."
    ),
    tools=[serper_tool],
    allow_delegation=False,
    max_iter=2
)

ResourceCollectionAgent = Agent(
    role="Technical Resource Curator",
    goal="Identify and curate relevant datasets, models, and code repositories for {topic} use cases",
    llm=llm,  # Lower temp for precision
    verbose=True,
    memory=True,
    backstory=(
        "You are a technical resource curator with deep knowledge of ML/AI datasets and open-source repositories. "
        "You specialize in finding high-quality, relevant resources from Kaggle, GitHub, and Hugging Face "
        "that align with specific use cases and business requirements. You provide detailed, actionable resource recommendations."
    ),
    tools=[kaggle_search, github_search],
    allow_delegation=False,
    max_iter=2
)

ProposalSynthesiserAgent = Agent(
    role="Proposal Synthesiser",
    goal="Combine research, use-case list and resources into a single client-ready proposal",
    llm=llm2,
    verbose=True,
    memory=False,
    backstory=(
        "You are a management-consulting partner.  You read three markdown files "
        "and craft an executive proposal with summary, prioritised use-cases, "
        "ROI table, resource appendix and references."
    ),
    tools=[serper_tool],
    max_iter=1,
    allow_delegation=False
)

__all__ = [
  "MarketResearchAgent",
  "UseCaseAgent",
  "ResourceCollectionAgent",
  "ProposalSynthesiserAgent"
]