# Prompt Engineering: Structured JSON Outputs

---

## 1. Introduction

In many AI applications, especially those involving APIs, databases, or downstream pipelines, it's essential that outputs from Large Language Models (LLMs) be predictable, machine-readable, and strictly structured. JSON (JavaScript Object Notation) is the standard format for this purpose.

This section explores the theory and best practices for crafting prompts that reliably return structured JSON from LLMs.

---

## 2. Prompt Design Principles

### ✅ Be Explicit
Always **clearly describe** the desired format. Don't assume the LLM understands unless you spell it out.

Example:
> "Return the result as a JSON object with the following fields: 'title' (string), 'genre' (string), 'rating' (float from 0 to 10). Do not include any explanations or formatting outside of the JSON."

### ✅ Include Schema Expectations
List all keys and expected value types in the prompt.

Example:
```json
{
  "title": "string",
  "genre": "string",
  "rating": "float (0.0 to 10.0)"
}

### ✅ Use Delimiters
Wrap your response in triple backticks to help with extraction:

Respond only with a valid JSON object wrapped in triple backticks.
Example: 
```json
{ "title": "Inception", "genre": "Sci-Fi", "rating": 9.3 }


### ✅ Keep Language Minimal
Avoid open-ended instructions like “Explain why” or “Tell me more.” Use commands like:
- “Output only”
- “Strict JSON format”
- “No extra text or comments”

---

## 3. Examples of Well-Designed Prompts

### 🎯 Basic Movie Example
> "Give me one movie recommendation in the following JSON format. Respond with only the JSON, and ensure it is valid:  
> ```json  
> {  
>   "title": "string",  
>   "genre": "string",  
>   "rating": "float from 0.0 to 10.0"  
> }  
> ```"

### 🎯 With Multiple Results
> "Return a JSON array with 3 recommended books. Each item should be an object with 'title' (string), 'author' (string), and 'year' (integer). Output only the array."

---

## 4. Parsing and Validation

After receiving the output from the LLM, you need to **parse and validate** it to ensure structural correctness.

### A. `json.loads()`
- Converts a JSON-formatted string into a Python dictionary or list.
- Example:
```python
import json

response = '{"title": "The Matrix", "genre": "Action", "rating": 8.7}'
data = json.loads(response)

### B. jsonschema Validation

- Ensures the structure matches what you expect.
- Protects downstream code from unexpected keys, data types, or missing fields.

from jsonschema import validate, ValidationError

schema = {
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "genre": { "type": "string" },
    "rating": { "type": "number", "minimum": 0, "maximum": 10 }
  },
  "required": ["title", "genre", "rating"]
}

try:
    validate(instance=data, schema=schema)
    print("Valid JSON ✅")
except ValidationError as e:
    print(f"Validation failed ❌: {e.message}")

## 5. Common Mistakes to Avoid

    ❌ Outputting JSON with natural language explanations before or after

    ❌ Incorrect data types (e.g., "rating": "8.5" as a string instead of float)

    ❌ Missing required fields

    ❌ Malformed or unescaped characters (e.g., quotes inside strings)

    ❌ Using vague instructions ("Give me info about a movie")