# Practical Exercise: Function Calling and JSON Schema

**Course**: Road to AI Agent Engineer  
**Unit**: Function Calling and JSON Schema  
**Duration**: 45–60 minutes

---

## Objective

You will implement function calling patterns and JSON schema validation to create reliable AI agent interactions. This includes:
- Defining function schemas
- Implementing parameter validation
- Creating JSON schema validators
- Building error handling systems

You may test your implementations using Hugging Face Inference API.

---

## Exercise 1: Basic Function Calling

### Task

Create a simple function calling system that can handle a weather API function. Implement:

1. **Function Schema Definition**: Define a weather function with location and units parameters
2. **Parameter Validation**: Validate input parameters using JSON schema
3. **Function Execution**: Simulate weather API call
4. **Response Handling**: Return structured weather data

### Requirements

- Function name: `get_weather`
- Parameters: `location` (string, required), `units` (string, optional, enum: ["celsius", "fahrenheit"])
- Response: Temperature, condition, humidity
- Error handling for invalid parameters

### Constraints
- Use JSON schema for parameter validation
- Implement proper error messages
- Return structured JSON response
- Handle missing optional parameters

---

## Exercise 2: JSON Schema Validation

### Task

Build a comprehensive JSON schema validation system for user registration data.

### Requirements

Create schemas for:
- **User Registration**: name, email, age, password
- **Address Information**: street, city, country, postal_code
- **Preferences**: newsletter_subscription, theme, language

### Validation Rules

- Email format validation
- Age range (18-120)
- Password strength (minimum 8 characters, at least one number)
- Required vs optional fields
- Nested object validation

### Constraints
- Implement custom validation functions
- Provide detailed error messages
- Handle multiple validation scenarios
- Test with valid and invalid data

---

## Exercise 3: Advanced Function Patterns

### Task

Implement a multi-function system with conditional execution and chaining.

### Requirements

Create three functions:
1. **User Lookup**: Find user by email
2. **Order History**: Get user's order history
3. **Recommendation Engine**: Generate product recommendations

### Function Chaining

- Chain: User Lookup → Order History → Recommendations
- Conditional execution based on user existence
- Error handling for missing users
- Batch processing capabilities

### Advanced Features

- Function dependency management
- Retry mechanisms for failed calls
- Response caching
- Performance monitoring

### Constraints
- Implement proper error propagation
- Handle partial failures gracefully
- Optimize for performance
- Provide detailed logging

---

## Bonus Exercise: Schema Evolution

### Task

Design a schema versioning system that can handle schema changes over time.

### Requirements

- Version-aware schema validation
- Backward compatibility
- Migration strategies
- Schema documentation

### Constraints
- Support multiple schema versions
- Automatic schema detection
- Migration validation
- Comprehensive testing 