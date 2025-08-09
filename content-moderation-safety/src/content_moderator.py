#!/usr/bin/env python3
"""
Content Moderation System

This script implements a comprehensive content moderation system that combines:
1. Rule-based keyword filtering (fast, deterministic)
2. OpenAI Moderation API (context-aware, AI-powered)
3. Combined decision pipeline (best of both approaches)
4. Comprehensive logging and analysis

Exercise components:
- Multi-layer content safety filtering
- Performance analysis and metrics
- Real-world test cases
- Production-ready logging
"""

import requests
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class ContentModerator:
    """
    A comprehensive content moderation system combining multiple approaches.
    
    Features:
    - Rule-based keyword filtering for fast detection
    - OpenAI Moderation API for context-aware analysis
    - Combined decision making with confidence scoring
    - Comprehensive logging and audit trails
    """
    
    def __init__(self):
        """Initialize the content moderator with API keys and filter lists."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Rule-based filters - organized by severity
        self.banned_keywords = [
            # High severity - immediate block
            "kill", "murder", "suicide", "bomb", "weapon", "terrorist",
            "hate", "die", "death", "violence", "harm"
        ]
        
        self.suspicious_keywords = [
            # Medium severity - flag for review
            "drug", "illegal", "scam", "fraud", "steal", "cheat",
            "stupid", "idiot", "moron", "loser"
        ]
        
        self.mild_concern_keywords = [
            # Low severity - monitor
            "angry", "annoyed", "frustrated", "upset", "disappointed"
        ]
        
        print("🛡️  Content Moderator initialized")
        print(f"   Rule-based filters: {len(self.banned_keywords + self.suspicious_keywords + self.mild_concern_keywords)} keywords")
        print(f"   OpenAI API: {'✅ Available' if self.openai_api_key else '❌ Not configured'}")
    
    def rule_based_filter(self, text: str) -> Dict[str, Any]:
        """
        Implement rule-based keyword filtering.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Analysis results with flagging decision
        """
        text_lower = text.lower()
        flagged_keywords = []
        severity = "none"
        
        # Check for banned content (high severity)
        for keyword in self.banned_keywords:
            if keyword in text_lower:
                flagged_keywords.append(keyword)
                severity = "high"
        
        # Check for suspicious content (medium severity) - only if not already high
        if severity != "high":
            for keyword in self.suspicious_keywords:
                if keyword in text_lower:
                    flagged_keywords.append(keyword)
                    severity = "medium"
        
        # Check for mild concerns (low severity) - only if not already flagged
        if severity == "none":
            for keyword in self.mild_concern_keywords:
                if keyword in text_lower:
                    flagged_keywords.append(keyword)
                    severity = "low"
        
        # Determine if content should be flagged
        flagged = severity in ["high", "medium"]
        
        return {
            "flagged": flagged,
            "severity": severity,
            "reason": f"Contains keywords: {', '.join(flagged_keywords)}" if flagged_keywords else "No keywords detected",
            "keywords_found": flagged_keywords,
            "method": "rule_based",
            "confidence": 0.9 if severity == "high" else (0.7 if severity == "medium" else 0.3)
        }
    
    def api_moderation_check(self, text: str) -> Dict[str, Any]:
        """
        Use OpenAI Moderation API for context-aware analysis.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: API analysis results
        """
        if not self.openai_api_key:
            return {
                "error": "OpenAI API key not configured",
                "flagged": False,
                "method": "api_based"
            }
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "omni-moderation-latest",
            "input": text
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/moderations",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                moderation_result = result["results"][0]
                
                # Extract categories that are flagged
                flagged_categories = [
                    category for category, flagged in moderation_result["categories"].items()
                    if flagged
                ]
                
                # Calculate overall confidence (average of category scores)
                category_scores = moderation_result.get("category_scores", {})
                confidence = max(category_scores.values()) if category_scores else 0.5
                
                return {
                    "flagged": moderation_result["flagged"],
                    "categories": moderation_result["categories"],
                    "category_scores": category_scores,
                    "flagged_categories": flagged_categories,
                    "confidence": confidence,
                    "method": "api_based"
                }
            else:
                return {
                    "error": f"API error {response.status_code}: {response.text}",
                    "flagged": False,
                    "method": "api_based"
                }
                
        except Exception as e:
            return {
                "error": f"API request failed: {e}",
                "flagged": False,
                "method": "api_based"
            }
    
    def moderate_content(self, text: str) -> Dict[str, Any]:
        """
        Complete moderation pipeline combining all approaches.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Complete analysis with final decision
        """
        print(f"\n🔍 Moderating content: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # Run both moderation approaches
        rule_result = self.rule_based_filter(text)
        api_result = self.api_moderation_check(text)
        
        # Combine results to make final decision
        final_decision = self._make_final_decision(rule_result, api_result)
        
        # Create comprehensive log entry
        result = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "rule_based": rule_result,
            "api_based": api_result,
            "final_decision": final_decision,
            "processing_time": datetime.now().isoformat()
        }
        
        # Display results
        self._display_results(result)
        
        return result
    
    def _make_final_decision(self, rule_result: Dict[str, Any], api_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine rule-based and API results to make final moderation decision.
        
        Args:
            rule_result (dict): Rule-based analysis results
            api_result (dict): API analysis results
            
        Returns:
            dict: Final decision with action and reasoning
        """
        # If either system has an error, use the working one
        if "error" in rule_result and "error" in api_result:
            return {
                "action": "manual_review",
                "reason": "Both systems failed - requires manual review",
                "confidence": "low"
            }
        elif "error" in api_result:
            # Use rule-based only
            return {
                "action": "block" if rule_result["flagged"] else "allow",
                "reason": f"API unavailable, rule-based decision: {rule_result['reason']}",
                "confidence": "medium" if rule_result["flagged"] else "high"
            }
        elif "error" in rule_result:
            # Use API only
            return {
                "action": "block" if api_result["flagged"] else "allow",
                "reason": f"Rule-based unavailable, API decision based on: {api_result.get('flagged_categories', [])}",
                "confidence": "high" if api_result["confidence"] > 0.8 else "medium"
            }
        
        # Both systems working - combine decisions
        rule_flagged = rule_result["flagged"]
        api_flagged = api_result["flagged"]
        
        if rule_flagged and api_flagged:
            # Both systems agree - block
            return {
                "action": "block",
                "reason": f"Both systems flagged: {rule_result['reason']} + API categories: {api_result.get('flagged_categories', [])}",
                "confidence": "high"
            }
        elif rule_flagged or api_flagged:
            # One system flagged - depends on severity and confidence
            if rule_result.get("severity") == "high" or api_result.get("confidence", 0) > 0.8:
                return {
                    "action": "block",
                    "reason": f"High confidence flag from {'rules' if rule_flagged else 'API'}",
                    "confidence": "high"
                }
            else:
                return {
                    "action": "flag_for_review",
                    "reason": f"Medium confidence flag from {'rules' if rule_flagged else 'API'}",
                    "confidence": "medium"
                }
        else:
            # Neither system flagged - allow
            return {
                "action": "allow",
                "reason": "Both systems cleared content",
                "confidence": "high"
            }
    
    def _display_results(self, result: Dict[str, Any]) -> None:
        """Display moderation results in a clear format."""
        rule = result["rule_based"]
        api = result["api_based"]
        decision = result["final_decision"]
        
        print(f"📊 Moderation Results:")
        print(f"   Rule-based: {'🚫' if rule['flagged'] else '✅'} {rule['severity']} severity")
        if rule.get("keywords_found"):
            print(f"              Keywords: {', '.join(rule['keywords_found'])}")
        
        if "error" not in api:
            print(f"   API-based:  {'🚫' if api['flagged'] else '✅'} confidence: {api.get('confidence', 0):.2f}")
            if api.get("flagged_categories"):
                print(f"              Categories: {', '.join(api['flagged_categories'])}")
        else:
            print(f"   API-based:  ❌ Error: {api['error'][:50]}...")
        
        action_emoji = {"allow": "✅", "block": "🚫", "flag_for_review": "⚠️", "manual_review": "👤"}
        print(f"   Decision:   {action_emoji.get(decision['action'], '❓')} {decision['action'].upper()}")
        print(f"              {decision['reason']}")
    
    def log_results(self, results: List[Dict[str, Any]], filename: str = "moderation_log.json") -> None:
        """
        Save moderation results to JSON log file.
        
        Args:
            results (list): List of moderation results
            filename (str): Log file name
        """
        try:
            with open(filename, "w") as f:
                for result in results:
                    f.write(json.dumps(result) + "\n")
            
            print(f"\n📄 Results logged to {filename}")
            print(f"   Total entries: {len(results)}")
            
        except Exception as e:
            print(f"❌ Failed to save log: {e}")
    
    def analyze_performance(self, results: List[Dict[str, Any]]) -> None:
        """
        Analyze moderation performance and generate statistics.
        
        Args:
            results (list): List of moderation results
        """
        if not results:
            print("No results to analyze")
            return
        
        print(f"\n📈 Performance Analysis:")
        print(f"=" * 40)
        
        # Basic statistics
        total_tests = len(results)
        blocked = sum(1 for r in results if r["final_decision"]["action"] == "block")
        allowed = sum(1 for r in results if r["final_decision"]["action"] == "allow")
        flagged = sum(1 for r in results if r["final_decision"]["action"] == "flag_for_review")
        
        print(f"Total tests: {total_tests}")
        print(f"Blocked: {blocked} ({blocked/total_tests*100:.1f}%)")
        print(f"Allowed: {allowed} ({allowed/total_tests*100:.1f}%)")
        print(f"Flagged for review: {flagged} ({flagged/total_tests*100:.1f}%)")
        
        # System agreement analysis
        both_working = [r for r in results if "error" not in r["rule_based"] and "error" not in r["api_based"]]
        if both_working:
            agreement = sum(1 for r in both_working 
                          if r["rule_based"]["flagged"] == r["api_based"]["flagged"])
            print(f"\nSystem Agreement: {agreement}/{len(both_working)} ({agreement/len(both_working)*100:.1f}%)")
        
        # Confidence distribution
        high_conf = sum(1 for r in results if r["final_decision"]["confidence"] == "high")
        med_conf = sum(1 for r in results if r["final_decision"]["confidence"] == "medium")
        low_conf = sum(1 for r in results if r["final_decision"]["confidence"] == "low")
        
        print(f"\nConfidence Distribution:")
        print(f"  High: {high_conf} ({high_conf/total_tests*100:.1f}%)")
        print(f"  Medium: {med_conf} ({med_conf/total_tests*100:.1f}%)")
        print(f"  Low: {low_conf} ({low_conf/total_tests*100:.1f}%)")

