# Prompt Engineering: Structured JSON Outputs

A comprehensive exercise for learning how to extract structured JSON data from Large Language Models (LLMs) using prompt engineering techniques.

## 🎯 Overview

This project demonstrates the complete workflow for:
- Designing prompts that generate structured JSON
- Connecting to OpenAI API
- Parsing and validating JSON responses
- Saving valid outputs and logging errors

## 📁 Project Structure

```
prompt-engineering/
├── src/
│   └── recommender.py          # Main implementation
├── examples/
│   └── valid_outputs.json      # Valid movie recommendations
├── logs/
│   └── invalid.json            # Failed validation attempts
├── theory.md                   # Prompt engineering theory
├── exercise.md                 # Exercise instructions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
└── .gitignore                 # Git ignore rules
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd prompt-engineering

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 2. Configure API Key

Edit `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. Run the Exercise

```bash
python src/recommender.py
```

## 📚 Exercise Components

### Exercise 1: Create a Prompt
Design prompts that generate structured JSON with specific fields:
- `title`: string
- `genre`: string  
- `rating`: float (0.0 to 10.0)

### Exercise 2: Interact with LLM
Connect to OpenAI API and generate responses using the designed prompts.

### Exercise 3: Parse JSON Output
Use `json.loads()` to convert raw responses into Python dictionaries.

### Exercise 4: Validate JSON Structure
Define JSON schemas and validate data using `jsonschema`.

### Exercise 5: Save Valid Outputs
Store valid outputs in `/examples/` and log invalid attempts in `/logs/`.

## 🔧 Key Features

- **Secure API Key Management**: Uses `.env` files with `.gitignore`
- **Comprehensive Validation**: JSON schema validation with detailed error messages
- **Data Persistence**: Saves valid outputs and logs errors
- **Error Handling**: Graceful handling of API errors and malformed JSON
- **Clean Code**: Professional, well-documented implementation

## 📖 Theory

See `theory.md` for comprehensive coverage of:
- Prompt design principles
- JSON parsing techniques
- Schema validation best practices
- Common mistakes to avoid

## 🛠️ Dependencies

- `openai>=1.0.0` - OpenAI API client
- `jsonschema>=4.0.0` - JSON schema validation
- `python-dotenv>=1.0.0` - Environment variable management

## 📊 Example Output

### Valid Movie Recommendation
```json
{
  "timestamp": "2025-07-28T21:52:56.036612",
  "data": {
    "title": "The Matrix",
    "genre": "Sci-Fi",
    "rating": 8.7
  }
}
```

### Invalid Attempt Log
```json
{
  "timestamp": "2025-07-28T21:53:29.178302",
  "raw_response": "```json\n{\n  \"title\": \"The Matrix\",\n  \"rating\": 15.0\n}\n```",
  "error": "Validation failed - data does not match schema requirements"
}
```

## 🎓 Learning Outcomes

After completing this exercise, you'll understand:
- How to design prompts for structured output
- Best practices for JSON parsing and validation
- Production-ready error handling and logging
- Secure API key management
- Complete workflow from prompt to validated data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🔗 Related Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [JSON Schema Specification](https://json-schema.org/)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
