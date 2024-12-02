from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
from test_crew.tools.custom_tool import PcapTool

# Check our tools documentations for more information on how to use them
from crewai_tools import FileReadTool
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Set, Tuple
from enum import Enum

# log findings pydantic model
class log_finding_types(str, Enum):
    missing = 'missing line'
    repeted = 'repeted line'
    error = 'error line'

class log_finding(BaseModel):
    type: log_finding_types = Field(..., description="The type of the finding.")
    details: str = Field(..., description="Why this finding explain the symptoms")

class log_findings(BaseModel):
    findings: List[log_finding] = Field(..., description="The list of log_file_finding")

# pcap findings pydantic model
class pcap_finding_types(str, Enum):
    missing = 'missing packet'
    repeted = 'repeted packets'
    error = 'error packet'

class pcap_finding(BaseModel):
    type: log_finding_types = Field(..., description="The type of the finding.")
    details: str = Field(..., description="Why this finding explain the symptoms")

class pcap_findings(BaseModel):
    findings: List[pcap_finding] = Field(..., description="The list of log_file_finding")

@CrewBase
class TestCrew():
	"""TestCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def cisco_expert(self) -> Agent:
		file_read_tool = FileReadTool()
		return Agent(
			config=self.agents_config['cisco_expert'],
			tools=[file_read_tool],
			llm=LLM(model="ollama/qwen2.5:32b", base_url="http://localhost:11434"),
			verbose=True
		)

	@agent
	def pcap_expert(self) -> Agent:
		file_read_tool = FileReadTool()
		pcaptool = PcapTool()
		return Agent(
			config=self.agents_config['pcap_expert'],
			tools=[file_read_tool, pcaptool],
			llm=LLM(model="ollama/qwen2.5:32b", base_url="http://localhost:11434"),
			verbose=True
		)
	
	@agent
	def network_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['network_engineer'],
			llm=LLM(model="ollama/qwen2.5:32b", base_url="http://localhost:11434"),
			verbose=True
		)

	@task
	def analyse_cisco_log(self) -> Task:
		return Task(
			config=self.tasks_config['analyse_cisco_log'],
			output_pydantic=log_findings
		)

	@task
	def analyse_packet_capture(self) -> Task:
		return Task(
			config=self.tasks_config['analyse_packet_capture'],
			output_pydantic=pcap_findings
		)
	
	@task
	def final_report(self) -> Task:
		return Task(
			config=self.tasks_config['final_report'],
			output_file='report.md',
			# context=[self.analyse_cisco_log, self.analyse_packet_capture]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TestCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