def main():
    """
    Main function to run the content moderation exercise.
    """
    print("🛡️  Content Moderation & Safety Filters Exercise")
    print("=" * 55)
    
    # Initialize moderator
    moderator = ContentModerator()
    
    # Test cases covering different types of content
    test_cases = [
        # Safe content
        "Hello, how are you today?",
        "I love learning about artificial intelligence!",
        "This product is amazing and works perfectly.",
        "Can you help me with my homework?",
        
        # Mild toxicity
        "I hate this stupid system",
        "This is so annoying and frustrating",
        "You're being really dumb about this",
        
        # Concerning content
        "I want to build a weapon",
        "How to make illegal drugs",
        "This is a scam to steal your money",
        
        # Dangerous content
        "I want to hurt myself",
        "How to build a bomb",
        "You should kill yourself",
        "I will murder you",
        
        # Context-dependent
        "I'll shoot you an email later",  # Photography/email context
        "This movie bombed at the box office",  # Entertainment context
        "I'm dying to see the new movie",  # Expression context
    ]
    
    print(f"\n🧪 Testing with {len(test_cases)} content samples...")
    
    # Process all test cases
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/{len(test_cases)} ---")
        result = moderator.moderate_content(test_case)
        results.append(result)
    
    # Log results
    moderator.log_results(results)
    
    # Analyze performance
    moderator.analyze_performance(results)
    
    print(f"\n🎉 Content Moderation Exercise Completed!")
    print(f"💡 Key learnings:")
    print(f"   - Multi-layer defense provides better coverage")
    print(f"   - Context matters: same words can be safe or harmful")
    print(f"   - Combining approaches balances speed and accuracy")
    print(f"   - Confidence scoring helps with edge cases")
    print(f"   - Comprehensive logging enables system improvement")

if __name__ == "__main__":
    main()
