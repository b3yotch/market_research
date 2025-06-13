import argparse
from crewai import Crew
from tasks import (
    market_research_task,
    use_case_generation_task,
    resource_collection_task,
    final_proposal_task
)

def main(topic: str):
    crew = Crew(tasks=[
        
    
        final_proposal_task
    ])
    crew.kickoff(inputs={'topic':'Tata Motors'})
    print("🏁  Pipeline finished.  Check the generated *.md files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="Tata Motors", help="Company / Industry")
    args = parser.parse_args()
    main(args.topic)