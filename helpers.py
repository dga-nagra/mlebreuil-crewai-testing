# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew, LLM


# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key



def _get_default_llm_name():
    return os.getenv("DEFAULT_LLM_MODEL", "ollama/llama3.2")

def _get_llm_base_url():
    return os.getenv("LLM_BASE_URL") or os.getenv("DEFAULT_LLM_BASE_URL") or None

def get_default_llm():
    model_name = _get_default_llm_name()
    base_url = _get_llm_base_url()
    print(model_name, base_url)
    return LLM(model=model_name, base_url=base_url)


DEFAULT_LLM = get_default_llm()
