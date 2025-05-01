from crewai import Process , Crew
from tools import tool
from agents import MarketResearchAgent, Use_case_Agent
from tasks import MarketResearchTask,UseCaseTask

crew=Crew(agents=[MarketResearchAgent,Use_case_Agent],
          tasks=[MarketResearchTask,UseCaseTask],
          
          process=Process.sequential)

result= crew.kickoff(inputs={'topic':'Tata Motors'})
print(result)