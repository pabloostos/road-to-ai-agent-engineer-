"""
Prompt Engineering Exercise: Structured JSON Output from LLMs
===========================================================

This module implements the exercise for extracting structured JSON data
from Large Language Models using OpenAI API.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def exercise_1():
    """
    Exercise 1: Create a Prompt
    
    Write a prompt that asks the LLM to return a movie recommendation 
    in strict JSON format with the following fields:
    - title: string  
    - genre: string  
    - rating: float between 0.0 and 10.0
    
    Constraints:
    - Output should be JSON only, no explanations or extra text
    - Wrap JSON in triple backticks for easier extraction
    """
    prompt = """Return a movie recommendation in strict JSON format with the following structure. Respond with ONLY the JSON object, no explanations or additional text.

    Required fields:
    - title: string (movie title)
    - genre: string (movie genre)
    - rating: float (rating between 0.0 and 10.0)

    Example format:
    ```json
    {
    "title": "Inception",
    "genre": "Sci-Fi",
    "rating": 8.8
    }
    ```

    Respond with only a valid JSON object wrapped in triple backticks.
    """
    
    return prompt

def exercise_2():
    """
    Exercise 2: Generate Response using OpenAI API
    
    Connects to OpenAI API and generates a response using the prompt
    from exercise_1. Saves the raw response to a file for later processing.
    
    Returns:
        str: Raw response from the LLM, or None if error occurs
    """
    # Get API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        return None
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    print("OpenAI client initialized")
    
    # Get prompt from exercise 1
    prompt = exercise_1()
    print("Using prompt from exercise 1:")
    print(prompt)
    
    # Call OpenAI API
    print("Calling OpenAI API...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2  # Low temperature for consistent output
        )
        
        # Extract response content
        raw_response = response.choices[0].message.content
        print("Raw response from LLM:")
        print(raw_response)
        
        # Save response to file
        with open("raw_response.txt", "w") as f:
            f.write(raw_response)
        print("Response saved to 'raw_response.txt'")
        
        return raw_response
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def exercise_3():
    """
    Exercise 3: Parse JSON Output
    
    Uses json.loads() to convert the raw string into a Python dictionary.
    Extracts JSON from the LLM response and handles different formats.
    
    Returns:
        dict: Parsed JSON data, or None if parsing fails
    """
    import json
    
    # Read the raw response from file
    try:
        with open("raw_response.txt", "r") as f:
            raw_response = f.read()
    except FileNotFoundError:
        print("Error: raw_response.txt not found. Run exercise_2 first.")
        return None
    
    print("Raw response from file:")
    print(raw_response)
    
    # Extract JSON from response
    json_string = extract_json_from_response(raw_response)
    if not json_string:
        print("Error: Could not extract JSON from response")
        return None
    
    print("Extracted JSON string:")
    print(json_string)
    
    # Use json.loads() to parse JSON into Python dictionary
    try:
        parsed_data = json.loads(json_string)
        print("Successfully parsed JSON using json.loads()")
        print(f"Parsed data: {parsed_data}")
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON with json.loads(): {e}")
        return None

def extract_json_from_response(response):
    """
    Extract JSON from LLM response, handling different formats.
    
    Args:
        response (str): Raw response from LLM
        
    Returns:
        str: Extracted JSON string, or None if not found
    """
    # Remove leading/trailing whitespace
    response = response.strip()
    
    # Try to extract JSON from triple backticks with json specifier
    if "```json" in response:
        start = response.find("```json") + 7
        end = response.rfind("```")
        if end > start:
            return response[start:end].strip()
    
    # Try to extract JSON from triple backticks without specifier
    elif "```" in response:
        start = response.find("```") + 3
        end = response.rfind("```")
        if end > start:
            return response[start:end].strip()
    
    # If no backticks, assume the entire response is JSON
    return response

def exercise_4():
    """
    Exercise 4: Validate JSON Structure
    
    Defines a JSON Schema and validates the data using jsonschema.
    Ensures the movie recommendation has the correct structure and data types.
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    from jsonschema import validate, ValidationError
    
    # Define the JSON schema for movie recommendations
    schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Movie title"
            },
            "genre": {
                "type": "string", 
                "description": "Movie genre"
            },
            "rating": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 10.0,
                "description": "Rating between 0.0 and 10.0"
            }
        },
        "required": ["title", "genre", "rating"],
        "additionalProperties": False
    }
    
    # Get parsed data from exercise 3
    parsed_data = exercise_3()
    if not parsed_data:
        print("Error: No data to validate. Run exercise_3 first.")
        return False
    
    print("Validating JSON structure against schema...")
    print(f"Schema requirements:")
    print(f"- title: string")
    print(f"- genre: string") 
    print(f"- rating: number (0.0 to 10.0)")
    print(f"- All fields required")
    print(f"- No additional properties allowed")
    
    # Validate the data against the schema
    try:
        validate(instance=parsed_data, schema=schema)
        print("Validation successful: Data matches schema requirements")
        return True
    except ValidationError as e:
        print(f"Validation failed: {e.message}")
        print(f"Path: {e.path}")
        return False

