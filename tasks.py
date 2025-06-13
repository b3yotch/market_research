# tasks.py (REFINED)
from crewai import Task
from agents import MarketResearchAgent, UseCaseAgent, ResourceCollectionAgent, ProposalSynthesiserAgent


market_research_task = Task(
    description=(
        "Conduct comprehensive market research for {topic}. Your analysis must include:\n"
        "1. Industry overview and market size\n"
        "2. Key players \n" 
        "3. Current AI/ML adoption trends in this industry\n"
        "4. Strategic focus areas (operations, supply chain, customer experience)\n"
        "5. Recent developments and future outlook\n\n"
        "Reference authoritative sources like McKinsey, Deloitte, PwC, and industry reports."
    ),
    expected_output=(
        "Structured markdown report with sections:\n"
        "# Market Research Report: {topic}\n"
        "## Executive Summary\n"
        "## Industry Overview\n" 
        
        "## AI/ML Adoption Trends\n"
        "## Strategic Opportunities\n"
        "## References"
    ),
    agent=MarketResearchAgent,
    output_file="market_research_report.md"
)

use_case_generation_task = Task(
    description=(
        "Using **market_research_report.md** generate GENAI / ML use-cases.\n"
        "For EACH use-case include:\n"
        "• Linked Insight/Reference (e.g. [Ref-3])\n"
        "• ImpactScore(1-5)  FeasibilityScore(1-5)\n"
        "• Description | Business Value | Technical Reqs | Timeline\n"
        "Return the top-5 sorted by (Impact*Feasibility) then the long-tail."
    ),
    expected_output=(
        "Structured markdown report:\n"
        "# AI/ML Use Cases for {topic}\n"
        "## Priority Use Cases (Top 5)\n"
        "## Operational Efficiency Use Cases\n"
        "## Customer Experience Use Cases\n"
        "## Innovation & Growth Use Cases\n"
        "## Implementation Roadmap\n"
        "Each use case should include: Description, Business Value, Technical Requirements, Timeline"
    ),
    agent=UseCaseAgent,
    context=[market_research_task],  # Explicit dependency
    output_file="use_cases_report.md"
)

resource_collection_task = Task(
    description=(
        "Based on the identified use cases for {topic}, curate relevant technical resources:\n"
        "1. Search for datasets on Kaggle that support the use cases\n"
        "2. Find relevant GitHub repositories with implementations\n"
        "3. Identify pre-trained models on Hugging Face\n"
        "4. Provide actionable recommendations for each resource\n\n"
        "Focus on high-quality, well-maintained resources with good documentation."
    ),
    expected_output=(
        "Comprehensive resource collection in markdown:\n"
        "# Technical Resources for {topic}\n"
        "## Datasets (Kaggle)\n"
        "## Code Repositories (GitHub)\n" 
        "## Pre-trained Models (Hugging Face)\n"
        "## Recommended Implementation Stack\n"
        "Each resource should include: Title, Platform, Direct Link, Relevance Score, Usage Notes"
    ),
    agent=ResourceCollectionAgent,
    context=[market_research_task, use_case_generation_task],  # Depends on both previous tasks
    output_file="technical_resources.md"
)


final_proposal_task = Task(
    description=(
        "Read **market_research_report.md**, **use_cases_report.md**, "
        "and **technical_resources.md** then craft a polished proposal:\n"
        "1. Executive Summary (≤200 words)\n"
        "2. Top-5 Use-Cases table (Name, ImpactScore, FeasibilityScore, ROI rationale)\n"
        "3. Implementation Roadmap (Phases, 0-24 m)\n"
        "4. Risks & Mitigations\n"
        "5. Resource Appendix (clickable links) \n"
        "6. References\n"
        "Format: markdown"
    ),
    expected_output="# Final AI / GenAI Proposal for {topic}",
    agent=ProposalSynthesiserAgent,
    context=[market_research_task, use_case_generation_task, resource_collection_task],
    output_file="final_proposal.md"
)

__all__ = [
    "market_research_task",
    "use_case_generation_task",
    "resource_collection_task",
    "final_proposal_task"
]