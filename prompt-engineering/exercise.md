# 🧠 Exercise: Structured JSON Output from LLMs

## 🎯 Objective

Design and test a prompt that instructs a Large Language Model (LLM) to return **structured JSON** data. You'll write code to interact with the LLM, parse its response, and validate the structure using `jsonschema`.

This exercise helps you solidify your understanding of prompt engineering and lays the foundation for using LLMs in production-grade applications.

---

## 🧩 Instructions

### 1. Create a Prompt
Write a prompt that asks the LLM to return a **movie recommendation** in **strict JSON format**, including the following fields:

- `title`: string  
- `genre`: string  
- `rating`: float between 0.0 and 10.0

🔸 **Constraints**:
- The output should be JSON **only**, with no explanations or extra text.
- Wrap the JSON in triple backticks to make it easier to extract (optional but recommended).

---

### 2. Interact with the LLM
Use your preferred method to call an LLM (e.g. OpenAI API, local model, or manual copy-paste from ChatGPT). Save the raw response as a string.

---

### 3. Parse the JSON Output
Use json.loads() to convert the raw string into a Python dictionary.

---

### 4. Validate the JSON Structure
Define a JSON Schema and validate the data using jsonschema.

---

### 5. Save Valid Outputs
Store valid outputs in a folder called /examples/ inside a file like valid_outputs.json.
If you want to keep a log of failed attempts or malformed JSON, create a logs/invalid.json file and append entries with error messages.