def exercise_5():
    """
    Exercise 5: Save Valid Outputs
    
    Stores valid outputs in /examples/valid_outputs.json.
    Logs failed attempts in /logs/invalid.json with error messages.
    Creates necessary folder structure if it doesn't exist.
    
    Returns:
        bool: True if valid data was saved, False otherwise
    """
    import json
    import os
    from datetime import datetime
    
    # Create necessary directories
    os.makedirs("examples", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Get validation result from exercise 4
    validation_result = exercise_4()
    
    if validation_result:
        # Save valid output
        parsed_data = exercise_3()  # Get the parsed data again
        
        # Load existing valid outputs or create new list
        valid_outputs_file = "examples/valid_outputs.json"
        try:
            with open(valid_outputs_file, "r") as f:
                valid_outputs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            valid_outputs = []
        
        # Add timestamp to the data
        output_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": parsed_data
        }
        
        # Append to valid outputs
        valid_outputs.append(output_entry)
        
        # Save to file
        with open(valid_outputs_file, "w") as f:
            json.dump(valid_outputs, f, indent=2)
        
        print(f"Success: Valid output saved to {valid_outputs_file}")
        print(f"Total valid outputs: {len(valid_outputs)}")
        return True
        
    else:
        # Log invalid attempt
        invalid_log_file = "logs/invalid.json"
        
        # Load existing invalid logs or create new list
        try:
            with open(invalid_log_file, "r") as f:
                invalid_logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            invalid_logs = []
        
        # Get the raw response for logging
        try:
            with open("raw_response.txt", "r") as f:
                raw_response = f.read()
        except FileNotFoundError:
            raw_response = "No raw response file found"
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "raw_response": raw_response,
            "error": "Validation failed - data does not match schema requirements"
        }
        
        # Append to invalid logs
        invalid_logs.append(log_entry)
        
        # Save to file
        with open(invalid_log_file, "w") as f:
            json.dump(invalid_logs, f, indent=2)
        
        print(f"Logged: Invalid attempt saved to {invalid_log_file}")
        print(f"Total invalid attempts: {len(invalid_logs)}")
        return False

def main():
    """
    Main function to test the complete flow:
    1. Generate response (exercise_2)
    2. Parse JSON (exercise_3)
    3. Validate structure (exercise_4)
    4. Save outputs (exercise_5)
    """
    print("Testing Complete Flow")
    print("=" * 50)
    
    # Test exercise 2 (generate response)
    print("Step 1: Generating response from OpenAI API...")
    result = exercise_2()
    
    if not result:
        print("Failed to get response from OpenAI API")
        return
    
    print(f"Success: Received response with {len(result)} characters")
    print("\n" + "=" * 50)
    
    # Test exercise 3 (parse JSON)
    print("Step 2: Parsing JSON from response...")
    parsed_data = exercise_3()
    
    if not parsed_data:
        print("Failed to parse JSON from response")
        return
    
    print(f"Success: JSON parsed successfully!")
    print(f"Movie title: {parsed_data.get('title', 'N/A')}")
    print(f"Genre: {parsed_data.get('genre', 'N/A')}")
    print(f"Rating: {parsed_data.get('rating', 'N/A')}")
    print("\n" + "=" * 50)
    
    # Test exercise 4 (validate structure)
    print("Step 3: Validating JSON structure...")
    validation_result = exercise_4()
    
    if not validation_result:
        print("Failed: Data validation failed")
        return
    
    print("Success: Data validation passed!")
    print("\n" + "=" * 50)
    
    # Test exercise 5 (save outputs)
    print("Step 4: Saving outputs...")
    save_result = exercise_5()
    
    if save_result:
        print("Success: Valid output saved!")
    else:
        print("Failed: Could not save output")

if __name__ == "__main__":
    main()
    
    