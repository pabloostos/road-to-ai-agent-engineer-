"""
Example: Context Memory and Feedback Loops
Demonstrates the concepts from the Memory & Context Management lecture.
"""

# This is a conceptual example showing the structure
# In a real implementation, you would use actual API calls

class ContextMemoryExample:
    """
    Example implementation of context memory and feedback loops.
    This demonstrates the concepts without actual API calls.
    """
    
    def __init__(self):
        """Initialize the context memory system."""
        self.conversation_memory = []
        self.feedback_history = []
        self.max_context_turns = 5
    
    def add_to_memory(self, speaker: str, message: str):
        """Add a message to conversation memory."""
        self.conversation_memory.append(f"{speaker}: {message}")
        
        # Keep only the last N turns to manage token limits
        if len(self.conversation_memory) > self.max_context_turns * 2:
            self.conversation_memory = self.conversation_memory[-self.max_context_turns * 2:]
    
    def get_context(self) -> str:
        """Get the current conversation context."""
        return "\n".join(self.conversation_memory[-self.max_context_turns * 2:])
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response with context awareness.
        This is a simulation - in real implementation, you'd call an LLM API.
        """
        # Add user input to memory
        self.add_to_memory("User", user_input)
        
        # Get context for response generation
        context = self.get_context()
        
        # Simulate LLM response generation
        response = f"Based on our conversation context, here's my response to: {user_input}"
        
        # Add response to memory
        self.add_to_memory("Assistant", response)
        
        return response
    
    def feedback_review(self, response: str) -> str:
        """
        Review a response using self-critique.
        This is a simulation - in real implementation, you'd call an LLM API.
        """
        review_prompt = f"""
        Review the following response for clarity and accuracy:
        "{response}"
        Suggest improvements if necessary.
        """
        
        # Simulate feedback generation
        feedback = f"Review of response: {response[:50]}... - This response could be improved by being more specific."
        
        # Store feedback for learning
        self.feedback_history.append({
            "response": response,
            "feedback": feedback,
            "timestamp": "2024-01-01 12:00:00"
        })
        
        return feedback
    
    def improve_response(self, original_response: str, feedback: str) -> str:
        """
        Improve a response based on feedback.
        This is a simulation - in real implementation, you'd call an LLM API.
        """
        improvement_prompt = f"""
        Original response: "{original_response}"
        Feedback: "{feedback}"
        
        Please provide an improved version of the response.
        """
        
        # Simulate improved response
        improved_response = f"Improved version of: {original_response[:30]}... (incorporating feedback)"
        
        return improved_response


def demonstrate_context_memory():
    """Demonstrate context memory and feedback loops."""
    
    print("🧠 Context Memory and Feedback Loops Demo")
    print("=" * 50)
    
    # Create the example system
    system = ContextMemoryExample()
    
    # Simulate a conversation with context
    print("\n1️⃣ Starting conversation with context memory...")
    
    user_messages = [
        "Hello! I need help planning a trip to Paris.",
        "I want to visit the Eiffel Tower and Louvre Museum.",
        "What's the best time to visit these attractions?",
        "Can you also suggest some good restaurants nearby?"
    ]
    
    for i, message in enumerate(user_messages, 1):
        print(f"\n📝 Turn {i}: {message}")
        
        # Generate response with context
        response = system.generate_response(message)
        print(f"🤖 Assistant: {response}")
        
        # Apply feedback loop
        feedback = system.feedback_review(response)
        print(f"🔍 Feedback: {feedback}")
        
        # Improve response based on feedback
        improved_response = system.improve_response(response, feedback)
        print(f"✨ Improved: {improved_response}")
    
    # Show final context
    print(f"\n📚 Final Conversation Context:")
    print("-" * 30)
    context = system.get_context()
    for line in context.split('\n'):
        if line.strip():
            print(f"  {line}")
    
    print(f"\n📊 System Statistics:")
    print(f"  - Total conversation turns: {len(system.conversation_memory)}")
    print(f"  - Feedback reviews: {len(system.feedback_history)}")
    print(f"  - Context management: Active (last {system.max_context_turns} turns)")


if __name__ == "__main__":
    demonstrate_context_memory()
