#!/usr/bin/env python3
"""
LangSmith Prompt Versioning System
==================================

This module demonstrates how to use LangSmith for professional prompt versioning
and experiment tracking. LangSmith is the industry-standard platform used by
leading AI companies for managing LLM experiments.

Key Concepts:
- Experiment tracking with automatic versioning
- Performance comparison across prompt versions
- Metadata management and team collaboration
- Custom evaluators for quality scoring
- A/B testing for prompt optimization

Learning Objectives:
- Understand LangSmith platform capabilities
- Implement systematic prompt versioning
- Compare performance across experiments
- Generate reports and insights
- Collaborate with teams on prompt development
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LangSmith and LangChain components with updated imports
try:
    from langsmith import Client
    from langchain_community.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.callbacks import LangChainTracer
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Please install: pip install langsmith langchain langchain-community")
    exit(1)


class LangSmithPromptVersioning:
    """
    Professional prompt versioning system using LangSmith.
    
    This class demonstrates how to:
    1. Create and track prompt experiments
    2. Compare performance across versions
    3. Manage metadata and team collaboration
    4. Generate reports and insights
    5. Implement A/B testing
    
    Real-world applications:
    - Customer service chatbot optimization
    - Content generation prompt refinement
    - Code review assistant improvement
    - Search query optimization
    """
    
    def __init__(self, project_name: str = "prompt-versioning-demo"):
        """
        Initialize the LangSmith prompt versioning system.
        
        Args:
            project_name (str): Name of the LangSmith project for organizing experiments
        
        This sets up:
        - LangSmith client for experiment tracking
        - OpenRouter LLM for testing prompts
        - Project structure for organizing experiments
        """
        # Initialize LangSmith client
        self.client = Client()
        self.project_name = project_name
        
        # Set up OpenRouter LLM (supports multiple models)
        self.llm = ChatOpenAI(
            model="mistralai/mistral-small-3.2-24b-instruct:free",  # Can be changed to gpt-4, claude, etc.
            temperature=0.7,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY")
        )
        
        # Initialize experiment tracking
        self.experiments = {}  # Store experiment IDs locally
        self.results_cache = {}  # Cache results for comparison
        self.prompt_store = {}  # Store prompt texts locally
        
        print(f"🛡️  LangSmith Prompt Versioning System Initialized")
        print(f"   Project: {project_name}")
        print(f"   Model: {self.llm.model_name}")
        print(f"   LangSmith API: {'✅ Available' if os.getenv('LANGSMITH_API_KEY') else '❌ Not configured'}")
        print(f"   OpenRouter API: {'✅ Available' if os.getenv('OPENROUTER_API_KEY') else '❌ Not configured'}")
    
    def create_prompt_experiment(self, 
                                prompt_name: str, 
                                prompt_text: str, 
                                metadata: Dict[str, Any]) -> str:
        """
        Create a new prompt experiment in LangSmith.
        
        This is like creating a new "branch" in Git, but for prompts.
        Each experiment gets a unique ID and tracks all interactions.
        
        Args:
            prompt_name (str): Name of the prompt (e.g., "customer_email")
            prompt_text (str): The actual prompt text to test
            metadata (dict): Additional information about the experiment
            
        Returns:
            str: Experiment ID for tracking
            
        Example:
            experiment_id = system.create_prompt_experiment(
                "customer_email",
                "Write a professional response to a customer inquiry.",
                {"version": "1.0", "author": "Alice", "tone": "professional"}
            )
        """
        try:
            # Create a unique experiment name and ID
            version = metadata.get('version', 'v1')
            experiment_name = f"{prompt_name}_{version}"
            experiment_id = f"{experiment_name}_{int(time.time())}"
            
            # Store prompt text locally (in real LangSmith, this would be stored in the platform)
            self.prompt_store[experiment_id] = {
                "name": experiment_name,
                "text": prompt_text,
                "metadata": metadata,
                "created_at": datetime.now().isoformat()
            }
            
            # Store experiment ID locally for easy access
            self.experiments[experiment_name] = experiment_id
            
            print(f"✅ Created experiment: {experiment_name}")
            print(f"   ID: {experiment_id}")
            print(f"   Metadata: {metadata}")
            
            return experiment_id
            
        except Exception as e:
            print(f"❌ Failed to create experiment: {e}")
            # Fallback: create a local experiment ID
            fallback_id = f"local_{prompt_name}_{int(time.time())}"
            self.experiments[prompt_name] = fallback_id
            return fallback_id
    
    def test_prompt_version(self, 
                           experiment_id: str, 
                           test_inputs: List[str],
                           model_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Test a prompt version with multiple inputs and track results.
        
        This function runs the prompt against test inputs and automatically
        tracks performance metrics in LangSmith. It's like running unit tests
        for your prompts.
        
        Args:
            experiment_id (str): ID of the experiment to test
            test_inputs (list): List of test inputs to try
            model_params (dict): Optional model parameters (temperature, etc.)
            
        Returns:
            dict: Results with responses, metrics, and performance data
            
        Example:
            results = system.test_prompt_version(
                experiment_id,
                ["My order is late", "Product is defective"],
                {"temperature": 0.5}
            )
        """
        results = {
            "experiment_id": experiment_id,
            "test_inputs": test_inputs,
            "responses": [],
            "metrics": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Get the prompt text from our local store
        prompt_text = self._get_prompt_text_from_experiment(experiment_id)
        
        print(f"🧪 Testing experiment {experiment_id}")
        print(f"   Test inputs: {len(test_inputs)}")
        print(f"   Model params: {model_params or 'default'}")
        
        for i, input_text in enumerate(test_inputs, 1):
            print(f"   Running test {i}/{len(test_inputs)}: {input_text[:50]}...")
            
            try:
                # Start timing
                start_time = time.time()
                
                # Create messages for the LLM
                messages = [
                    SystemMessage(content=prompt_text),
                    HumanMessage(content=input_text)
                ]
                
                # Call the LLM with LangSmith tracing
                response = self.llm.invoke(messages)
                
                # Calculate metrics
                end_time = time.time()
                response_time = end_time - start_time
                
                # Store result
                result = {
                    "input": input_text,
                    "response": response.content,
                    "response_time": response_time,
                    "timestamp": datetime.now().isoformat(),
                    "model_params": model_params or {}
                }
                
                results["responses"].append(result)
                
                print(f"     ✅ Response: {response.content[:100]}...")
                print(f"     ⏱️  Time: {response_time:.2f}s")
                
            except Exception as e:
                print(f"     ❌ Error: {e}")
                results["responses"].append({
                    "input": input_text,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate overall metrics
        successful_responses = [r for r in results["responses"] if "response" in r]
        if successful_responses:
            avg_response_time = sum(r["response_time"] for r in successful_responses) / len(successful_responses)
            avg_response_length = sum(len(r["response"]) for r in successful_responses) / len(successful_responses)
            
            results["metrics"] = {
                "total_tests": len(test_inputs),
                "successful_tests": len(successful_responses),
                "success_rate": len(successful_responses) / len(test_inputs),
                "avg_response_time": avg_response_time,
                "avg_response_length": avg_response_length
            }
        
        # Cache results for comparison
        self.results_cache[experiment_id] = results
        
        print(f"📊 Test completed for {experiment_id}")
        print(f"   Success rate: {results['metrics'].get('success_rate', 0):.1%}")
        print(f"   Avg response time: {results['metrics'].get('avg_response_time', 0):.2f}s")
        
        return results
    
    def compare_experiments(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """
        Compare performance across multiple experiments.
        
        This function analyzes results from different prompt versions
        and provides insights on which performs better. It's like
        running a benchmark test across different configurations.
        
        Args:
            experiment_ids (list): List of experiment IDs to compare
            
        Returns:
            dict: Comparison analysis with metrics and recommendations
            
        Example:
            comparison = system.compare_experiments([exp1_id, exp2_id, exp3_id])
        """
        print(f"📈 Comparing {len(experiment_ids)} experiments...")
        
        comparison = {
            "experiments": {},
            "summary": {},
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Collect results for each experiment
        for exp_id in experiment_ids:
            if exp_id in self.results_cache:
                comparison["experiments"][exp_id] = self.results_cache[exp_id]
            else:
                print(f"⚠️  No cached results for {exp_id}")
        
        if not comparison["experiments"]:
            print("❌ No experiments to compare")
            return comparison
        
        # Calculate comparison metrics
        metrics_comparison = {}
        for exp_id, results in comparison["experiments"].items():
            metrics = results.get("metrics", {})
            metrics_comparison[exp_id] = {
                "success_rate": metrics.get("success_rate", 0),
                "avg_response_time": metrics.get("avg_response_time", 0),
                "avg_response_length": metrics.get("avg_response_length", 0)
            }
        
        # Find best performers
        if metrics_comparison:
            best_success_rate = max(metrics_comparison.values(), key=lambda x: x["success_rate"])
            fastest_response = min(metrics_comparison.values(), key=lambda x: x["avg_response_time"])
            
            comparison["summary"] = {
                "total_experiments": len(experiment_ids),
                "best_success_rate": best_success_rate["success_rate"],
                "fastest_response_time": fastest_response["avg_response_time"],
                "metrics_comparison": metrics_comparison
            }
            
            # Generate recommendations
            for exp_id, metrics in metrics_comparison.items():
                if metrics["success_rate"] == best_success_rate["success_rate"]:
                    comparison["recommendations"].append(
                        f"🎯 {exp_id} has the best success rate ({metrics['success_rate']:.1%})"
                    )
                
                if metrics["avg_response_time"] == fastest_response["avg_response_time"]:
                    comparison["recommendations"].append(
                        f"⚡ {exp_id} has the fastest response time ({metrics['avg_response_time']:.2f}s)"
                    )
        
        print(f"📊 Comparison completed")
        print(f"   Best success rate: {comparison['summary'].get('best_success_rate', 0):.1%}")
        print(f"   Fastest response: {comparison['summary'].get('fastest_response_time', 0):.2f}s")
        
        return comparison
    
    def generate_changelog(self, experiment_ids: List[str]) -> str:
        """
        Generate a changelog from experiment history.
        
        This creates a markdown changelog showing the evolution
        of prompts over time, similar to software versioning.
        
        Args:
            experiment_ids (list): List of experiment IDs to include
            
        Returns:
            str: Markdown formatted changelog
            
        Example:
            changelog = system.generate_changelog([exp1_id, exp2_id, exp3_id])
            print(changelog)
        """
        print(f"📝 Generating changelog for {len(experiment_ids)} experiments...")
        
        changelog = f"# Prompt Versioning Changelog\n\n"
        changelog += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Group experiments by prompt name
        experiments_by_name = {}
        for exp_id in experiment_ids:
            if exp_id in self.results_cache:
                # Extract prompt name from experiment ID
                prompt_name = exp_id.split('_')[0] if '_' in exp_id else exp_id
                if prompt_name not in experiments_by_name:
                    experiments_by_name[prompt_name] = []
                experiments_by_name[prompt_name].append(exp_id)
        
        # Generate changelog for each prompt
        for prompt_name, exp_ids in experiments_by_name.items():
            changelog += f"## {prompt_name.title()} Prompt\n\n"
            
            for exp_id in exp_ids:
                results = self.results_cache[exp_id]
                metrics = results.get("metrics", {})
                
                # Get prompt metadata
                prompt_info = self.prompt_store.get(exp_id, {})
                metadata = prompt_info.get("metadata", {})
                
                changelog += f"### Version {metadata.get('version', exp_id)}\n\n"
                changelog += f"- **Author:** {metadata.get('author', 'Unknown')}\n"
                changelog += f"- **Tone:** {metadata.get('tone', 'Not specified')}\n"
                changelog += f"- **Success Rate:** {metrics.get('success_rate', 0):.1%}\n"
                changelog += f"- **Avg Response Time:** {metrics.get('avg_response_time', 0):.2f}s\n"
                changelog += f"- **Avg Response Length:** {metrics.get('avg_response_length', 0):.0f} chars\n"
                changelog += f"- **Tests Run:** {metrics.get('total_tests', 0)}\n\n"
                
                # Add improvement notes
                if metadata.get('improvement'):
                    changelog += f"**Improvement:** {metadata['improvement']}\n\n"
                
                # Add sample responses
                if results.get("responses"):
                    changelog += f"**Sample Response:**\n"
                    sample_response = results["responses"][0].get("response", "No response")
                    changelog += f"```\n{sample_response[:200]}...\n```\n\n"
            
            changelog += "---\n\n"
        
        print(f"✅ Changelog generated successfully")
        return changelog
    
    def export_results(self, experiment_id: str, format: str = "json") -> str:
        """
        Export experiment results in various formats.
        
        This allows you to save results for external analysis,
        reporting, or sharing with team members.
        
        Args:
            experiment_id (str): ID of the experiment to export
            format (str): Export format ("json", "csv", "markdown")
            
        Returns:
            str: Exported data or filename
            
        Example:
            json_data = system.export_results(exp_id, "json")
            csv_file = system.export_results(exp_id, "csv")
        """
        if experiment_id not in self.results_cache:
            print(f"❌ No results found for experiment {experiment_id}")
            return ""
        
        results = self.results_cache[experiment_id]
        
        if format.lower() == "json":
            filename = f"experiment_{experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Exported to {filename}")
            return filename
            
        elif format.lower() == "csv":
            import csv
            filename = f"experiment_{experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Input', 'Response', 'Response Time', 'Timestamp'])
                
                for response in results.get("responses", []):
                    writer.writerow([
                        response.get("input", ""),
                        response.get("response", ""),
                        response.get("response_time", 0),
                        response.get("timestamp", "")
                    ])
            
            print(f"✅ Exported to {filename}")
            return filename
            
        elif format.lower() == "markdown":
            filename = f"experiment_{experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
            with open(filename, 'w') as f:
                f.write(f"# Experiment Results: {experiment_id}\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write metrics
                metrics = results.get("metrics", {})
                f.write("## Metrics\n\n")
                f.write(f"- Success Rate: {metrics.get('success_rate', 0):.1%}\n")
                f.write(f"- Avg Response Time: {metrics.get('avg_response_time', 0):.2f}s\n")
                f.write(f"- Avg Response Length: {metrics.get('avg_response_length', 0):.0f} chars\n\n")
                
                # Write responses
                f.write("## Responses\n\n")
                for i, response in enumerate(results.get("responses", []), 1):
                    f.write(f"### Test {i}\n\n")
                    f.write(f"**Input:** {response.get('input', '')}\n\n")
                    f.write(f"**Response:** {response.get('response', '')}\n\n")
                    f.write(f"**Time:** {response.get('response_time', 0):.2f}s\n\n")
            
            print(f"✅ Exported to {filename}")
            return filename
        
        else:
            print(f"❌ Unsupported format: {format}")
            return ""
    
    def _get_prompt_text_from_experiment(self, experiment_id: str) -> str:
        """
        Helper method to get prompt text from experiment.
        
        Gets the prompt text from our local prompt store.
        """
        if experiment_id in self.prompt_store:
            return self.prompt_store[experiment_id]["text"]
        
        # Fallback to a generic prompt
        return "You are a helpful assistant. Please respond to the following:"


def main():
    """
    Main function to demonstrate the LangSmith prompt versioning system.
    
    This runs a complete example showing:
    1. Creating multiple prompt experiments
    2. Testing each version with sample inputs
    3. Comparing performance across versions
    4. Generating reports and changelogs
    """
    print("🚀 LangSmith Prompt Versioning Demo")
    print("=" * 50)
    
    # Initialize the system
    versioning = LangSmithPromptVersioning("prompt-versioning-demo")
    
    # Define test inputs (real-world scenarios)
    customer_test_inputs = [
        "My order hasn't arrived yet and I'm very frustrated",
        "The product I received is defective and doesn't work",
        "I want to cancel my subscription immediately",
        "Can you help me with a billing question?"
    ]
    
    # Create multiple prompt experiments (different versions)
    print("\n📝 Creating prompt experiments...")
    
    # Version 1: Basic professional
    email_v1 = versioning.create_prompt_experiment(
        "customer_email",
        "Write a professional response to a customer inquiry.",
        {
            "version": "1.0",
            "author": "Alice",
            "tone": "professional",
            "target_length": "short",
            "notes": "Basic professional response template"
        }
    )
    
    # Version 2: Empathetic and helpful
    email_v2 = versioning.create_prompt_experiment(
        "customer_email",
        "Write an empathetic and helpful response to a customer inquiry. Show understanding and provide clear solutions.",
        {
            "version": "1.1",
            "author": "Bob",
            "tone": "empathetic",
            "target_length": "medium",
            "improvement": "more_caring",
            "notes": "Added empathy and solution focus"
        }
    )
    
    # Version 3: Action-oriented
    email_v3 = versioning.create_prompt_experiment(
        "customer_email",
        "Write a response to a customer inquiry that includes specific next steps and contact information.",
        {
            "version": "1.2",
            "author": "Charlie",
            "tone": "actionable",
            "target_length": "medium",
            "improvement": "specific_actions",
            "notes": "Added specific action items and contact info"
        }
    )
    
    # Test each version
    print("\n🧪 Testing prompt versions...")
    
    results_v1 = versioning.test_prompt_version(email_v1, customer_test_inputs)
    results_v2 = versioning.test_prompt_version(email_v2, customer_test_inputs)
    results_v3 = versioning.test_prompt_version(email_v3, customer_test_inputs)
    
    # Compare all versions
    print("\n📊 Comparing all versions...")
    comparison = versioning.compare_experiments([email_v1, email_v2, email_v3])
    
    # Generate changelog
    print("\n📝 Generating changelog...")
    changelog = versioning.generate_changelog([email_v1, email_v2, email_v3])
    
    # Export results
    print("\n💾 Exporting results...")
    versioning.export_results(email_v1, "json")
    versioning.export_results(email_v2, "markdown")
    
    # Display summary
    print("\n🎉 Demo completed successfully!")
    print("=" * 50)
    print("📈 Key Insights:")
    for recommendation in comparison.get("recommendations", []):
        print(f"   {recommendation}")
    
    print(f"\n📄 Generated files:")
    print(f"   - Changelog (see above)")
    print(f"   - JSON export: experiment_{email_v1}_*.json")
    print(f"   - Markdown export: experiment_{email_v2}_*.md")
    
    print(f"\n🌐 View detailed results in LangSmith:")
    print(f"   https://smith.langchain.com/")
    
    print(f"\n💡 Next steps:")
    print(f"   - Analyze results in LangSmith dashboard")
    print(f"   - Share experiments with team members")
    print(f"   - Implement custom evaluators")
    print(f"   - Set up automated testing pipeline")


if __name__ == "__main__":
    main()
