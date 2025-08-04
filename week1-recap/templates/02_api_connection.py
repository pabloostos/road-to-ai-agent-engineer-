# API Connection Templates
# Week 1 - Road to AI Agent Engineer

import requests
import openai
from typing import Dict, Any

def setup_openai_client(api_key: str):
    """Setup OpenAI client."""
    openai.api_key = api_key
    return openai

def call_huggingface_api(api_key: str, model: str, inputs: str):
    """Call Hugging Face API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": inputs}
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('translation_text', str(result[0]))
        return str(result)
    else:
        raise Exception(f"API Error: {response.status_code}")

def call_openrouter_api(api_key: str, prompt: str, max_tokens: int = 200):
    """Call OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error: {response.status_code}") 