from crewai import Process , Crew

from agents import MarketResearchAgent, ResourceCollectionAgent,UseCaseAgent
from tasks import MarketResearchTask,UseCaseTask,ResourceCollectionTask

crew=Crew(agents=[MarketResearchAgent,UseCaseAgent,ResourceCollectionAgent],
          tasks=[MarketResearchTask,UseCaseTask, ResourceCollectionTask],
          
          process=Process.sequential)

result= crew.kickoff(inputs={'topic':'Tata Motors'})
print(result)