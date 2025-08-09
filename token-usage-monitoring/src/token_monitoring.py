#!/usr/bin/env python3
"""
Token Usage & Cost Monitoring Script

This script implements the exercise requirements:
1. Sends a prompt to an LLM via OpenRouter
2. Calculates tokens used for input and output
3. Estimates total cost based on pricing rules
4. Logs information in structured JSON file

Requirements fulfilled:
- OpenRouter API integration
- Token counting with tiktoken
- Cost calculation
- JSON logging with timestamps
- Sample with multiple prompts for deliverable
"""

import requests
import tiktoken
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Pricing - OpenRouter GPT-3.5-turbo pricing (check their pricing page for current rates)
PRICE_INPUT = 0.0015   # $0.0015 per 1K input tokens
PRICE_OUTPUT = 0.002   # $0.002 per 1K output tokens

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Count tokens using tiktoken for OpenAI-compatible models.
    
    Args:
        text (str): Text to count tokens for
        model (str): Model name for tokenizer selection
        
    Returns:
        int: Number of tokens
    """
    try:
        # Use the base model name for tiktoken (remove provider prefix)
        base_model = model.split('/')[-1] if '/' in model else model
        enc = tiktoken.encoding_for_model(base_model)
        return len(enc.encode(text))
    except:
        # Fallback estimation if model not supported by tiktoken
        return int(len(text.split()) * 1.3)  # Rough estimation

def call_openrouter_api(prompt, model=MODEL, max_tokens=200):
    """
    Make API call to OpenRouter.
    
    Args:
        prompt (str): The prompt to send
        model (str): Model to use
        max_tokens (int): Maximum tokens for response
        
    Returns:
        dict: API response
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def calculate_cost(input_tokens, output_tokens):
    """
    Calculate total cost based on token usage.
    
    Args:
        input_tokens (int): Number of input tokens
        output_tokens (int): Number of output tokens
        
    Returns:
        float: Total cost in USD
    """
    input_cost = (input_tokens / 1000) * PRICE_INPUT
    output_cost = (output_tokens / 1000) * PRICE_OUTPUT
    return input_cost + output_cost

def log_to_json(log_entry, filename="token_usage_log.json"):
    """
    Log entry to JSON file (append mode).
    
    Args:
        log_entry (dict): Log data to write
        filename (str): Log file name
    """
    with open(filename, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def process_prompt(prompt, model=MODEL, max_tokens=200):
    """
    Process a single prompt through the complete pipeline:
    1. Count input tokens
    2. Make API call
    3. Count output tokens
    4. Calculate cost
    5. Log everything
    
    Args:
        prompt (str): The prompt to process
        model (str): Model to use
        max_tokens (int): Maximum tokens for response
        
    Returns:
        dict: Processing results
    """
    print(f"\n📝 Processing prompt: {prompt}")
    print("-" * 50)
    
    # Step 1: Count input tokens
    input_tokens = count_tokens(prompt)
    print(f"🔢 Input tokens: {input_tokens}")
    
    # Step 2: Make API call
    print(f"🚀 Making API call to {model}...")
    try:
        response = call_openrouter_api(prompt, model, max_tokens)
        
        if 'choices' not in response:
            print(f"❌ API Error: {response}")
            return None
            
        output_text = response['choices'][0]['message']['content']
        print(f"✅ Response received: {len(output_text)} characters")
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return None
    
    # Step 3: Count output tokens
    output_tokens = count_tokens(output_text)
    print(f"🔢 Output tokens: {output_tokens}")
    
    # Step 4: Calculate cost
    cost = calculate_cost(input_tokens, output_tokens)
    print(f"💰 Total cost: ${cost:.6f}")
    
    # Step 5: Create log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt": prompt,
        "prompt_tokens": input_tokens,
        "completion_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "total_cost": round(cost, 6),
        "response": output_text
    }
    
    # Step 6: Log to JSON file
    log_to_json(log_entry)
    print(f"📋 Logged to token_usage_log.json")
    
    # Display summary
    print(f"\n📊 Summary:")
    print(f"   Input tokens: {input_tokens}")
    print(f"   Output tokens: {output_tokens}")
    print(f"   Total tokens: {input_tokens + output_tokens}")
    print(f"   Cost: ${cost:.6f}")
    
    return log_entry

def main():
    """
    Main function - processes multiple prompts to create sample log file
    as required for the deliverable.
    """
    print("🎯 Token Usage & Cost Monitoring Script")
    print("=" * 50)
    
    # Check API key
    if not OPENROUTER_API_KEY:
        print("❌ Error: OPENROUTER_API_KEY not found in environment")
        print("Please set it in your .env file")
        return
    
    print(f"✅ Using model: {MODEL}")
    print(f"💰 Pricing: ${PRICE_INPUT}/1K input, ${PRICE_OUTPUT}/1K output tokens")
    
    # Sample prompts for deliverable (minimum 3 different prompts)
    test_prompts = [
        "Explain quantum computing in simple terms.",
        "Write a haiku about artificial intelligence.",
        "What are the benefits of renewable energy?",
        "How does machine learning work?"
    ]
    
    results = []
    total_cost = 0
    
    # Process each prompt
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔄 Processing prompt {i}/{len(test_prompts)}")
        
        result = process_prompt(prompt)
        
        if result:
            results.append(result)
            total_cost += result['total_cost']
        else:
            print(f"⚠️  Skipping prompt {i} due to error")
    
    # Final summary
    print(f"\n🎉 Processing Complete!")
    print(f"=" * 50)
    print(f"📋 Prompts processed: {len(results)}")
    print(f"💰 Total cost: ${total_cost:.6f}")
    print(f"📄 Log file: token_usage_log.json")
    
    if results:
        avg_cost = total_cost / len(results)
        total_tokens = sum(r['total_tokens'] for r in results)
        avg_tokens = total_tokens / len(results)
        
        print(f"📊 Averages:")
        print(f"   Cost per prompt: ${avg_cost:.6f}")
        print(f"   Tokens per prompt: {avg_tokens:.1f}")
        print(f"   Cost per token: ${total_cost/total_tokens:.8f}")
    
    print(f"\n📂 Check 'token_usage_log.json' for detailed logs")

if __name__ == "__main__":
    main()
