from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import send_push_notification
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class TrendingCompany(BaseModel):
    """ Un'azienda presente nelle notizie e che sta attirando attenzione """
    name: str = Field(description="Nome dell'azienda")
    ticker: str = Field(description="Simbolo ticker del titolo")
    reason: str = Field(description="Motivo per cui questa azienda è di tendenza nelle notizie")


class TrendingCompanyList(BaseModel):
    """ Elenco di più aziende di tendenza presenti nelle notizie """
    companies: list[TrendingCompany] = Field(description="Elenco delle aziende di tendenza nelle notizie")


class TrendingCompanyResearch(BaseModel):
    """ Ricerca dettagliata su un'azienda """
    name: str = Field(description="Nome dell'azienda")
    market_position: str = Field(description="Posizione attuale sul mercato e analisi della concorrenza")
    future_outlook: str = Field(description="Prospettive future e potenziale di crescita")
    investment_potential: str = Field(description="Potenziale di investimento e adeguatezza ai fini di un investimento")


class TrendingCompanyResearchList(BaseModel):
    """ Elenco delle ricerche dettagliate su tutte le aziende """
    research_list: list[TrendingCompanyResearch] = Field(description="Ricerca completa su tutte le aziende di tendenza")
@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],
                     tools=[SerperDevTool()], memory=True)
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'],
                     tools=[SerperDevTool()], memory=True)

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], 
                     tools=[send_push_notification], memory=True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
