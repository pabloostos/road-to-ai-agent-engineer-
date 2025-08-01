# 🎓 Road to AI Agent Engineer

## Lecture 4: Function Calling & JSON Schema

⏱ Duration: 45 minutes — Professor-level Intensive

🧠 Goal: Master the mechanics of structured function calling and JSON Schema validation to enable LLMs to interact with tools, APIs, and data pipelines with precision and reliability.

A deep dive into how modern language models use structured function calls and JSON Schema to interact with tools, APIs, and data pipelines.

---

## 📋 Table of Contents

1. [Why This Topic Matters](#why-this-topic-matters)
2. [What Is Function Calling in LLMs?](#what-is-function-calling-in-llms)
3. [The Role of JSON Schema](#the-role-of-json-schema)
4. [Anatomy of a Function Call](#anatomy-of-a-function-call)
5. [Design Principles & Best Practices](#design-principles--best-practices)
6. [Real-World Use Cases](#real-world-use-cases)
7. [Hands-On Exercise: Simulate a Function Call](#hands-on-exercise-simulate-a-function-call)
8. [Final Reflection](#final-reflection)

---

## 🧭 Why This Topic Matters

As we move from static chatbots to dynamic AI agents, one capability becomes central: the ability for LLMs to execute structured actions like calling APIs, triggering tools, or generating structured responses.

Function calling allows an LLM to stop generating plain text and instead output well-formed data that matches a schema — enabling it to:

- **Trigger real-world tools**
- **Query databases**
- **Integrate with APIs**
- **Power autonomous agents**

Understanding this mechanism is critical to building trustworthy, reliable AI systems that can interface with software environments.

---

## 📚 Part 1: What Is Function Calling in LLMs?

**Function Calling** is a mechanism introduced in modern LLM APIs (like OpenAI's functions or tool_call) that allows the model to output a structured invocation of a function rather than plain text.

### Instead of saying:

> "The weather in Madrid is 32°C."

### It says:

```json
{
  "name": "getWeather",
  "arguments": {
    "location": "Madrid",
    "units": "metric"
  }
}
```

This output can be passed to an actual backend function, API, or system that performs the task.

### 🛠️ Core Mechanics

1. **Step 1**: You define a list of available functions the LLM can "call," with their names, descriptions, and parameters.
2. **Step 2**: The LLM chooses a function and produces structured arguments.
3. **Step 3**: Your code executes the actual function, then feeds the result back to the LLM.

---

## 📏 Part 2: The Role of JSON Schema

Every function definition uses **JSON Schema** to define the shape, types, and constraints of its parameters. JSON Schema is like a contract that ensures data integrity between the LLM and external systems.

### 🎨 Basic Example

**Function:**

```json
{
  "name": "bookFlight",
  "description": "Books a flight for a user",
  "parameters": {
    "type": "object",
    "properties": {
      "origin": { "type": "string" },
      "destination": { "type": "string" },
      "date": { "type": "string", "format": "date" }
    },
    "required": ["origin", "destination", "date"]
  }
}
```

**This schema:**

- Forces the LLM to produce correct fields
- Ensures type-checking (e.g., no integer instead of a string)
- Enables validation before function execution

---

## 🧱 Part 3: Anatomy of a Function Call

| Component | Description |
|-----------|-------------|
| **name** | Name of the function/tool |
| **description** | Explains what the function does |
| **parameters** | JSON Schema object describing expected inputs |
| **arguments** | Actual values passed when calling the function |

---

## ✅ Part 4: Best Practices for Function Calling

| Best Practice | Why It Matters |
|---------------|----------------|
| Use clear, consistent naming | Improves readability and mapping to real functions |
| Enforce required parameters | Prevents incomplete invocations |
| Use enum for predefined options | Constrains possible values for better control |
| Add format hints (e.g., date) | Guides LLM to produce valid syntax |
| Test with invalid inputs | Ensure your schema handles edge cases robustly |

---

## 🌍 Part 5: Real-World Use Cases

### 1. Weather Agent

- **Function**: `getWeather(location)`
- **JSON Schema** validates city name
- **Output** triggers API call to OpenWeather

### 2. Calendar Scheduling

- **Function**: `createEvent(title, date, time)`
- **LLM** generates function call, calendar API creates event

### 3. Travel Booking Bot

- **Function**: `searchHotels(city, checkin, nights)`
- **Results** dynamically fetched and rendered

### 4. Internal Tool Automation

- **LLM** generates `runAnalysis(dataset, model_type)`
- **Used** in enterprise AI pipelines or AutoML agents

---

## 🧪 Part 6: Hands-On Exercise

### 🎯 Objective

Write a JSON Schema and simulate a function call for a movie recommendation tool.

### Step 1: Define the Function

Create a function `recommendMovie` with the following parameters:

- `genre` (string, required)
- `min_rating` (number, optional)
- `year_range` (object with start and end, optional)

### Step 2: JSON Schema

Write a JSON Schema for that function.

### Step 3: Prompt the LLM to Simulate a Call

Provide the following input:

> "I want a comedy from the 2000s with at least 7.5 stars."

**Expected function call output:**

```json
{
  "name": "recommendMovie",
  "arguments": {
    "genre": "comedy",
    "min_rating": 7.5,
    "year_range": {
      "start": 2000,
      "end": 2009
    }
  }
}
```

---

## 🧩 Final Reflection

Function calling and JSON Schema mark a new phase in LLM development — one where language meets action.

You are no longer working with just language generation — you're designing a cooperative interface between intelligent reasoning and programmatic execution.

---

## 🚀 In Your Road to AI Agent Engineering

You will use this technique to:

- **Integrate LLMs with APIs and tools**
- **Design multi-step workflows** (via chaining or agents)
- **Enable AI copilots** to manipulate data or trigger backend logic
- **Ensure safety** through schema validation
- **Build dynamic, reliable autonomous systems**

---

## 🎯 Key Takeaways

- **Function Calling = Structured Output**: Allows LLMs to return data instead of natural language
- **JSON Schema = Contract**: Ensures function inputs are valid and safe
- **Design Matters**: Naming, types, and constraints all affect LLM behavior
- **Prompt Engineering Still Applies**: Role and instructions influence function selection
- **Validation is Critical**: Always validate inputs before execution
- **Error Handling**: Plan for function failures and invalid inputs 