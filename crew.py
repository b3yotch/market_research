from crewai import Process , Crew
from tools import tool
from agents import MarketResearchAgent, Use_case_Agent,Resource_Collection_Agent
from tasks import MarketResearchTask,UseCaseTask,ResourceCollectionTask

crew=Crew(agents=[MarketResearchAgent,Use_case_Agent,Resource_Collection_Agent],
          tasks=[MarketResearchTask,UseCaseTask, ResourceCollectionTask],
          
          process=Process.sequential)

result= crew.kickoff(inputs={'topic':'Tata Motors'})
print(result)