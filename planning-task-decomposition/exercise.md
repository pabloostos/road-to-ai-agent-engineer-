# Exercise: Simple Task Planning System

## 🎯 **Objective**
Build a basic AI planning system that can break down a goal into subtasks and execute them step by step.

## 📋 **Exercise Requirements**

### **Step 1: Goal Definition**
- Create a simple goal: `"Plan a weekend trip to Barcelona"`

### **Step 2: Task Decomposition**
- Use OpenRouter API to break down the goal into 5-7 subtasks
- Store the subtasks in a structured format

### **Step 3: Execution Simulation**
- Simulate executing each subtask by printing status messages
- Track completion progress

## 🛠️ **What You'll Build**

**File: `src/simple_planner.py`**
- A `SimplePlanner` class with 3 main methods:
  1. `decompose_goal()` - Break goal into subtasks
  2. `execute_plan()` - Run subtasks sequentially  
  3. `track_progress()` - Monitor completion status

## 📝 **Expected Output**
```
🎯 Goal: Plan a weekend trip to Barcelona

📋 Generated Plan:
1. Research flights to Barcelona
2. Book accommodation
3. Plan daily itinerary
4. Research local attractions
5. Create budget estimate

🚀 Executing Plan:
✅ Executing: Research flights to Barcelona
✅ Executing: Book accommodation
✅ Executing: Plan daily itinerary
✅ Executing: Research local attractions
✅ Executing: Create budget estimate

🎉 Plan completed successfully!
```

## 🎯 **Learning Focus**
- **Simple & Clean**: Minimal code, maximum learning
- **Core Concepts**: Goal → Decomposition → Execution
- **Practical**: Real-world planning workflow
- **Extensible**: Easy to add more features later

## ⏱️ **Time Estimate**
- **Implementation**: 15-20 minutes
- **Testing**: 5 minutes
- **Total**: ~25 minutes

Ready to build your first AI planning system! 🚀
