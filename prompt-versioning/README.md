# Prompt Versioning with LangSmith

## Overview

This module covers **Prompt Versioning** using **LangSmith** - the industry-standard platform for LLM experiment tracking and prompt management. Learn how to systematically track, compare, and optimize prompts using professional-grade tools that are used by leading AI companies.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- **Use LangSmith** for professional prompt experiment tracking
- **Compare performance** across different prompt versions systematically
- **Manage metadata** and experiment configurations effectively
- **Generate reports** and analyze results using LangSmith dashboard
- **Collaborate with teams** on prompt development and optimization
- **Implement A/B testing** for prompt performance evaluation

## 📚 Theory Coverage

### Key Concepts Covered:
1. **Why Prompt Versioning Matters**
   - Reproducibility in AI experiments
   - Experiment tracking and optimization
   - Team collaboration workflows
   - Debugging and performance monitoring

2. **LangSmith Platform Features**
   - Automatic experiment tracking
   - Performance metrics and visualization
   - Team collaboration tools
   - Custom evaluators and scoring

3. **Best Practices**
   - Experiment design and metadata
   - Performance comparison methodologies
   - Team collaboration workflows
   - Production deployment strategies

4. **Real-World Applications**
   - Chatbot development and optimization
   - Data processing pipeline evolution
   - Search system performance tracking

## 🛠️ Tools & Technologies

### Core Technologies:
- **LangSmith** - Professional experiment tracking platform
- **LangChain** - LLM framework integration
- **OpenRouter API** - Multi-model LLM access
- **Python** - Implementation language

### Key Libraries:
- `langsmith` - LangSmith client and API
- `langchain` - LLM framework and tools
- `langchain-openai` - OpenAI/OpenRouter integration
- `requests` - API communication
- `pandas` - Data analysis and processing

## 📁 Module Structure

```
prompt-versioning/
├── theory.md                    # Comprehensive theory content
├── exercise.md                  # LangSmith-based exercise instructions
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .env                         # Environment variables (copy from .env.example)
├── .env.example                 # Environment template
├── src/
│   └── langsmith_prompt_versioning.py  # Main implementation
├── examples/
│   ├── email_experiments/       # Sample email prompt experiments
│   └── code_review_experiments/ # Sample code review experiments
└── tests/
    └── test_langsmith_versioning.py    # Unit tests
```

## 🚀 Getting Started

### 1. LangSmith Setup
```bash
# Sign up for LangSmith account
# Visit: https://smith.langchain.com

# Get your API key from LangSmith dashboard
# Set up your first project
```

### 2. Environment Setup
```bash
# Navigate to the module directory
cd prompt-versioning

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys:
# LANGSMITH_API_KEY=your_langsmith_key
# LANGSMITH_PROJECT=your_project_name
# OPENROUTER_API_KEY=your_openrouter_key
```

### 3. Prerequisites
- **LangSmith Account** - Free tier available at [smith.langchain.com](https://smith.langchain.com)
- **OpenRouter API Key** - For testing prompts with various LLMs
- **Python 3.8+** - For running the implementation

### 4. Quick Start
```python
from src.langsmith_prompt_versioning import LangSmithPromptVersioning

# Initialize the system
versioning = LangSmithPromptVersioning("my-prompt-project")

# Create your first experiment
experiment_id = versioning.create_prompt_experiment(
    "customer_email",
    "Write a professional response to a customer inquiry about {topic}.",
    {"version": "1.0", "author": "Alice", "tone": "professional"}
)

# Test the prompt
test_inputs = ["My order is late", "Product is defective"]
results = versioning.test_prompt_version(experiment_id, test_inputs)
print(results)

# View results in LangSmith dashboard
# Visit: https://smith.langchain.com
```

## 📊 Exercise Overview

### Main Exercise: LangSmith Prompt Versioning System

**Objective:** Implement a comprehensive prompt versioning system using LangSmith for professional-grade experiment tracking.

**Key Features to Implement:**
1. **LangSmith Integration** - Automatic experiment tracking and tracing
2. **Performance Comparison** - Statistical analysis across experiments
3. **Metadata Management** - Structured experiment information
4. **Team Collaboration** - Shared experiments and feedback
5. **Custom Evaluators** - Quality scoring and metrics

### Test Scenarios:
1. **Customer Service Email Generator** - Iterate on response quality and tone
2. **Code Review Assistant** - Optimize for different review focuses

### Expected Deliverables:
- Complete Python implementation with LangSmith
- LangSmith project with multiple experiments
- Performance comparison reports
- Generated changelogs and documentation
- Team collaboration demonstration
- Custom evaluators implementation

## 🎓 Learning Path

### Before This Module:
- ✅ Prompt Engineering fundamentals
- ✅ System prompts and role-playing
- ✅ Function calling and JSON schema
- ✅ Business workflow prompts
- ✅ Response caching
- ✅ Retry and error handling
- ✅ Token usage monitoring
- ✅ Content moderation

### After This Module:
- 🔄 Prompt optimization techniques
- 🔄 A/B testing for AI systems
- 🔄 Performance evaluation frameworks
- 🔄 Production deployment strategies

## 🔧 Advanced Features

### Bonus Challenges:
1. **Custom Evaluators** - Implement LangSmith custom evaluators for quality scoring
2. **Automated Testing** - Set up CI/CD pipeline with LangSmith integration
3. **Dashboard Creation** - Build custom dashboard using LangSmith API
4. **Multi-Model Testing** - Compare performance across different LLM providers
5. **Production Integration** - Deploy prompt versioning to production environment
6. **Advanced Analytics** - Create custom analytics using LangSmith data exports

## 📈 Success Metrics

### Technical Competencies:
- ✅ LangSmith platform mastery
- ✅ Experiment design and tracking
- ✅ Performance analysis and comparison
- ✅ Team collaboration workflows
- ✅ Custom evaluator implementation

### Practical Skills:
- ✅ Professional experiment tracking
- ✅ Statistical analysis techniques
- ✅ Team collaboration best practices
- ✅ Documentation and reporting
- ✅ Production deployment strategies

## 🆘 Troubleshooting

### Common Issues:
1. **LangSmith API Errors** - Verify API key and project setup
2. **OpenRouter API Issues** - Check API key and rate limits
3. **Import Errors** - Ensure all dependencies are installed
4. **Experiment Tracking** - Verify LangSmith project configuration

### Getting Help:
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Community](https://discord.gg/langchain)
- Check exercise.md for detailed implementation guidance
- Review theory.md for conceptual understanding

## 📚 Additional Resources

### Documentation:
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenRouter API Docs](https://openrouter.ai/docs)

### Tools & Platforms:
- [LangSmith](https://smith.langchain.com/) - Professional experiment tracking
- [Weights & Biases](https://wandb.ai/) - Alternative experiment tracking
- [MLflow](https://mlflow.org/) - Open-source experiment tracking

### Best Practices:
- [LangSmith Best Practices](https://docs.smith.langchain.com/how-tos/)
- [Experiment Design](https://www.coursera.org/learn/experimentation) - Statistical methods
- [A/B Testing](https://www.optimizely.com/optimization-glossary/ab-testing/) - Testing methodologies

---

**Ready to master professional prompt versioning with LangSmith? Let's build industry-standard experiment tracking! 🚀**
