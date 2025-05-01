from crewai import Agent
from dotenv import load_dotenv
import os
from tools import tool

load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
# Get Groq API key
groq_api_key=os.get_env("GROQ_API_KEY")
from langchain_groq import ChatGroq


MarketResearchAgent = Agent(
    role="Market Research Agent",
    goal="Research the market for {topic}",
    llm=ChatGroq(temperature=0,
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
    llm=ChatGroq(temperature=0,
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
    allow_delegation=False
)
