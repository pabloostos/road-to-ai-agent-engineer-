# Learning Templates
# Week 1 - Road to AI Agent Engineer

from typing import Dict, Any, List, Callable

class ExerciseFramework:
    def __init__(self, exercise_name: str):
        self.exercise_name = exercise_name
        self.steps = []
        self.results = {}
    
    def add_step(self, step_name: str, step_func: Callable):
        """Add a step to the exercise."""
        self.steps.append({
            "name": step_name,
            "function": step_func
        })
    
    def run_exercise(self, input_data: Any = None):
        """Run the complete exercise."""
        print(f"Running Exercise: {self.exercise_name}")
        print("=" * 50)
        
        for i, step in enumerate(self.steps, 1):
            print(f"\nStep {i}: {step['name']}")
            print("-" * 30)
            
            try:
                result = step['function'](input_data)
                self.results[step['name']] = result
                print(f"✅ {step['name']} completed successfully")
            except Exception as e:
                print(f"❌ {step['name']} failed: {e}")
                self.results[step['name']] = {"error": str(e)}
        
        return self.results

def create_practice_scenario(scenario_name: str, description: str, tasks: List[str]):
    """Create a practice scenario."""
    return {
        "name": scenario_name,
        "description": description,
        "tasks": tasks,
        "completed": False
    }

def create_test_framework(test_name: str, test_cases: List[Dict[str, Any]]):
    """Create a test framework."""
    def run_tests():
        results = {
            "test_name": test_name,
            "total_tests": len(test_cases),
            "passed": 0,
            "failed": 0,
            "results": []
        }
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Running test {i}: {test_case['name']}")
            
            try:
                result = test_case['test']()
                if result:
                    results["passed"] += 1
                    print(f"✅ Test {i} passed")
                else:
                    results["failed"] += 1
                    print(f"❌ Test {i} failed")
            except Exception as e:
                results["failed"] += 1
                print(f"❌ Test {i} failed with error: {e}")
            
            results["results"].append({
                "test_case": test_case['name'],
                "passed": result if 'result' not in locals() else result
            })
        
        return results
    
    return run_tests

def create_evaluation_metrics():
    """Create evaluation metrics."""
    return {
        "accuracy": 0.0,
        "response_time": 0.0,
        "success_rate": 0.0,
        "error_rate": 0.0
    }

def create_progress_tracker():
    """Create a progress tracker."""
    return {
        "completed_exercises": [],
        "current_exercise": None,
        "total_exercises": 0,
        "progress_percentage": 0.0
    } 