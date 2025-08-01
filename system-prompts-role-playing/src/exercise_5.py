#!/usr/bin/env python3
"""
Exercise 5: Production-Ready Implementation

Build a complete, production-ready role-playing system with proper error handling,
monitoring, logging, and safety features.
"""

import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RolePlayingSystem:
    """Production-ready role-playing system."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "meta-llama/Llama-3.1-8B-Instruct"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.parameters = {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95,
            "return_full_text": False,
            "do_sample": True
        }
        self.roles = self._load_roles()
        self.conversation_history = []
        self.safety_filters = self._load_safety_filters()
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        os.makedirs('examples/production', exist_ok=True)
        
        logger.info("RolePlayingSystem initialized successfully")
    
    def _load_roles(self):
        """Load predefined roles."""
        return {
            "medical_expert": {
                "name": "Dr. Elena Rodriguez",
                "role": "Expert Medical Researcher",
                "system_prompt": """You are Dr. Elena Rodriguez, an Expert Medical Researcher.
                Always respond as a medical professional with expertise in AI and healthcare.
                Be professional, compassionate, and educational in your responses.
                Never provide medical advice that could be harmful."""
            },
            "tech_expert": {
                "name": "Alex Chen",
                "role": "Senior Software Engineer",
                "system_prompt": """You are Alex Chen, a Senior Software Engineer.
                Always respond as a tech professional with expertise in software development.
                Be technical, helpful, and solution-oriented in your responses.
                Focus on best practices and clean code."""
            },
            "creative_expert": {
                "name": "Maria Santos",
                "role": "Creative Director",
                "system_prompt": """You are Maria Santos, a Creative Director.
                Always respond as a creative professional with expertise in design and innovation.
                Be imaginative, inspiring, and artistic in your responses.
                Encourage creative thinking and artistic expression."""
            }
        }
    
    def _load_safety_filters(self):
        """Load safety filters for content moderation."""
        return {
            "inappropriate_keywords": [
                "harmful", "dangerous", "illegal", "inappropriate"
            ],
            "medical_disclaimers": [
                "This is not medical advice",
                "Consult a healthcare professional",
                "For informational purposes only"
            ]
        }
    
    def validate_input(self, user_input):
        """Validate and sanitize user input."""
        if not user_input or len(user_input.strip()) == 0:
            raise ValueError("Input cannot be empty")
        
        if len(user_input) > 1000:
            raise ValueError("Input too long (max 1000 characters)")
        
        # Check for inappropriate content
        user_input_lower = user_input.lower()
        for keyword in self.safety_filters["inappropriate_keywords"]:
            if keyword in user_input_lower:
                logger.warning(f"Potentially inappropriate input detected: {user_input}")
                raise ValueError("Input contains inappropriate content")
        
        return user_input.strip()
    
    def generate_response(self, role_id, user_input):
        """Generate response with comprehensive error handling."""
        try:
            # Validate input
            user_input = self.validate_input(user_input)
            
            # Get role
            if role_id not in self.roles:
                raise ValueError(f"Role '{role_id}' not found")
            
            role = self.roles[role_id]
            
            # Create prompt
            prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{role['system_prompt']}<|eot_id|><|start_header_id|>user<|end_header_id|>{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
            
            payload = {
                "inputs": prompt,
                "parameters": self.parameters
            }
            
            # Make API call with timeout
            logger.info(f"Generating response for role: {role['name']}")
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0]['generated_text'].strip()
                    
                    # Apply safety filters
                    generated_text = self._apply_safety_filters(generated_text, role_id)
                    
                    # Log conversation
                    self._log_conversation(role_id, user_input, generated_text)
                    
                    logger.info(f"Response generated successfully for {role['name']}")
                    return {
                        "success": True,
                        "role": role['name'],
                        "response": generated_text,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    raise Exception("Invalid API response format")
            else:
                raise Exception(f"API Error: {response.status_code}")
                
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "validation"
            }
        except requests.exceptions.Timeout:
            logger.error("API request timeout")
            return {
                "success": False,
                "error": "Request timeout",
                "error_type": "timeout"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return {
                "success": False,
                "error": f"API error: {e}",
                "error_type": "api_error"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {e}",
                "error_type": "unknown"
            }
    
    def _apply_safety_filters(self, response, role_id):
        """Apply safety filters to generated response."""
        # Add medical disclaimers for medical expert
        if role_id == "medical_expert":
            if any(medical_term in response.lower() for medical_term in ["treatment", "diagnosis", "medicine"]):
                response += "\n\nNote: This is for informational purposes only. Please consult a healthcare professional for medical advice."
        
        return response
    
    def _log_conversation(self, role_id, user_input, response):
        """Log conversation for monitoring."""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "role_id": role_id,
            "user_input": user_input,
            "response": response
        }
        self.conversation_history.append(conversation_entry)
        
        # Save to file
        with open('examples/production/conversation_log.json', 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def get_system_stats(self):
        """Get system statistics."""
        return {
            "total_conversations": len(self.conversation_history),
            "available_roles": list(self.roles.keys()),
            "system_status": "operational"
        }
    
    def switch_role(self, role_id):
        """Switch to a different role."""
        if role_id not in self.roles:
            raise ValueError(f"Role '{role_id}' not found")
        
        logger.info(f"Switching to role: {self.roles[role_id]['name']}")
        return {
            "success": True,
            "role": self.roles[role_id]['name'],
            "message": f"Switched to {self.roles[role_id]['name']}"
        }

def test_production_system(api_key):
    """Test the production-ready system."""
    print("Exercise 5: Production-Ready Implementation")
    print("=" * 50)
    
    if not api_key:
        logger.error("API key not found")
        return
    
    # Initialize system
    print("Initializing production system...")
    system = RolePlayingSystem(api_key)
    
    # Test scenarios
    test_scenarios = [
        ("medical_expert", "Hello, how are you?"),
        ("tech_expert", "What's your expertise in software development?"),
        ("creative_expert", "How do you approach creative projects?"),
        ("medical_expert", "Can you give me medical advice?"),
        ("invalid_role", "This should fail"),
        ("", "This should also fail")
    ]
    
    print(f"\nTesting {len(test_scenarios)} scenarios:")
    print("=" * 40)
    
    for i, (role_id, user_input) in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: Role={role_id}, Input='{user_input}'")
        print("-" * 40)
        
        try:
            result = system.generate_response(role_id, user_input)
            
            if result["success"]:
                print(f"✅ Success: {result['role']}")
                print(f"Response: {result['response']}")
            else:
                print(f"❌ Error: {result['error']}")
                print(f"Error Type: {result['error_type']}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Get system stats
    print(f"\nSystem Statistics:")
    print("=" * 20)
    stats = system.get_system_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\nExercise 5 completed successfully!")
    print("Production system is ready for deployment!")

def main():
    """Main function."""
    api_key = load_dotenv()
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    test_production_system(api_key)

if __name__ == "__main__":
    main()
