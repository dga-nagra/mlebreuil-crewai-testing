# Warning control
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
# from helper import load_env
# load_env()
from helpers import get_default_llm, get_ollama_client, get_default_model


import os
import yaml
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, LLM

from IPython.display import display, Markdown


# I get "Connection Reset by peer"
# https://github.com/crewAIInc/crewAI/issues/1337

ollama = get_ollama_client()
model = get_default_model()
# DEFAULT_LLM = get_default_llm()
# print(DEFAULT_LLM.base_url, DEFAULT_LLM.model)

BASE_URL="http://localhost:11430"
os.environ["OPENAI_BASE_URL"] = BASE_URL

# OpenTelemetry is causing issues. We need to disable it.
# https://github.com/crewAIInc/crewAI/issues/372
os.environ["OTEL_SDK_DISABLED"] = "true"

DEFAULT_LLM = LLM('ollama/deepseek-r1:32b', base_url=BASE_URL)


# Define file paths for YAML configurations
files = {
    'agents': 'config_L1/agents.yaml',
    'tasks': 'config_L1/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']



class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description="List of resources required to complete the task")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")


# default_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
default_llm = DEFAULT_LLM  # LLM(model="ollama/llama3.2")

# Creating Agents
project_planning_agent = Agent(
  config=agents_config['project_planning_agent'],
  llm=default_llm,
)

estimation_agent = Agent(
  config=agents_config['estimation_agent'],
  llm=default_llm,
)

resource_allocation_agent = Agent(
  config=agents_config['resource_allocation_agent'],
  llm=default_llm,
)

# Creating Tasks
task_breakdown = Task(
  config=tasks_config['task_breakdown'],
  agent=project_planning_agent,
)

time_resource_estimation = Task(
  config=tasks_config['time_resource_estimation'],
  agent=estimation_agent
)

resource_allocation = Task(
  config=tasks_config['resource_allocation'],
  agent=resource_allocation_agent,
  output_pydantic=ProjectPlan # This is the structured output we want
)


print ("=" * 50)

# Creating Crew
crew = Crew(
  agents=[
    project_planning_agent,
    estimation_agent,
    resource_allocation_agent
  ],
  tasks=[
    task_breakdown,
    time_resource_estimation,
    resource_allocation
  ],
  verbose=True
)

print(crew)
print ("=" * 50)

project = 'Website'
industry = 'Technology'
project_objectives = 'Create a website for a small business'
team_members = """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
"""
project_requirements = """
- Create a responsive design that works well on desktop and mobile devices
- Implement a modern, visually appealing user interface with a clean look
- Develop a user-friendly navigation system with intuitive menu structure
- Include an "About Us" page highlighting the company's history and values
- Design a "Services" page showcasing the business's offerings with descriptions
- Create a "Contact Us" page with a form and integrated map for communication
- Implement a blog section for sharing industry news and company updates
- Ensure fast loading times and optimize for search engines (SEO)
- Integrate social media links and sharing capabilities
- Include a testimonials section to showcase customer feedback and build trust
"""

# The given Python dictionary
inputs = {
  'project_type': project,
  'project_objectives': project_objectives,
  'industry': industry,
  'team_members': team_members,
  'project_requirements': project_requirements
}

print("Starting kickoff")
# Run the crew
result = crew.kickoff(
  inputs=inputs
)