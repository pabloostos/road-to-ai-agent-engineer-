# Business Prompts: Workflow Automation

## Overview

This module covers prompt engineering for business workflows and enterprise automation. Learn how to design prompts that power real-world business operations across different departments.

## Learning Objectives

- Understand business workflow prompt design principles
- Create domain-specific prompts for different business functions
- Design structured outputs for automation and integration
- Implement prompts for customer support, sales, HR, and operations
- Master context preservation and goal alignment techniques

## Project Structure

```
business-prompts/
├── README.md              # This file
├── theory.md              # Theoretical concepts and business applications
├── exercise.md            # Practical exercises and tasks
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── src/                  # Source code
│   ├── exercise_1.py     # Customer support prompts
│   ├── exercise_2.py     # Sales and marketing prompts
│   ├── exercise_3.py     # HR and operations prompts
│   └── exercise_4.py     # Cross-domain business prompts
├── examples/             # Example outputs and templates
└── tests/               # Test files
```

## Quick Start

1. Clone the repository
2. Navigate to this module: `cd business-prompts`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys
5. Read `theory.md` for business workflow concepts
6. Complete exercises in `src/`

## API Setup

This module uses **OpenRouter API** for demonstrations, which provides access to multiple LLM models including GPT-4, Claude, and others. Set your API key in the `.env` file:

```
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

### Getting OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to your API keys section
4. Copy your API key
5. Add it to your `.env` file

## Business Domains Covered

- **Customer Support**: Ticket classification, reply drafting, sentiment analysis
- **Sales & Marketing**: Lead scoring, call summaries, campaign generation
- **HR & Talent**: Resume screening, interview summaries, policy Q&A
- **Operations & Analytics**: Log parsing, incident classification, KPI structuring

## Exercises

- **Exercise 1**: Customer Support Automation - Ticket classification and reply drafting
- **Exercise 2**: Sales & Marketing Workflows - Lead scoring and call summaries
- **Exercise 3**: HR & Operations - Resume screening and incident classification
- **Exercise 4**: Cross-Domain Integration - Multi-department workflow automation 