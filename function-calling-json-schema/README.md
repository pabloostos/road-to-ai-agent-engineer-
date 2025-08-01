# Function Calling and JSON Schema

## Overview

This module covers Function Calling and JSON Schema techniques for AI Agent Engineering. Learn how to design structured function calls and validate responses using JSON schemas.

## Learning Objectives

- Understand function calling patterns in LLMs
- Design JSON schemas for structured responses
- Implement function validation and error handling
- Create reusable function calling templates
- Master schema-based response validation

## Project Structure

```
function-calling-json-schema/
├── README.md              # This file
├── theory.md              # Theoretical concepts and best practices
├── exercise.md            # Practical exercises and tasks
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── src/                  # Source code
│   ├── exercise_1.py     # Basic function calling
│   ├── exercise_2.py     # JSON schema validation
│   └── exercise_3.py     # Advanced function patterns
├── examples/             # Example outputs and templates
└── tests/               # Test files
```

## Quick Start

1. Clone the repository
2. Navigate to this module: `cd function-calling-json-schema`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys
5. Read `theory.md` for concepts
6. Complete exercises in `src/`

## API Setup

This module uses **OpenRouter** for demonstrations, which provides access to multiple LLM models including GPT-4, Claude, and others. Set your API key in the `.env` file:

```
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

### Getting OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to your API keys section
4. Copy your API key
5. Add it to your `.env` file

## Exercises

- **Exercise 1**: Basic Function Calling - Implement simple function calling patterns
- **Exercise 2**: JSON Schema Validation - Create and validate JSON schemas
- **Exercise 3**: Advanced Function Patterns - Build complex function calling systems 