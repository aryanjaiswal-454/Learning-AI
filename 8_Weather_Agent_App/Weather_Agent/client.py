import os
import json
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Provider:
    """One provider described as pure data"""
    
    name: str
    """Name of the provider"""
    env_var: str
    """Environment variable name for the provider's API key"""
    is_free: bool
    """Whether the provider is free or not"""
    base_url: str|None
    """Base URL for the provider's API"""
    model: str|None
    """Model name for the provider's API"""
    
    
PROVIDERS=[
    Provider(
        name="Groq",
        env_var="GROQ_API_KEY",
        is_free=False,
        base_url="https://api.groq.com/",
        model="openai/gpt-oss-120b"  
    ),
    # can i use one more geoq provider -> answer: yes, you can add another provider by creating a new instance of the Provider class and adding it to the PROVIDERS dictionary. For example:
    Provider(
        name="Groq2",
        env_var="GROQ2_API_KEY",
        is_free=False,
        base_url="https://api.groq.com/",
        model="openai/gpt-oss-20b"  
    ) 
]

def select_provider()->Provider:
    for provider in PROVIDERS:
        if os.environ.get(provider.env_var): # check if the environment variable for the provider's API key is set
            return provider
        
        expected = ", ".join(provider.env_var for provider in PROVIDERS)
        raise RuntimeError(f"No provider key set. Please set one of the following environment variables: {expected}")
    
def get_client_and_model():
    provider = select_provider()
    api_key = os.environ[provider.env_var]
    if provider.base_url is None:
        client = Groq(api_key=api_key)
    else:
        client = Groq(api_key=api_key, base_url=provider.base_url)
        
    return client, provider.model, provider