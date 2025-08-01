# 🎓 Road to AI Agent Engineer  
## Lecture 3: Prompt Engineering for API Simulation  
⏱ Duration: 30 minutes — Professor-level Intensive  
🧠 Goal: Learn to design LLM prompts that simulate API calling behavior and produce integration-ready responses.

A practical masterclass in using prompts to simulate HTTP requests and responses with accuracy, structure, and reliability — essential for building AI agents that communicate with external systems.

---

## 📋 Table of Contents
1. Why This Topic Matters  
2. What Is API Simulation via Prompting?  
3. Design Structure for API-like Prompts  
4. Prompt Patterns for HTTP Methods  
5. Best Practices for Integration-Ready Responses  
6. Real-World Examples: GET & POST  
7. Final Hands-On Exercise  
8. Reflection  

---

## 🧭 Why This Topic Matters

AI agents increasingly need to **interface with APIs** — fetching data, triggering workflows, or simulating backend logic. While LLMs can't natively execute API calls, they **can generate valid, mock API responses** that match production specifications.

When done right, this technique is a cornerstone for:

- **Mocking APIs** for demos, testing, and front-end development  
- **Prototyping AI assistants** that imitate live system behavior  
- **Training users and developers** in realistic scenarios  
- **Generating structured data** ready for programmatic parsing  

---

## 📚 Part 1: What Is API Simulation via Prompting?

**API Simulation** means using prompts to guide the LLM to output valid, structured representations of an API's request or response — including headers, endpoints, methods, status codes, and payloads.

🧾 Think of it as:  
> "Instructing the LLM to act like a live server responding to HTTP requests."

It's prompt-based interface design.

---

## 🧱 Part 2: Design Structure for API Prompts

When designing prompts that simulate API behavior, the following structure is key:

| Component        | Purpose                                      | Example                              |
|------------------|----------------------------------------------|--------------------------------------|
| **Role Definition** | Set identity of the LLM                     | "You are a RESTful API simulator."   |
| **Behavioral Scope** | Limit to valid HTTP specs                  | "Only output HTTP-like responses."   |
| **Format Requirement** | Define response format (Markdown, JSON, etc.) | "Wrap response in code blocks."      |
| **Call Details**   | Include endpoint, method, parameters         | "POST to /login with body {...}"     |
| **Status Feedback**| Provide status codes, messages               | "Respond with 200 OK or 401 Unauthorized." |

🔧 Example Prompt Skeleton:

You are a REST API simulator.
Respond using valid HTTP formatting. Include:

    Method

    URL

    Headers

    Status code and message

    JSON body (if applicable)

Wrap your full response in triple backticks using http or json.


---

## 🔀 Part 3: Prompt Patterns for HTTP Methods

### 📥 GET Request Simulation

Used to **retrieve resources**. Simulated outputs include status, headers, and data body.

🧪 Prompt:

> "Simulate a GET request to `/users/42`. Return user details if found."

🧾 Output:

```http
GET /users/42 HTTP/1.1  
Host: api.example.com  
Authorization: Bearer {token}

HTTP/1.1 200 OK  
Content-Type: application/json  

{
  "id": 42,
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

### 📨 POST Request Simulation

Used to submit new data. Prompts should include body content and expect response codes like 201 Created or 400 Bad Request.

🧪 Prompt:

> "Simulate a POST request to /register with user payload. Return 201 on success."

🧾 Output:

```http
POST /register HTTP/1.1  
Host: api.example.com  
Content-Type: application/json  

{
  "username": "jane_doe",
  "email": "jane@example.com",
  "password": "securepassword123"
}

HTTP/1.1 201 Created  
Content-Type: application/json  

{
  "message": "User created successfully",
  "user_id": 101
}
```

---

## 🧠 Part 4: Best Practices for Integration-Ready API Prompts

📌 Use These Prompt Engineering Techniques:

| Technique | Description |
|-----------|-------------|
| Explicit Role | Define the model as an API engine or server |
| Structural Clarity | Demand exact formats: headers, JSON, status |
| Method Simulation | Ask for GET, POST, PUT, DELETE structure explicitly |
| Status Control | Define expected codes (e.g. 200, 404, 500) |
| Context Sensitivity | Link input to valid output (e.g., invalid payloads) |
| Block Wrapping | Use http or json consistently |

---

## 📦 Part 5: Real-World Examples

### Example 1 — GET: Weather Data

**Prompt:**

> "Simulate a GET request to /weather?city=Madrid&unit=celsius. Return weather data."

**Output:**

```http
GET /weather?city=Madrid&unit=celsius HTTP/1.1  
Host: weatherapi.ai  

HTTP/1.1 200 OK  
Content-Type: application/json  

{
  "city": "Madrid",
  "temperature": 29,
  "unit": "celsius",
  "condition": "sunny"
}
```

### Example 2 — POST: Login Error

**Prompt:**

> "Simulate a POST request to /login with wrong credentials. Return error."

**Output:**

```http
POST /login HTTP/1.1  
Host: authserver.ai  
Content-Type: application/json  

{
  "email": "wrong@user.com",
  "password": "wrongpass"
}

HTTP/1.1 401 Unauthorized  
Content-Type: application/json  

{
  "error": "Invalid email or password"
}
```

---

## 🛠 Part 6: Hands-On Exercise

🎯 **Scenario**: You are building a front-end for a food delivery app. You need to simulate a POST request to /orders with the user's cart. Your goal is to generate a prompt that will produce:

- HTTP POST structure
- JSON body with food items, total, and delivery address
- 201 response with an order ID

🔧 **Try designing this prompt:**

> "You are an API simulator. Respond with a full HTTP POST interaction to the `/orders` endpoint.  
> Include a realistic food cart payload in the request body.  
> Return a 201 Created response with an order confirmation object.  
> Wrap everything in triple backticks with `http` format."

**Expected Output:**

```http
POST /orders HTTP/1.1  
Host: fooddelivery.ai  
Content-Type: application/json  

{
  "user_id": 150,
  "items": [
    { "name": "Margherita Pizza", "qty": 1, "price": 9.99 },
    { "name": "Garlic Bread", "qty": 2, "price": 3.50 }
  ],
  "total": 16.99,
  "address": "Calle Mayor 25, Madrid"
}

HTTP/1.1 201 Created  
Content-Type: application/json  

{
  "order_id": "FDX123456",
  "status": "confirmed",
  "estimated_delivery": "30 minutes"
}
```

---

## 🧩 Final Reflection

Prompt engineering for API simulation unlocks a crucial use case in agent-based workflows: enabling structured, reliable, and testable mock interactions. This bridges the gap between natural language reasoning and systems design.

## 🎯 Key Takeaways

- Prompts can simulate API calls with remarkable accuracy
- Format control (status, headers, JSON) is essential
- Role definition (API simulator, HTTP responder) shapes behavior
- GET, POST, and error handling patterns follow real-world logic
- Useful for mock UIs, tests, agent pipelines, or training data

🧠 **Remember**: You're not just prompting text.  
You're engineering protocol-aware agents that speak in the language of systems.
