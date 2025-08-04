# Integration Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List, Callable

class APIIntegration:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def make_request(self, endpoint: str, method: str = "GET", data: Dict[str, Any] = None):
        """Make API request."""
        import requests
        
        url = f"{self.base_url}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=self.headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=self.headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()

class ServiceConnector:
    def __init__(self):
        self.services = {}
    
    def register_service(self, name: str, service_func: Callable):
        """Register a service function."""
        self.services[name] = service_func
    
    def call_service(self, name: str, *args, **kwargs):
        """Call a registered service."""
        if name not in self.services:
            raise ValueError(f"Service '{name}' not found")
        
        return self.services[name](*args, **kwargs)

def create_data_flow(source: Callable, processor: Callable, destination: Callable):
    """Create a data flow pipeline."""
    def pipeline(data):
        # Extract data from source
        raw_data = source(data)
        
        # Process data
        processed_data = processor(raw_data)
        
        # Send to destination
        return destination(processed_data)
    
    return pipeline

def create_workflow_integration(workflow_steps: List[Callable]):
    """Create a workflow integration."""
    def execute_workflow(input_data):
        result = input_data
        
        for step in workflow_steps:
            result = step(result)
        
        return result
    
    return execute_workflow 