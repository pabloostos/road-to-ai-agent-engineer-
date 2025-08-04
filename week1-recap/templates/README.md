# 🛠️ Week 1 Templates Collection

## 📚 Overview

This folder contains 20 simplified template files covering all the patterns and techniques learned in Week 1 of the AI Agent Engineer course. Each file contains reusable functions and classes that can be imported and used in future projects.

## 📁 Template Files

### 🔑 **01_api_key_management.py**
- `load_api_key()` - Generic API key loader
- `load_openai_key()` - OpenAI API key loader
- `load_huggingface_key()` - Hugging Face API key loader
- `load_openrouter_key()` - OpenRouter API key loader
- `check_api_key_exists()` - Check if API key exists

### 🌐 **02_api_connection.py**
- `setup_openai_client()` - Setup OpenAI client
- `call_huggingface_api()` - Call Hugging Face API
- `call_openrouter_api()` - Call OpenRouter API

### 📊 **03_json_processing.py**
- `extract_json_from_response()` - Extract JSON from LLM response
- `parse_json_safely()` - Safely parse JSON string
- `validate_json_schema()` - Validate against JSON schema
- `create_simple_schema()` - Create simple JSON schema

### 🎭 **04_system_prompts.py**
- `create_basic_system_prompt()` - Create basic system prompt
- `create_role_prompt()` - Create detailed role prompt
- `create_format_prompt()` - Create format-specific prompts
- `create_behavior_prompt()` - Create behavior-specific prompts

### 🔧 **05_function_calling.py**
- `create_function_schema()` - Create function schema
- `simulate_function_call()` - Simulate function calling
- `create_weather_function()` - Weather function schema
- `create_calendar_function()` - Calendar function schema

### 🎯 **06_prompt_engineering.py**
- `create_json_prompt()` - Create JSON output prompts
- `create_api_simulation_prompt()` - Create API simulation prompts
- `create_business_prompt()` - Create business workflow prompts
- `create_structured_prompt()` - Create structured prompts

### 🛡️ **07_error_handling.py**
- `safe_api_call()` - Safely call API functions
- `validate_input()` - Validate input data
- `handle_json_error()` - Handle JSON parsing errors
- `create_error_response()` - Create standardized error response
- `retry_on_failure()` - Retry function on failure

### 📝 **08_logging.py**
- `setup_logging()` - Setup basic logging
- `log_api_call()` - Log API call details
- `log_conversation()` - Log conversation details
- `save_to_json_log()` - Save data to JSON log
- `log_error()` - Log error with details

### 🗂️ **09_file_management.py**
- `create_directory()` - Create directory if it doesn't exist
- `save_json()` - Save data to JSON file
- `load_json()` - Load data from JSON file
- `append_to_json()` - Append data to existing JSON file
- `list_files()` - List files in directory

### ✅ **10_data_validation.py**
- `validate_email()` - Validate email format
- `validate_required_fields()` - Validate required fields
- `validate_data_types()` - Validate data types
- `validate_string_length()` - Validate string length
- `validate_numeric_range()` - Validate numeric range
- `create_validation_schema()` - Create validation schema

### 💼 **11_business_workflows.py**
- `create_support_ticket_classifier()` - Support ticket classification
- `create_lead_scorer()` - Lead scoring
- `create_resume_screener()` - Resume screening
- `create_incident_classifier()` - Incident classification
- `create_customer_journey_analyzer()` - Customer journey analysis
- `create_workflow_orchestrator()` - Workflow orchestration
- `create_business_intelligence()` - Business intelligence
- `create_policy_qa()` - Policy Q&A

### 🧪 **12_testing.py**
- `test_api_connection()` - Test API connection
- `test_json_parsing()` - Test JSON parsing
- `test_schema_validation()` - Test schema validation
- `run_test_suite()` - Run a suite of tests
- `benchmark_function()` - Benchmark function performance

