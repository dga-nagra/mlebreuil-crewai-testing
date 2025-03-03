# CrewAi Review


## Introduction

[CrewAI](https://github.com/crewAIInc/crewAI) is an agentic AI framework.  
It is built on top of [LiteLLM](https://github.com/BerriAI/litellm) which is a generic wrapper for LLM APIs.


[Ollama](https://github.com/ollama/ollama) is a tool to download and run LLM locally on your machine. It can also be used as a webserver.  
The webserver is compatible with OpenAI API and that can be used through LiteLLM or a library like [ollama-python](https://github.com/ollama/ollama-python).

## Current state

Regarding the current version of the tools:
- CrewAI: 0.102.0
- LiteLLM: v1.61.20.rc
- Ollama: v0.5.12

CrewAI and Ollama have not reached their version 1.x.x at the moment.  
LiteLLM has still [many bugs pending](https://github.com/ollama/ollama/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and I personnally faced a few of them:
- https://github.com/BerriAI/litellm/issues/8594
- https://github.com/crewAIInc/crewAI/issues/1337
- https://github.com/crewAIInc/crewAI/issues/372

Hopefull, there were workarounds or upgrade/downgrading the library will remove some blocking bugs.

### Quality

If we look at CrewAI's code, there are many bad code designs. Also, many features seem redundant and/or not sufficiently scoped.  
We can look at `CrewBase` being a decorator, the pydantic models are not properly defined for class-level attributes, `Knowledge` is redundant with `Tools`, `Flow` are an alternative to `Crew` (as it is never shown how it can combine with Crews) without expliciting it and the behaviour is quite chemical (see `router` decorator example). There are also many assumption that are not maintained throughout the "documentation" (e.g. the use of the `crewai` CLI)

## Review

**Ollama** itself already gets the job done. The documentation isn't well written, but it is simple to use so the examples provided are enough. Using it directly works but we will then not be able to easily switch to another API. This is where LiteLLM comes to a handy.

**LiteLLM** will allow us to use LLM independently of the platform behind it. It can also be set up as a [proxy server, aka "LLM Gateway"](https://docs.litellm.ai/docs/simple_proxy).

At this point, there is no reason for not using LiteLLM as an intermediate.

**CrewAI** makes it easier to use agentic AI (multi-agents). We can already do it without CrewAI and the benefits of Agentic AI isn't that obvious. 


## Agentic AI

An Agentic AI may comprise a single agent or multiple agents. "Agentic" only means that the AI take a role and a purpose.
Sources:
- [What is agentic AI?](https://www.ibm.com/think/topics/agentic-ai) (See the "Examples of agentic AI" section)
- [Agency, Agentic AI and Multi-Agent Systems](https://hungdu.com/agency-agentic-ai-and-multi-agent-systems/#:~:text=An%20Agentic%20AI%20system%20may%20comprise%20a%20single,%22Agentic%20AI%22%20is%20frequently%20associated%20with%20multi-agent%20systems.)

You can search for "multi-agents vs Single Agents".

Agentic AI is specialized and has a goal. In comparison, a "Generative AI" doesn't.

### Multi-agents vs Single agent AI 

From [Multi-agent vs Single Agent (CrewAi Forum)](https://community.crewai.com/t/multi-agent-vs-single-agent/3019), we can find a good and simple reason for using multi-agent AI:
> The main issue that you may face using a single agent with multiple tools is **hallucination** – the LLM could get confused when presented with **too many tools** and may not select the right tools or not fail when necessary by hallucinating and coming up with nonsensical answer (tool to invoke or tool parameters).
> **A single agent also needs longer context** in the prompt which further increases hallucination.
> By breaking down into focused and smaller tasks, we can make LLM to **generate a more relevant answer** (for example the correct tool/parameters) for a given task. Another issue is managing complexity of the system: having a monolith agent makes it difficult to make it extensible and robust: For example if we want to change a small aspect (a prompt change for a specific scenario), it could have ripple (negative) effect on other aspects.
> 
> I do not have empirical data of my own, but suggest reading this resource I came across: Unlocking complex problem-solving with multi-agent collaboration on Amazon Bedrock | AWS Machine Learning Blog


## Conclusion

CrewAI is a framework for agentic AI that allows us to easily upgrade from single agent to multi agent when needed. It is built on top of LiteLLM which allows us to easily change the models we use.

There is no reason for not using it as we can easily use only a fraction of its features and upgrade progressively. The main downside is the lack of maturity for the tool, but we won't have many more mature tools considering the explosion of popularity of AI in the last few years.