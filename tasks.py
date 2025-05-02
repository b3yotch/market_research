from crewai import Task
from tools import tool
from agents import MarketResearchAgent, Use_case_Agent, Resource_Collection_Agent

MarketResearchTask = Task(
    description=(
        "Conduct in-depth market research for {topic}. "
        "Identify the company's core business segments, key offerings, and strategic initiatives "
        "in areas like operations, supply chain, and digital transformation. "
        "You can also  refer to reports and insights on AI and digital transformation from industry-specific sources such as McKinsey, Deloitte, or Nexocode."
        "also identify the competitors and add what they are doing better."
        
    ),
    expected_output="A comprehensive market analysis report on {topic} including industry positioning, competitive landscape, and key business areas.",
    agent=MarketResearchAgent ,
    output_file="market_research.txt"
)

UseCaseTask = Task(
    description="Using the market research conducted on {topic}, analyze industry trends and suggest GenAI/LLM/ML use cases. Recommend improvements in customer experience, operations, or innovation. Also based on the market research agents' competitor analysis  suggest appropriate measures to outdo them",
    expected_output="Markdown report with sections: [Industry Trends], [Use Cases], [Suggested Improvements using GenAI, LLM, ML]",
    
    agent=Use_case_Agent,
    async_execution=False,
    output_file="use_case.txt"
)

ResourceCollectionTask = Task(
    description="Using the use cases generated  on {topic}, analyze industry trends and extract relevant datasets from kaggle, hugging face , git hub.",
    expected_output=(
    "Markdown report with a list of 5–10 relevant datasets or repositories. "
    "Each item should include:\n"
    "- **Title**\n"
    "- **Platform** (Kaggle / GitHub / Hugging Face)\n"
    "- **Direct Link**\n"
    "- **Short Description** (1–2 lines)\n"
)
,
    
    agent=Resource_Collection_Agent,
    async_execution=False,
    output_file="resource.txt"
)
