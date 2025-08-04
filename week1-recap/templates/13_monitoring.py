# Monitoring Templates
# Week 1 - Road to AI Agent Engineer

import time
from datetime import datetime
from typing import Dict, Any, List

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            "api_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "average_response_time": 0,
            "total_response_time": 0
        }
    
    def record_api_call(self, success: bool, response_time: float):
        """Record API call metrics."""
        self.metrics["api_calls"] += 1
        self.metrics["total_response_time"] += response_time
        
        if success:
            self.metrics["successful_calls"] += 1
        else:
            self.metrics["failed_calls"] += 1
        
        self.metrics["average_response_time"] = (
            self.metrics["total_response_time"] / self.metrics["api_calls"]
        )
    
    def get_success_rate(self) -> float:
        """Calculate success rate."""
        if self.metrics["api_calls"] == 0:
            return 0
        return self.metrics["successful_calls"] / self.metrics["api_calls"]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return {
            **self.metrics,
            "success_rate": self.get_success_rate(),
            "timestamp": datetime.now().isoformat()
        }

def create_health_check():
    """Create a basic health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

def monitor_performance(func: callable):
    """Decorator to monitor function performance."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            success = False
            result = str(e)
        
        response_time = time.time() - start_time
        
        return {
            "success": success,
            "result": result,
            "response_time": response_time
        }
    
    return wrapper 