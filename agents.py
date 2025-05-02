from crewai import Agent
from dotenv import load_dotenv
import os
from tools import tool

load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
# Get Groq API key
groq_api_key=os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq


MarketResearchAgent = Agent(
    role="Market Research Agent",
    goal="Research the market for {topic}",
    llm=ChatGroq(temperature=0.4,
             model="groq/compound-beta-mini",
             api_key=groq_api_key),
    verbose=True,
    memory=False,
    backstory=(
        "You're a specialized market research agent tasked with analyzing {topic}. "
        "Your role is to identify the company's industry segment, key product offerings, and strategic focus areas, "
        "including operations, supply chain, and customer engagement strategies. When using tools like Serper, only pass search terms as plain strings like {'search_query': 'your search here'}."
    ),
    tools=[tool],
    allow_delegation=True
)

Use_case_Agent = Agent(
    role="Use Case Agent",
    goal="Create a use case for the market research agent",
    llm=ChatGroq(temperature=0.4,
             model="groq/compound-beta",
             api_key=groq_api_key),
    verbose=True,
    memory=False,
backstory=(
    "You're an AI strategy consultant. Based on insights provided by the market research agent on {topic}, "
    "you identify how GenAI, LLMs, and ML can drive improvements in operations, customer experience, innovation and  its products  . When using tools like Serper, only pass search terms as plain strings like {'search_query': 'your search here'}. "
)
,
    tools=[tool],
    allow_delegation=True
)


Resource_Collection_Agent = Agent(
    role="Resource_Collection_Agent ",
    goal="prepare relevant resources based on the use case generated ",
    llm=ChatGroq(temperature=0.2,
             model="groq/gemma2-9b-it",
             api_key=groq_api_key),
    verbose=True,
    memory=False,
backstory=(
    "You are a resource analyst specialized in identifying high-quality, relevant datasets and assets from platforms like Kaggle, GitHub, and Hugging Face. "
    "You analyze the use cases related to {topic} and search for datasets, models, or repos that can support implementation. "
    "Use keyword-based searches and return results in markdown format. "
    "When using tools like Serper, only pass search terms as plain strings like {'search_query': 'your search here'}."
)

,
    tools=[tool],
    allow_delegation=False
)