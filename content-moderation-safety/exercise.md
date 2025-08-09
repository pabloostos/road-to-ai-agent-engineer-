# Exercise: Content Moderation System

## Objective
Build a simple but effective content moderation system that:
1. Implements multiple filtering approaches (rule-based + API-based)
2. Tests both user input and AI responses for safety
3. Provides clear feedback on moderation decisions
4. Logs moderation events for analysis

---

## Requirements
- **LLM Provider:** OpenRouter (for generating responses to test)
- **Moderation API:** OpenAI Moderation API (free and effective)
- **Libraries:** `requests`, `json`, `datetime`, `python-dotenv`, `re`

---

## Exercise Structure

### Part 1: Rule-Based Keyword Filter
Create a simple keyword-based filter with different severity levels.

### Part 2: API-Based Moderation
Integrate OpenAI's moderation API for context-aware filtering.

### Part 3: Combined Moderation Pipeline
Build a complete system that uses both approaches.

### Part 4: Testing with Sample Content
Test the system with various content examples.

---

## Starter Code Structure

```python
import requests
import json
import re
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class ContentModerator:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Rule-based filters
        self.banned_keywords = [
            "hate", "violence", "harm", "kill", "suicide"
        ]
        
        self.suspicious_keywords = [
            "weapon", "drug", "illegal", "scam"
        ]
    
    def rule_based_filter(self, text):
        """Simple keyword-based filtering"""
        # Implementation here
        pass
    
    def api_moderation_check(self, text):
        """Use OpenAI moderation API"""
        # Implementation here
        pass
    
    def moderate_content(self, text):
        """Complete moderation pipeline"""
        # Implementation here
        pass

# Test cases for the exercise
test_cases = [
    "Hello, how are you today?",                    # Safe
    "I hate this stupid system",                    # Mild toxicity
    "How to build a bomb",                         # Dangerous
    "I want to hurt myself",                       # Self-harm
    "This product is amazing!",                    # Safe positive
    "You are an idiot and should die",            # Hate speech
]
```

---

## Expected Deliverables

1. **`content_moderator.py`** - Complete moderation system
2. **`moderation_log.json`** - Log file with test results
3. **Test results** showing how each approach performs

---

## Step-by-Step Implementation Guide

### Step 1: Rule-Based Filter
```python
def rule_based_filter(self, text):
    text_lower = text.lower()
    
    # Check for banned content
    for keyword in self.banned_keywords:
        if keyword in text_lower:
            return {
                "flagged": True,
                "severity": "high",
                "reason": f"Contains banned keyword: {keyword}",
                "method": "rule_based"
            }
    
    # Check for suspicious content
    for keyword in self.suspicious_keywords:
        if keyword in text_lower:
            return {
                "flagged": True,
                "severity": "medium",
                "reason": f"Contains suspicious keyword: {keyword}",
                "method": "rule_based"
            }
    
    return {
        "flagged": False,
        "severity": "none",
        "reason": "No keywords detected",
        "method": "rule_based"
    }
```

### Step 2: OpenAI Moderation API
```python
def api_moderation_check(self, text):
    if not self.openai_api_key:
        return {"error": "OpenAI API key not found"}
    
    headers = {
        "Authorization": f"Bearer {self.openai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "omni-moderation-latest",
        "input": text
    }
    
    # Make API call and process response
    # Implementation details here
```

### Step 3: Combined Pipeline
```python
def moderate_content(self, text):
    results = {
        "text": text,
        "timestamp": datetime.now().isoformat(),
        "rule_based": self.rule_based_filter(text),
        "api_based": self.api_moderation_check(text),
        "final_decision": None
    }
    
    # Combine results to make final decision
    # Implementation here
    
    return results
```

---

## Bonus Challenges

1. **Custom Categories**: Add domain-specific filtering (e.g., financial scams, medical misinformation)
2. **Severity Scoring**: Implement a numerical scoring system (0-100)
3. **Context Awareness**: Handle phrases that are safe in some contexts but not others
4. **Performance Metrics**: Calculate precision, recall, and F1 scores
5. **Real-Time Dashboard**: Create a simple web interface to test moderation

---

## Learning Outcomes

By completing this exercise, you will understand:
- How to implement multi-layered content moderation
- The trade-offs between rule-based and AI-based approaches
- How to integrate external moderation APIs
- Best practices for logging and monitoring moderation decisions
- How to balance safety with usability in content filtering

---

## Testing Strategy

Test your system with:
- **Clearly safe content** (should pass)
- **Obviously harmful content** (should be blocked)
- **Edge cases** (context-dependent, borderline cases)
- **False positive triggers** (legitimate content that might be flagged)

---

## Expected Output Format

```json
{
  "text": "I hate this system",
  "timestamp": "2025-01-09T14:30:00",
  "rule_based": {
    "flagged": true,
    "severity": "high",
    "reason": "Contains banned keyword: hate",
    "method": "rule_based"
  },
  "api_based": {
    "flagged": true,
    "categories": {
      "harassment": true,
      "hate": false
    },
    "confidence": 0.85
  },
  "final_decision": {
    "action": "block",
    "reason": "Both systems flagged content",
    "confidence": "high"
  }
}
```

This exercise provides hands-on experience with real content moderation challenges while keeping the implementation manageable and educational.
