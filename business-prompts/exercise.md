# Exercise: Prompt Design for Business Workflows

## Objective

Design and test prompts that enable language models to perform useful business tasks across different departments. You will simulate **real-world workflows** by implementing domain-specific prompts for various business functions.

---

## Exercise Overview

This module contains **4 comprehensive exercises** covering different business domains:

### Exercise 1: Customer Support Automation
**Objective**: Implement prompts for customer support workflows including ticket classification, reply drafting, and sentiment analysis.

**Tasks**:
- Create ticket classification prompts
- Design reply drafting templates
- Implement sentiment analysis
- Test with real support scenarios

### Exercise 2: Sales & Marketing Workflows
**Objective**: Build prompts for sales and marketing operations including lead scoring, call summaries, and campaign generation.

**Tasks**:
- Design lead scoring algorithms
- Create call summary templates
- Implement campaign generation prompts
- Test with sales scenarios

### Exercise 3: HR & Operations
**Objective**: Develop prompts for HR and operations including resume screening, incident classification, and policy Q&A.

**Tasks**:
- Create resume screening prompts
- Design incident classification
- Implement policy Q&A systems
- Test with HR scenarios

### Exercise 4: Cross-Domain Integration
**Objective**: Integrate prompts across multiple business domains to create comprehensive workflow automation.

**Tasks**:
- Combine prompts from different departments
- Create multi-step workflows
- Implement cross-domain data processing
- Test end-to-end business processes

---

## General Instructions

### Step 1: Choose a Use Case

For each exercise, focus on the specific business domain:

* 💬 **Customer Support**: Drafting replies, assigning ticket urgency, sentiment analysis
* 📈 **Sales**: Scoring leads, summarizing call notes, campaign generation
* 🌐 **Marketing**: Generating campaign ideas, classifying audiences, content creation
* 🡩‍💼 **HR**: Screening resumes, drafting onboarding info, policy Q&A
* ⚙️ **Operations**: Categorizing reports, summarizing incidents, KPI analysis

### Step 2: Write the Prompt

Design structured prompts that:

* Clarify the model's role and business context
* Describe the input data and format
* Define the expected output format (JSON, Markdown, etc.)
* Include business-specific constraints and requirements

**Example Template:**

```
You are an AI assistant for the [department].
Analyze the following [input] and return a [structured output] with the following fields: [...]
Consider the business context: [specific business requirements]
```

### Step 3: Test Your Prompt

Use OpenRouter API to test the prompts. Review the output for:

* Format accuracy and consistency
* Business relevance and completeness
* Integration readiness for automation
* Error handling and edge cases

### Step 4: Reflect and Improve

For each exercise, answer:

1. Did the model return the correct structure and format?
2. Was the output usable for business automation?
3. How would you improve the prompt for production use?
4. What business value does this automation provide?

---

## Deliverable Format

Submit each exercise in this format:

### Exercise [Number]: [Domain] Automation

#### Prompt Design
```text
[Your prompt goes here]
```

#### Sample Output
```json
[LLM response output here]
```

#### Business Impact
```
1. [Business value provided]
2. [Automation benefits]
3. [Integration opportunities]
```

#### Reflection
```
1. [Format accuracy assessment]
2. [Business utility evaluation]
3. [Improvement suggestions]
```

---

## Bonus Challenge

Reframe your prompts to serve **multiple departments** with slight variations:

* How reusable is your prompt structure across domains?
* What parts are domain-specific vs. generalizable?
* How can you create a unified prompt framework?

---

## API Configuration

This module uses **OpenRouter API** for testing. Configure your environment:

1. Get your OpenRouter API key from [openrouter.ai](https://openrouter.ai/)
2. Set the environment variable: `OPENROUTER_API_KEY=your-key-here`
3. Use the provided test scripts in `src/` to validate your prompts

---

> **Remember**: Business workflow prompts bridge the gap between natural language and business logic, turning AI into a practical tool for enterprise automation. 