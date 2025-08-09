# Exercise: Token Usage & Cost Monitoring Script

## Objective
Implement a Python script that:
1. Sends a prompt to an LLM.
2. Calculates the number of tokens used for both input and output.
3. Estimates the total cost based on pricing rules.
4. Logs this information in a structured CSV or JSON file.

---

## Requirements
- **LLM Provider:** OpenAI GPT-4 or GPT-3.5
- **Libraries:** `openai`, `tiktoken`, `json` or `csv`, `datetime`

---

## Steps
1. **Initialize the Script**
   - Set API key and model.
2. **Token Counting**
   - Use `tiktoken` to count tokens in the prompt.
3. **Make API Request**
   - Capture the model's response.
4. **Count Output Tokens**
   - Tokenize the completion text.
5. **Cost Calculation**
   - Use provider pricing per 1,000 tokens.
6. **Logging**
   - Save request, token counts, cost, and timestamp to a log file.

---

## Example Starter Code
```python
import openai
import tiktoken
import json
from datetime import datetime

# Config
openai.api_key = "YOUR_API_KEY"
MODEL = "gpt-4"
PRICE_INPUT = 0.03  # USD per 1K tokens
PRICE_OUTPUT = 0.06

def count_tokens(text, model=MODEL):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

prompt = "Explain quantum computing in simple terms."

# Count input tokens
input_tokens = count_tokens(prompt)

# API call
response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=200
)

output_text = response.choices[0].message["content"]
output_tokens = count_tokens(output_text)

# Cost calculation
cost = (input_tokens / 1000 * PRICE_INPUT) + (output_tokens / 1000 * PRICE_OUTPUT)

# Logging
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "model": MODEL,
    "prompt_tokens": input_tokens,
    "completion_tokens": output_tokens,
    "total_cost": round(cost, 6),
    "response": output_text
}

with open("token_usage_log.json", "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}, Cost: ${cost:.6f}")
```

---

## Expected Output

```
Input tokens: 8, Output tokens: 150, Cost: $0.0102
```

---

## Deliverable

Submit:
1. Your final Python script.
2. A sample log file with at least 3 different prompts recorded.

---

## Bonus Challenges

1. **Multi-Model Support**: Extend the script to work with different models (GPT-3.5, GPT-4, Claude).
2. **Daily Budget Tracking**: Implement a feature that tracks daily spending and alerts when approaching a budget limit.
3. **Batch Processing**: Modify the script to handle multiple prompts efficiently.
4. **Visual Dashboard**: Create a simple visualization of token usage and costs over time.
5. **Cost Optimization**: Implement automatic prompt optimization to reduce token usage while maintaining quality.

---

## Learning Outcomes

By completing this exercise, you will understand:
- How to accurately count tokens before and after API calls
- The relationship between tokens and costs for different models
- Best practices for logging and monitoring LLM usage
- How to implement budget controls in production applications
- Strategies for optimizing token usage and reducing costs
