import os
import requests
from dotenv import load_dotenv

def load_api_key():
    """Load OpenRouter API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    return api_key

def test_openrouter_connection():
    """Test basic OpenRouter API connection with a simple prompt."""
    try:
        api_key = load_api_key()
        
        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Simple test prompt
        prompt = "Hello! Please respond with a simple greeting and tell me what you can do."
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100
        }
        
        print("Testing OpenRouter API connection...")
        print(f"Using model: {payload['model']}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            print("✅ API Connection Successful!")
            print(f"Response: {assistant_message}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function to run the test."""
    print("OpenRouter API Test")
    print("=" * 50)
    
    success = test_openrouter_connection()
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed. Please check your API key and connection.")

if __name__ == "__main__":
    main() 