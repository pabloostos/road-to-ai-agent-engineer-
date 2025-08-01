# Practical Exercise: Simulating API Behavior via LLM Prompting

**Course**: Road to AI Agent Engineer  
**Unit**: Prompt Engineering for API Simulation  
**Duration**: 30–45 minutes

---

## Objective

You will design and evaluate prompts that simulate realistic API behavior from an LLM. This includes:
- Generating a mock GET response
- Producing a valid POST request payload
- Returning a structured error response

You may test your prompts using an OpenAI, Claude, or Hugging Face interface with JSON output.

---

## Exercise 1: Simulate a GET Response

### Task

Create a prompt that simulates a GET request retrieving movie data. The API should return the following fields:

- movie_id (string)  
- title (string)  
- genre (string)  
- rating (float)  
- available_on_streaming (boolean)

### Constraints
- Output must be a valid JSON object.
- Wrap the output in triple backticks if using a chat interface.
- No explanatory text — only the structured data.

---

## Exercise 2: Create a POST Payload

### Task

Design a prompt that generates a POST request payload for creating a new customer record. Required fields:

- customer_id (string)  
- name (string)  
- email (string)  
- phone (string)  
- subscribed_to_newsletter (boolean)

### Constraints
- Output should represent a request payload.
- Must be valid JSON.
- No extra explanation.

---

## Bonus Exercise: Simulate a Structured API Error

### Task

Construct a prompt that simulates a server error response when a required parameter is missing from a POST request.

Expected Output:

```json
{
  "status_code": 422,
  "error": "Missing required field: 'email'"
}
```

### Constraints

- Must include a valid HTTP status code and descriptive error message.
- Use only structured JSON in your response.
