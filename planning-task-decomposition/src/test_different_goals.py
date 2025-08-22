"""
Test Different Goals with SimplePlanner
Demonstrates the planner with various types of goals.
"""

from simple_planner import SimplePlanner

def test_different_goals():
    """Test the planner with different types of goals."""
    
    # Create planner instance
    planner = SimplePlanner()
    
    # Test goals
    test_goals = [
        "Launch a digital marketing campaign for a new product",
        "Organize a team building event",
        "Create a personal fitness plan",
        "Plan a home renovation project"
    ]
    
    print("🧪 Testing Different Goals with SimplePlanner")
    print("=" * 60)
    
    for i, goal in enumerate(test_goals, 1):
        print(f"\n🔬 Test {i}: {goal}")
        print("-" * 40)
        
        # Decompose goal
        subtasks = planner.decompose_goal(goal)
        
        # Execute plan (simulated)
        success = planner.execute_plan()
        
        # Track progress
        if success:
            progress = planner.track_progress()
            print(f"✅ Test {i} completed: {progress['progress_percentage']:.1f}%")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_different_goals()
