"""
Simple Task Planning System
A basic AI planning system that breaks down goals into subtasks and executes them.
"""

import os
import time
from typing import List, Dict
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class SimplePlanner:
    """
    A simple AI planning system that can decompose goals into subtasks
    and execute them sequentially.
    """
    
    def __init__(self):
        """Initialize the planner with OpenRouter API configuration."""
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENROUTER_API_KEY'),
            base_url="https://openrouter.ai/api/v1"
        )
        self.subtasks = []
        self.completed_tasks = []
        self.current_goal = ""
    
    def decompose_goal(self, goal: str) -> List[str]:
        """
        Break down a high-level goal into subtasks using OpenRouter API.
        
        Args:
            goal (str): The main goal to decompose
            
        Returns:
            List[str]: List of subtasks
        """
        print(f"🎯 Goal: {goal}")
        print("\n🔍 Decomposing goal into subtasks...")
        
        self.current_goal = goal
        
        # Create prompt for task decomposition
        prompt = f"""
You are an expert AI planner. Break down the following goal into 5-7 specific, actionable subtasks.

Goal: {goal}

Requirements:
- Create exactly 5-7 subtasks
- Make each subtask specific and actionable
- Order them logically (most important first)
- Use clear, concise language
- Number each subtask (1., 2., 3., etc.)

Format your response as a numbered list only, no additional text.
"""
        
        try:
            # Call OpenRouter API for task decomposition
            response = self.client.chat.completions.create(
                model="mistralai/mistral-small-3.2-24b-instruct:free",
                messages=[
                    {"role": "system", "content": "You are an expert task planner and project manager."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Extract the plan from the response
            plan_text = response.choices[0].message.content.strip()
            
            # Parse the numbered list into subtasks
            self.subtasks = []
            for line in plan_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.') or line.startswith('6.') or line.startswith('7.')):
                    # Remove numbering and clean up
                    task = line.split('.', 1)[1].strip() if '.' in line else line
                    if task:
                        self.subtasks.append(task)
            
            # If parsing failed, create a simple fallback plan
            if not self.subtasks:
                self.subtasks = [
                    "Research and gather information",
                    "Create initial plan",
                    "Execute first steps",
                    "Monitor progress",
                    "Complete final tasks"
                ]
            
            print("📋 Generated Plan:")
            for i, task in enumerate(self.subtasks, 1):
                print(f"{i}. {task}")
            
            return self.subtasks
            
        except Exception as e:
            print(f"❌ Error during goal decomposition: {e}")
            # Fallback plan
            self.subtasks = [
                "Research and gather information",
                "Create initial plan", 
                "Execute first steps",
                "Monitor progress",
                "Complete final tasks"
            ]
            return self.subtasks
    
    def execute_plan(self) -> bool:
        """
        Execute all subtasks in sequence.
        
        Returns:
            bool: True if all tasks completed successfully
        """
        if not self.subtasks:
            print("❌ No plan to execute. Please decompose a goal first.")
            return False
        
        print(f"\n🚀 Executing Plan:")
        print("=" * 50)
        
        for i, task in enumerate(self.subtasks, 1):
            print(f"\n📝 Task {i}/{len(self.subtasks)}: {task}")
            
            # Simulate task execution
            success = self._execute_task(task)
            
            if success:
                print(f"✅ Executing: {task}")
                self.completed_tasks.append(task)
                time.sleep(0.5)  # Small delay for visual effect
            else:
                print(f"❌ Failed to execute: {task}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 Plan completed successfully!")
        return True
    
    def _execute_task(self, task: str) -> bool:
        """
        Simulate executing a single task.
        
        Args:
            task (str): The task to execute
            
        Returns:
            bool: True if task executed successfully
        """
        # Simulate different types of tasks
        if "research" in task.lower() or "gather" in task.lower():
            time.sleep(0.3)
        elif "create" in task.lower() or "plan" in task.lower():
            time.sleep(0.4)
        elif "execute" in task.lower() or "implement" in task.lower():
            time.sleep(0.5)
        elif "monitor" in task.lower() or "track" in task.lower():
            time.sleep(0.2)
        else:
            time.sleep(0.3)
        
        # Simulate 95% success rate
        return True
    
    def track_progress(self) -> Dict:
        """
        Track the progress of plan execution.
        
        Returns:
            Dict: Progress information
        """
        total_tasks = len(self.subtasks)
        completed_tasks = len(self.completed_tasks)
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        progress_info = {
            "goal": self.current_goal,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "remaining_tasks": total_tasks - completed_tasks,
            "progress_percentage": progress_percentage,
            "completed_list": self.completed_tasks.copy(),
            "remaining_list": [task for task in self.subtasks if task not in self.completed_tasks]
        }
        
        print(f"\n📊 Progress Report:")
        print(f"   Goal: {progress_info['goal']}")
        print(f"   Completed: {progress_info['completed_tasks']}/{progress_info['total_tasks']} tasks")
        print(f"   Progress: {progress_info['progress_percentage']:.1f}%")
        
        if progress_info['remaining_list']:
            print(f"   Remaining: {', '.join(progress_info['remaining_list'])}")
        
        return progress_info


def main():
    """Main function to demonstrate the SimplePlanner."""
    print("🤖 Simple Task Planning System")
    print("=" * 40)
    
    # Create planner instance
    planner = SimplePlanner()
    
    # Define the goal
    goal = "Plan a weekend trip to Barcelona"
    
    # Step 1: Decompose the goal
    subtasks = planner.decompose_goal(goal)
    
    # Step 2: Execute the plan
    success = planner.execute_plan()
    
    # Step 3: Track progress
    if success:
        progress = planner.track_progress()
        print(f"\n🎯 Final Status: {progress['progress_percentage']:.1f}% Complete")


if __name__ == "__main__":
    main()
