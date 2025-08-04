# Production Templates
# Week 1 - Road to AI Agent Engineer

import os
import json
from typing import Dict, Any, Optional

class ProductionSystem:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.logger = self.setup_logging()
        self.monitor = self.setup_monitoring()
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "api_keys": {
                "openai": os.getenv("OPENAI_API_KEY"),
                "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
                "openrouter": os.getenv("OPENROUTER_API_KEY")
            },
            "logging": {
                "level": "INFO",
                "file": "app.log"
            },
            "monitoring": {
                "enabled": True,
                "metrics_file": "metrics.json"
            }
        }
    
    def setup_logging(self):
        """Setup logging system."""
        import logging
        logging.basicConfig(
            level=getattr(logging, self.config["logging"]["level"]),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config["logging"]["file"]),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def setup_monitoring(self):
        """Setup monitoring system."""
        from templates.monitoring import SystemMonitor
        return SystemMonitor()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return {
            "status": "healthy",
            "config_loaded": bool(self.config),
            "logger_active": self.logger is not None,
            "monitor_active": self.monitor is not None
        }
    
    def graceful_shutdown(self):
        """Perform graceful shutdown."""
        self.logger.info("Shutting down system gracefully")
        # Save final metrics
        if self.config["monitoring"]["enabled"]:
            with open(self.config["monitoring"]["metrics_file"], 'w') as f:
                json.dump(self.monitor.get_stats(), f, indent=2)

def create_production_config():
    """Create a production configuration template."""
    return {
        "api_keys": {
            "openai": "your-openai-key",
            "huggingface": "your-huggingface-key",
            "openrouter": "your-openrouter-key"
        },
        "logging": {
            "level": "INFO",
            "file": "production.log"
        },
        "monitoring": {
            "enabled": True,
            "metrics_file": "production_metrics.json"
        },
        "safety": {
            "content_filtering": True,
            "input_sanitization": True,
            "disclaimers": True
        }
    } 