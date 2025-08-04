# Deployment Templates
# Week 1 - Road to AI Agent Engineer

import os
import json
from typing import Dict, Any, List

def create_requirements_file(dependencies: List[str]) -> str:
    """Create requirements.txt file."""
    return "\n".join(dependencies)

def create_env_example(env_vars: List[str]) -> str:
    """Create .env.example file."""
    return "\n".join([f"{var}=your-{var.lower()}-here" for var in env_vars])

def create_gitignore(patterns: List[str]) -> str:
    """Create .gitignore file."""
    return "\n".join(patterns)

def create_dockerfile(base_image: str = "python:3.9", requirements_file: str = "requirements.txt") -> str:
    """Create Dockerfile."""
    return f"""FROM {base_image}

WORKDIR /app

COPY {requirements_file} .
RUN pip install -r {requirements_file}

COPY . .

CMD ["python", "app.py"]"""

def create_docker_compose(services: Dict[str, Dict[str, Any]]) -> str:
    """Create docker-compose.yml file."""
    import yaml
    
    compose = {
        "version": "3.8",
        "services": services
    }
    
    return yaml.dump(compose, default_flow_style=False)

def create_deployment_config(environment: str = "production") -> Dict[str, Any]:
    """Create deployment configuration."""
    configs = {
        "production": {
            "logging_level": "INFO",
            "monitoring_enabled": True,
            "safety_checks": True,
            "rate_limiting": True
        },
        "development": {
            "logging_level": "DEBUG",
            "monitoring_enabled": False,
            "safety_checks": False,
            "rate_limiting": False
        }
    }
    
    return configs.get(environment, configs["development"])

def create_startup_script(entry_point: str = "app.py") -> str:
    """Create startup script."""
    return f"""#!/bin/bash

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Start application
python {entry_point}"""

def create_health_check_endpoint():
    """Create health check endpoint."""
    return """@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })""" 