### 📊 **13_monitoring.py**
- `SystemMonitor` class - System monitoring
- `create_health_check()` - Create health check
- `monitor_performance()` - Performance monitoring decorator

### 🛡️ **14_safety.py**
- `filter_sensitive_content()` - Filter sensitive information
- `validate_safe_content()` - Validate content is safe
- `add_safety_disclaimer()` - Add safety disclaimers
- `sanitize_input()` - Sanitize user input
- `check_content_safety()` - Check content for safety issues

### 🚀 **15_production.py**
- `ProductionSystem` class - Production-ready system
- `create_production_config()` - Create production configuration

### 🎨 **16_formatting.py**
- `format_json_response()` - Format JSON response
- `format_markdown_table()` - Format Markdown table
- `format_bullet_list()` - Format bullet list
- `format_numbered_list()` - Format numbered list
- `format_code_block()` - Format code block
- `format_http_response()` - Format HTTP response
- `format_api_response()` - Format standardized API response

### 🔗 **17_integration.py**
- `APIIntegration` class - API integration
- `ServiceConnector` class - Service connector
- `create_data_flow()` - Create data flow pipeline
- `create_workflow_integration()` - Create workflow integration

### 📚 **18_documentation.py**
- `create_function_docstring()` - Create function docstring
- `create_class_docstring()` - Create class docstring
- `create_api_documentation()` - Create API documentation
- `create_usage_example()` - Create usage example
- `create_config_documentation()` - Create configuration documentation

### 🚀 **19_deployment.py**
- `create_requirements_file()` - Create requirements.txt
- `create_env_example()` - Create .env.example
- `create_gitignore()` - Create .gitignore
- `create_dockerfile()` - Create Dockerfile
- `create_docker_compose()` - Create docker-compose.yml
- `create_deployment_config()` - Create deployment configuration
- `create_startup_script()` - Create startup script
- `create_health_check_endpoint()` - Create health check endpoint

### 📖 **20_learning.py**
- `ExerciseFramework` class - Exercise framework
- `create_practice_scenario()` - Create practice scenario
- `create_test_framework()` - Create test framework
- `create_evaluation_metrics()` - Create evaluation metrics
- `create_progress_tracker()` - Create progress tracker

## 🎯 Usage Examples

### Basic Usage
```python
# Import templates
from templates.api_key_management import load_openai_key
from templates.api_connection import call_openai_api
from templates.json_processing import parse_json_safely

# Use templates
api_key = load_openai_key()
response = call_openai_api(api_key, "Hello world")
data = parse_json_safely(response)
```

### Advanced Usage
```python
# Import multiple templates
from templates.production import ProductionSystem
from templates.monitoring import SystemMonitor
from templates.safety import validate_safe_content

# Create production system
system = ProductionSystem()
monitor = SystemMonitor()

# Use with safety checks
if validate_safe_content(user_input):
    result = system.process(user_input)
    monitor.record_api_call(True, response_time)
```

## 🚀 Quick Start

1. **Copy the templates** to your project
2. **Import the functions** you need
3. **Customize the templates** for your specific use case
4. **Combine multiple templates** for complex workflows

## 📋 Template Categories

### **Core Infrastructure**
- API Key Management
- API Connections
- JSON Processing
- Error Handling
- Logging
- File Management

### **AI/LLM Features**
- System Prompts
- Function Calling
- Prompt Engineering
- Data Validation
- Safety Features

### **Business Applications**
- Business Workflows
- Testing
- Monitoring
- Production Deployment

### **Development Tools**
- Formatting
- Integration
- Documentation
- Deployment
- Learning Framework

## 🎓 Learning Path

1. **Start with core templates** (01-06)
2. **Add error handling and logging** (07-09)
3. **Implement validation and safety** (10, 14)
4. **Build business workflows** (11-13)
5. **Deploy to production** (15-19)
6. **Use learning framework** (20)

---

*These templates provide a solid foundation for building AI agent systems and can be customized for specific project requirements.* 