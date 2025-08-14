# Exercise: Prompt Versioning with LangSmith

## Objective
Implement a comprehensive prompt versioning system using **LangSmith** - the industry-standard platform for LLM experiment tracking and prompt management. Learn how to:
1. **Track prompt experiments** with automatic versioning
2. **Compare performance** across different prompt versions
3. **Manage metadata** and experiment configurations
4. **Generate reports** and analyze results
5. **Collaborate** with teams on prompt development

---

## Requirements
- **LangSmith Account:** Sign up at [smith.langchain.com](https://smith.langchain.com)
- **LLM Provider:** OpenRouter API (GPT-3.5-turbo or GPT-4)
- **Libraries:** `langsmith`, `langchain`, `requests`, `json`, `os`, `datetime`, `python-dotenv`
- **Concepts:** Experiment tracking, prompt management, performance analysis

---

## Exercise Structure

### 1. Setup Environment
- Create LangSmith account and get API key
- Set `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT` in `.env`
- Install dependencies: `pip install -r requirements.txt`

### 2. Implement `LangSmithPromptVersioning` Class

Create a class that leverages LangSmith for comprehensive prompt management:

#### `__init__(self, project_name: str = "prompt-versioning-demo")`
- Initialize LangSmith client
- Set up project for experiment tracking
- Configure default model and parameters

#### `create_prompt_experiment(self, prompt_name: str, prompt_text: str, metadata: dict) -> str`
- Create a new experiment in LangSmith
- Store prompt with metadata and tags
- Return experiment ID for tracking

#### `test_prompt_version(self, experiment_id: str, test_inputs: list, model_params: dict = None) -> dict`
- Run prompt against multiple test inputs
- Track performance metrics automatically
- Store results in LangSmith dashboard

#### `compare_experiments(self, experiment_ids: list) -> dict`
- Compare performance across multiple experiments
- Generate statistical analysis
- Create comparison reports

#### `generate_changelog(self, experiment_ids: list) -> str`
- Extract changelog from LangSmith experiment history
- Include performance metrics and metadata
- Format for team documentation

#### `export_results(self, experiment_id: str, format: str = "json") -> str`
- Export experiment results and metadata
- Support JSON, CSV, and markdown formats
- Include performance metrics and traces

### 3. Create Test Scenarios

#### Scenario 1: Customer Service Email Generator
Create multiple prompt versions and test them:

**Experiment 1:** Basic professional response
```python
prompt_v1 = "Write a professional response to a customer inquiry about {topic}."
metadata_v1 = {
    "version": "1.0",
    "author": "Alice",
    "tone": "professional",
    "target_length": "short"
}
```

**Experiment 2:** Empathetic and helpful
```python
prompt_v2 = "Write an empathetic and helpful response to a customer inquiry about {topic}. Show understanding and provide clear solutions."
metadata_v2 = {
    "version": "1.1", 
    "author": "Bob",
    "tone": "empathetic",
    "target_length": "medium",
    "improvement": "more_caring"
}
```

**Experiment 3:** Action-oriented
```python
prompt_v3 = "Write a response to a customer inquiry about {topic}. Include specific next steps and contact information."
metadata_v3 = {
    "version": "1.2",
    "author": "Charlie", 
    "tone": "actionable",
    "target_length": "medium",
    "improvement": "specific_actions"
}
```

#### Scenario 2: Code Review Assistant
Iterate on code review prompts:

**Experiment 1:** General code review
**Experiment 2:** Security-focused review
**Experiment 3:** Performance optimization review
**Experiment 4:** Multi-language support

### 4. Performance Evaluation with LangSmith

LangSmith automatically tracks:
- **Response Time:** Latency measurements
- **Token Usage:** Input/output token counts
- **Cost Tracking:** API call costs
- **Quality Metrics:** Custom evaluation scores
- **Trace Analysis:** Step-by-step execution flow

### 5. Advanced Features

#### A/B Testing Framework
```python
def run_ab_test(self, experiment_a_id: str, experiment_b_id: str, test_inputs: list) -> dict:
    """Run A/B test between two prompt versions"""
    # Run both experiments with same inputs
    # Calculate statistical significance
    # Generate comparison report
```

#### Automated Quality Scoring
```python
def evaluate_response_quality(self, response: str, criteria: dict) -> float:
    """Use a second LLM to evaluate response quality"""
    # Implement custom evaluation criteria
    # Score responses on multiple dimensions
    # Store scores in LangSmith metadata
```

#### Team Collaboration Features
```python
def share_experiment(self, experiment_id: str, team_members: list) -> bool:
    """Share experiment results with team members"""
    # Use LangSmith sharing features
    # Add comments and feedback
    # Track collaboration history
```

---

## Example Implementation Structure

```python
from langsmith import Client
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from datetime import datetime

class LangSmithPromptVersioning:
    def __init__(self, project_name="prompt-versioning-demo"):
        """Initialize LangSmith client and project"""
        self.client = Client()
        self.project_name = project_name
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY")
        )
    
    def create_prompt_experiment(self, prompt_name, prompt_text, metadata):
        """Create a new prompt experiment in LangSmith"""
        # Create experiment with metadata
        experiment = self.client.create_experiment(
            name=f"{prompt_name}_{metadata['version']}",
            description=prompt_text,
            metadata=metadata
        )
        return experiment.id
    
    def test_prompt_version(self, experiment_id, test_inputs, model_params=None):
        """Test a prompt version with multiple inputs"""
        results = []
        
        for input_text in test_inputs:
            # Create prompt template
            prompt = ChatPromptTemplate.from_template(
                "You are a helpful assistant. {prompt_text}\n\nUser: {input}\nAssistant:"
            )
            
            # Run with LangSmith tracing
            with self.client.trace(
                project_name=self.project_name,
                experiment_id=experiment_id
            ) as tracer:
                response = self.llm.invoke(
                    prompt.format(prompt_text=prompt_text, input=input_text)
                )
                
                # Log results
                tracer.log(
                    inputs={"input": input_text},
                    outputs={"response": response.content},
                    metadata=model_params or {}
                )
                
                results.append({
                    "input": input_text,
                    "response": response.content,
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    def compare_experiments(self, experiment_ids):
        """Compare performance across experiments"""
        # Use LangSmith API to fetch experiment data
        # Generate comparison metrics
        # Create visualization-ready data
        pass
    
    def generate_changelog(self, experiment_ids):
        """Generate changelog from experiment history"""
        # Extract experiment metadata and results
        # Format as markdown changelog
        # Include performance trends
        pass

# Usage Example
versioning = LangSmithPromptVersioning()

# Create email prompt experiments
email_v1 = versioning.create_prompt_experiment(
    "customer_email",
    "Write a professional response to a customer inquiry about {topic}.",
    {"version": "1.0", "author": "Alice", "tone": "professional"}
)

email_v2 = versioning.create_prompt_experiment(
    "customer_email",
    "Write an empathetic and helpful response to a customer inquiry about {topic}. Show understanding and provide clear solutions.",
    {"version": "1.1", "author": "Bob", "tone": "empathetic"}
)

# Test with sample inputs
test_inputs = [
    "My order hasn't arrived yet",
    "The product is defective", 
    "I want to cancel my subscription"
]

results_v1 = versioning.test_prompt_version(email_v1, test_inputs)
results_v2 = versioning.test_prompt_version(email_v2, test_inputs)

# Compare experiments
comparison = versioning.compare_experiments([email_v1, email_v2])
print(comparison)
```

---

## Expected Deliverables

1. **Complete Python Implementation** (`langsmith_prompt_versioning.py`)
2. **LangSmith Project** with multiple experiments and traces
3. **Performance Comparison Report** (exported from LangSmith)
4. **Generated Changelog** (markdown format)
5. **Experiment Documentation** (screenshots and analysis)
6. **Team Collaboration Demo** (shared experiments and feedback)

---

## Bonus Challenges

1. **Custom Evaluators:** Implement LangSmith custom evaluators for quality scoring
2. **Automated Testing:** Set up CI/CD pipeline with LangSmith integration
3. **Dashboard Creation:** Build custom dashboard using LangSmith API
4. **Multi-Model Testing:** Compare performance across different LLM providers
5. **Production Integration:** Deploy prompt versioning to production environment
6. **Advanced Analytics:** Create custom analytics using LangSmith data exports

---

## Learning Outcomes

By completing this exercise, you will understand:
- How to use LangSmith for professional prompt management
- Best practices for experiment tracking and versioning
- How to implement A/B testing for prompt optimization
- Team collaboration workflows with shared experiments
- Performance analysis and reporting techniques
- Production-ready prompt deployment strategies

---

## Evaluation Criteria

- **LangSmith Integration:** Proper use of LangSmith features and API
- **Experiment Design:** Well-structured experiments with meaningful metadata
- **Performance Analysis:** Comprehensive comparison and insights
- **Documentation:** Clear changelog and experiment documentation
- **Collaboration:** Effective use of LangSmith sharing features
- **Code Quality:** Clean, well-documented, modular implementation
- **Advanced Features:** Implementation of bonus challenges
