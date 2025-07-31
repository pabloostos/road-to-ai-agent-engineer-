# Prompt Engineering: Structured JSON Outputs

A comprehensive guide to designing prompts that generate reliable, structured JSON data from Large Language Models (LLMs).

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [Prompt Design Principles](#2-prompt-design-principles)
3. [Examples of Well-Designed Prompts](#3-examples-of-well-designed-prompts)
4. [Parsing and Validation](#4-parsing-and-validation)
5. [Common Mistakes to Avoid](#5-common-mistakes-to-avoid)
6. [Best Practices Summary](#6-best-practices-summary)
7. [Production Considerations](#7-production-considerations)

---

## 1. Introduction

In many AI applications, especially those involving APIs, databases, or downstream pipelines, it's essential that outputs from Large Language Models (LLMs) be **predictable**, **machine-readable**, and **strictly structured**. JSON (JavaScript Object Notation) is the standard format for this purpose.

This guide explores the theory and best practices for crafting prompts that reliably return structured JSON from LLMs.

### 🎯 Why Structured JSON Matters

- **API Integration**: Easy integration with existing systems
- **Data Processing**: Consistent format for downstream analysis
- **Error Handling**: Predictable structure enables robust validation
- **Scalability**: Standard format works across different platforms

---

## 2. Prompt Design Principles

### ✅ Principle 1: Be Explicit

Always **clearly describe** the desired format. Don't assume the LLM understands unless you spell it out.

**❌ Bad Example:**
```
Tell me about a movie
```

**✅ Good Example:**
```
Return the result as a JSON object with the following fields: 
- 'title' (string): movie title
- 'genre' (string): movie genre  
- 'rating' (float from 0 to 10): movie rating

Do not include any explanations or formatting outside of the JSON.
```

### ✅ Principle 2: Include Schema Expectations

List all keys and expected value types in the prompt.

**✅ Example:**
```json
{
  "title": "string",
  "genre": "string", 
  "rating": "float (0.0 to 10.0)"
}
```

### ✅ Principle 3: Use Delimiters

Wrap your response in triple backticks to help with extraction.

**✅ Example:**
```
Respond only with a valid JSON object wrapped in triple backticks.

Example: 
{ "title": "Inception", "genre": "Sci-Fi", "rating": 9.3 }
```

### ✅ Principle 4: Keep Language Minimal

Avoid open-ended instructions like "Explain why" or "Tell me more." Use direct commands:

- ✅ "Output only"
- ✅ "Strict JSON format"
- ✅ "No extra text or comments"
- ❌ "Tell me more about this"
- ❌ "Explain your reasoning"

---

## 3. Examples of Well-Designed Prompts

### 🎯 Example 1: Basic Movie Recommendation

**Prompt:**
```
Give me one movie recommendation in the following JSON format. 
Respond with only the JSON, and ensure it is valid:

{
  "title": "string",
  "genre": "string",  
  "rating": "float from 0.0 to 10.0"
}
```

**Expected Output:**
```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "rating": 8.8
}
```

### 🎯 Example 2: Multiple Results

**Prompt:**
```
Return a JSON array with 3 recommended books. Each item should be an object with:
- 'title' (string): book title
- 'author' (string): author name  
- 'year' (integer): publication year

Output only the array.
```

**Expected Output:**
```json
[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925
  },
  {
    "title": "1984",
    "author": "George Orwell", 
    "year": 1949
  },
  {
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "year": 1960
  }
]
```

---

## 4. Parsing and Validation

After receiving the output from the LLM, you need to **parse and validate** it to ensure structural correctness.

### A. Using `json.loads()`

Converts a JSON-formatted string into a Python dictionary or list.

**Example:**
```python
import json

# Raw response from LLM
response = '{"title": "The Matrix", "genre": "Action", "rating": 8.7}'

# Parse into Python dictionary
data = json.loads(response)
print(data)  # {'title': 'The Matrix', 'genre': 'Action', 'rating': 8.7}

# Access individual fields
print(f"Movie: {data['title']}")
print(f"Genre: {data['genre']}")
print(f"Rating: {data['rating']}")
```

### B. Using jsonschema Validation

Ensures the structure matches what you expect. Protects downstream code from unexpected keys, data types, or missing fields.

**Example:**
```python
from jsonschema import validate, ValidationError

# Define the expected schema
schema = {
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "genre": { "type": "string" },
    "rating": { 
      "type": "number", 
      "minimum": 0, 
      "maximum": 10 
    }
  },
  "required": ["title", "genre", "rating"],
  "additionalProperties": False
}

# Validate the data
try:
    validate(instance=data, schema=schema)
    print("✅ Valid JSON - Structure matches schema")
except ValidationError as e:
    print(f"❌ Validation failed: {e.message}")
    print(f"Path: {e.path}")
```

---

## 5. Common Mistakes to Avoid

### ❌ Mistake 1: Natural Language with JSON

**❌ Bad Example:**
The LLM responds with natural language mixed with JSON:
```
Here's a movie recommendation for you:
{
  "title": "Inception",
  "genre": "Sci-Fi", 
  "rating": 8.8
}
I hope you like this movie!
```

**✅ Good Example:**
```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "rating": 8.8
}
```

### ❌ Mistake 2: Incorrect Data Types

**❌ Bad Example:**
The rating is returned as a string instead of a number:
```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "rating": "8.8"  // String instead of number
}
```

**✅ Good Example:**
```json
{
  "title": "Inception", 
  "genre": "Sci-Fi",
  "rating": 8.8  // Number
}
```

### ❌ Mistake 3: Missing Required Fields

**❌ Bad Example:**
The response is missing the required "genre" field:
```json
{
  "title": "Inception",
  "rating": 8.8
  // Missing "genre" field
}
```

**✅ Good Example:**
```json
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "rating": 8.8
}
```

### ❌ Mistake 4: Malformed Characters

**❌ Bad Example:**
The title contains unescaped quotes:
```json
{
  "title": "The "Matrix"",  // Unescaped quotes
  "genre": "Sci-Fi",
  "rating": 8.7
}
```

**✅ Good Example:**
```json
{
  "title": "The Matrix",  // Clean string
  "genre": "Sci-Fi", 
  "rating": 8.7
}
```

### ❌ Mistake 5: Vague Instructions

**❌ Bad Example:**
```
Give me info about a movie
```

**✅ Good Example:**
```
Return a JSON object with movie details including title, genre, and rating.
```

---

## 6. Best Practices Summary

### 📋 Core Principles

1. **Be explicit** about the exact JSON structure you want
2. **Include schema** with data types and constraints
3. **Use delimiters** (triple backticks) for easier extraction
4. **Keep language minimal** and direct
5. **Validate responses** using `jsonschema`
6. **Handle errors gracefully** with proper error messages
7. **Test your prompts** with different scenarios
8. **Document your schema** for team collaboration

### 🔧 Implementation Checklist

- [ ] Define clear schema requirements
- [ ] Use explicit data type specifications
- [ ] Include validation constraints
- [ ] Add error handling for malformed JSON
- [ ] Test with edge cases
- [ ] Document the expected format
- [ ] Set up monitoring for validation failures

---

## 7. Production Considerations

### 🚀 Scalability

- **Rate limiting**: Handle API quotas and retries
- **Caching**: Store validated responses for reuse
- **Batch processing**: Handle multiple requests efficiently
- **Performance monitoring**: Track response times and success rates

### 🛡️ Security & Safety

- **Input validation**: Sanitize user inputs before sending to LLM
- **Output validation**: Verify all responses match expected schema
- **Error logging**: Track failed attempts for debugging
- **Content filtering**: Ensure outputs meet safety guidelines

### 📊 Data Management

- **Data persistence**: Save valid outputs for analysis
- **Schema evolution**: Plan for future field additions
- **Version control**: Track schema changes over time
- **Backup strategies**: Protect against data loss

### 🔍 Monitoring & Analytics

- **Success rates**: Track validation success/failure rates
- **Response quality**: Monitor for consistent output quality
- **User feedback**: Collect feedback on output usefulness
- **Performance metrics**: Track API response times and costs

---

## 🎯 Key Takeaways

1. **Structure is everything** - Clear, explicit prompts produce better results
2. **Validation is crucial** - Always validate LLM outputs before using them
3. **Testing is essential** - Test your prompts with various scenarios
4. **Documentation matters** - Clear documentation helps team collaboration
5. **Iteration is key** - Continuously improve based on results

---

*This guide provides the foundation for building reliable, production-ready systems that generate structured JSON from Large Language Models.*