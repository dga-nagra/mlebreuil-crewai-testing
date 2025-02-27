# Add your utilities or helper functions to this file.

from functools import cache
import os
from typing import Any
from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew, LLM
from ollama import Client

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def _get_ollama_base_url():
    return os.getenv("LLM_BASE_URL") or os.getenv("DEFAULT_LLM_BASE_URL") or None

def get_ollama_client() -> Client:
    base_url = _get_ollama_base_url()
    return Client(host=base_url)


def _get_available_llms() -> list[str]:
    ollama_client = get_ollama_client()
    models_data: dict[str, Any] = {
        m.model: m
        for m in ollama_client.list().models 
        if m.model
    }
    models: list[str] = list(models_data)
    return models

# https://docs.crewai.com/concepts/llms#ollama-local-llms
def get_default_model() -> str:
    model = os.getenv("DEFAULT_LLM_MODEL")
    available_models = _get_available_llms()
    print("_get_default_llm_name")
    print(model)
    print(available_models)
    if not model or model not in available_models:
        model = available_models[0]
    return model 

def get_default_llm():
    provider = "ollama"
    model_name = get_default_model()
    base_url = _get_ollama_base_url()
    print(model_name, base_url)
    return LLM(model=f"{provider}/{model_name}", base_url=base_url)

