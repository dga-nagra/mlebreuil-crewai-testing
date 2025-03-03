# CrewAI

CrewAI is a framework that gives structure to multi-agents Agentic AI. It has many features and concepts.

## CLI

The CLI offers a few utilities. For example, it has the `crewai create ...` command to create a folder structure.

## Main Concepts
- [Agent](https://docs.crewai.com/concepts/agents): One agentic AI. It is created by combining a LLM and details about the agent's nature (Role, Goal, Backstory). You can give each agent different tools (see below what a tool is)
- [Tasks](https://docs.crewai.com/concepts/tasks): A piece of work with a result. Each task is accomplished by a single agent.
- [Crew](https://docs.crewai.com/concepts/crews): This groups together multiple agents and multiple tasks with some configurations on how the execution should be made.
- [Collaboration](https://docs.crewai.com/concepts/collaboration): 

## Main Features
The most important features are:
- [Tools](https://docs.crewai.com/concepts/tools): Allow the AI to take actions. A tool can be used to get data or to do state mutation on external systems.
-  [Knowledge](https://docs.crewai.com/concepts/knowledge): Gives more information to the AI (This can be achieved with a tool, but is more specific in its usage) 
- [Flows](https://docs.crewai.com/concepts/flows): Explicitly control how tasks communicate with each others
- [Training](https://docs.crewai.com/concepts/training): Pre-train your model to get better/faster results



## Secondary features
Less important features are:
- [Testing](https://docs.crewai.com/concepts/testing): It is mostly about testing the performance more that the results (which would be hard to test due to the non-deterministic nature of AI)
- [Planning](https://docs.crewai.com/concepts/training): An LLM is responsible for defining the tasks and assignation before starting the tasks. It is not specified what the beneficies are
- [Processes](https://docs.crewai.com/concepts/processes): How agents interacts, this is currently limited to Sequential and Hierarchical. Another one, "Consensual Process" is on the way.




## Features in depth

Here we will show the most import concepts/features with code

### Crew

A crew is literally just a groupment of tasks and agents

```python
agent = Agent(
    role="...",
    goal="...",
    backstory="...",
    # tools=[...],
)
task = Task(
    # name="...",
    description="...",
    expected_output="...",
    # agent=...,
    # tools=[...]
)
crew = Crew(
    agents=[agent],
    tasks=[task],
    ...
)
```
NOTE: Instead of passing each arguments manually, you can pass the whole config directly:
```python
agent = Agent(config={ ... }) 
```
This is useful when the configuration is defined externally (e.g. in a file)


To make the crew more re-usable, you should have a way to generate a new one on the fly.  
You could do it manually like so:

```python
def get_crew(...) -> Crew:
    agent = Agent(...)
    task = Task(...)
    return Crew(
        agents=[agent],
        tasks=[task],
        ...
    )
```
but CrewAI defined [CrewBase](https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators) to give more structure to it.

#### [CrewBase](https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators)

At this point:
- The benefits of using `CrewBase` over a function are unclear.
- `CrewBase` being a decorate causes many issues for the linter
- This binds the agents with the tasks. What if we want to re-use agents or group of agents for different groups of tasks ?


```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff


@CrewBase
class YourCrewName:
    """Description of your crew"""

    @before_kickoff
    def prepare_inputs(self, inputs):
        # Modify inputs before the crew starts
        inputs['additional_data'] = "Some extra information"
        return inputs

    @after_kickoff
    def process_output(self, output):
        # Modify output after the crew finishes
        output.raw += "\nProcessed after kickoff."
        return output

    @agent
    def agent_one(self) -> Agent:
        return Agent(...)

    @task
    def task_one(self) -> Task:
        return Task(...)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator. 
            process=Process.sequential,
            verbose=True,
        )
```

### Tools

There are many pre-existing tools, including:
- XMLSearchTool
- JSONSearchTool
- FirecrawlSearchTool / FirecrawlCrawlWebsiteTool / FirecrawlScrapeWebsiteTool


We can also [create our own tools](https://docs.crewai.com/concepts/tools#creating-your-own-tools)
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Class definition

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = "What this tool does. It's vital for effective utilization."
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, argument: str) -> str:
        # Your tool's logic here
        return "Tool's result"

# Function + Decorator

@tool("Name of my tool")
def my_tool(question: str) -> str:
    """Clear description for what this tool is useful for, your agent will need this information to use it."""
    # Function logic here
    return "Result from your custom tool"
```


#### [FLows](https://docs.crewai.com/concepts/flows )

Flows are a cosmetic way to define explicitly how we pass data between models


```python
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from litellm import completion


class ExampleFlow(Flow):
    @start()  # We can have multiple function decorated with `start`. They will start in parallel.
    def generate_city(self):
        print("Starting flow")
        # Each flow state automatically gets a unique ID
        print(f"Flow State ID: {self.state['id']}")

        response = completion(
            model=...,
            messages=[
                {
                    "role": "user",
                    "content": ...,
                },
            ],
        )

        random_city = response["choices"][0]["message"]["content"]
        # Store the city in our state
        self.state["city"] = random_city  # This is optional
        print(f"Random City: {random_city}")

        return random_city  # This is what will be passed to generate_fun_fact

    @listen(generate_city)
    def generate_fun_fact(self, random_city):  # random_city is the output of generate_city
        response = completion(
          {
              "role": "user",
              "content": f"Tell me a fun fact about {random_city}",  # We must pass the values ourselves.
          },
        )

        fun_fact = response["choices"][0]["message"]["content"]
        # Store the fun fact in our state
        self.state["fun_fact"] = fun_fact  # This is optional
        return fun_fact



flow = ExampleFlow()
result = flow.kickoff()

print(f"Generated fun fact: {result}")

```
