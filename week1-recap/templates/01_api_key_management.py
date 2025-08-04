# API Key Management Templates
# Week 1 - Road to AI Agent Engineer

import os
from dotenv import load_dotenv

def load_api_key(api_key_name: str):
    """Load any API key from environment variables."""
    load_dotenv()
    api_key = os.getenv(api_key_name)
    
    if not api_key:
        raise ValueError(f"{api_key_name} not found in environment variables")
    
    return api_key

def load_openai_key():
    """Load OpenAI API key."""
    return load_api_key('OPENAI_API_KEY')

def load_huggingface_key():
    """Load Hugging Face API key."""
    return load_api_key('HUGGINGFACE_API_KEY')

def load_openrouter_key():
    """Load OpenRouter API key."""
    return load_api_key('OPENROUTER_API_KEY')

def check_api_key_exists(api_key_name: str) -> bool:
    """Check if API key exists in environment."""
    load_dotenv()
    return os.getenv(api_key_name) is not None 