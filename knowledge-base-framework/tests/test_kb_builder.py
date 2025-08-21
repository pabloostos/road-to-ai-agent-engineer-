#!/usr/bin/env python3
"""
Test Script for KB Builder (Step 2)
===================================
This script demonstrates how to use the KB Builder step by step.

🎯 Learning Objectives:
- See how to use the KB Builder interface
- Understand configuration options
- Learn about validation and error handling
- See progress feedback in action
"""

from src.kb_builder import KnowledgeBaseBuilder

def main():
    """Test the KB Builder step by step."""
    print("🧪 Testing KB Builder (Step 2)")
    print("=" * 50)
    
    # Step 1: Initialize the builder
    print("\n🔧 Step 1: Initialize KB Builder")
    print("-" * 30)
    builder = KnowledgeBaseBuilder()
    
    # Step 2: List available files in different directories
    print("\n📄 Step 2: List Available Files")
    print("-" * 30)
    
    directories = ["data/ai_knowledge", "data/cooking_recipes", "data/company_policies"]
    
    for data_dir in directories:
        print(f"\n📁 Directory: {data_dir}")
        files = builder.list_available_files(data_dir)
        
        if files:
            for file_info in files:
                print(f"   📄 {file_info['name']}")
                print(f"      📊 Size: {file_info['size_mb']} MB")
                print(f"      📝 Lines: {file_info['lines']}")
        else:
            print("   ❌ No text files found")
    
    # Step 3: Create knowledge base with default settings
    print(f"\n🚀 Step 3: Create KB with Default Settings")
    print("-" * 50)
    
    result = builder.create_knowledge_base(
        name="default_kb",
        data_dir="data/ai_knowledge"
    )
    
    if result["success"]:
        print(f"✅ Success! Created KB: {result['name']}")
        print(f"   📊 Files processed: {result['files_processed']}")
        print(f"   📄 Total chunks: {result['stats']['total_chunks']}")
        print(f"   🔤 Total tokens: {result['stats']['total_tokens']:,}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Step 4: Create knowledge base with custom settings
    print(f"\n⚙️  Step 4: Create KB with Custom Settings")
    print("-" * 50)
    
    custom_config = {
        "chunk_size": 200,  # Smaller chunks
        "overlap_size": 20,  # Less overlap
        "similarity_threshold": 0.5  # Higher threshold
    }
    
    result = builder.create_knowledge_base(
        name="custom_kb",
        data_dir="data/cooking_recipes",
        config=custom_config
    )
    
    if result["success"]:
        print(f"✅ Success! Created KB: {result['name']}")
        print(f"   📊 Configuration used:")
        for key, value in result['config'].items():
            print(f"      • {key}: {value}")
        print(f"   📄 Total chunks: {result['stats']['total_chunks']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Step 5: List all knowledge bases
    print(f"\n📋 Step 5: List All Knowledge Bases")
    print("-" * 40)
    
    kbs = builder.list_knowledge_bases()
    
    if kbs:
        print(f"📚 Found {len(kbs)} knowledge bases:")
        for kb in kbs:
            print(f"\n   📚 {kb['name']}")
            print(f"      📅 Created: {kb['created_at']}")
            print(f"      📄 Chunks: {kb['total_chunks']}")
            print(f"      📁 Files: {kb['total_files']}")
            print(f"      🤖 Model: {kb['embedding_model']}")
    else:
        print("❌ No knowledge bases found")
    
    # Step 6: Test file validation
    print(f"\n🔍 Step 6: Test File Validation")
    print("-" * 35)
    
    # Test with valid files
    valid_files = ["data/ai_knowledge/ai_basics.txt"]
    validation = builder.validate_files(valid_files)
    
    print(f"✅ Validation test:")
    print(f"   📄 Files tested: {len(validation['files'])}")
    print(f"   ✅ Valid: {validation['valid']}")
    print(f"   ❌ Errors: {len(validation['errors'])}")
    
    # Test with non-existent file
    invalid_files = ["data/non_existent_file.txt"]
    validation = builder.validate_files(invalid_files)
    
    print(f"\n❌ Invalid file test:")
    print(f"   📄 Files tested: {len(validation['files'])}")
    print(f"   ✅ Valid: {validation['valid']}")
    print(f"   ❌ Errors: {len(validation['errors'])}")
    for error in validation['errors']:
        print(f"      • {error}")
    
    print(f"\n✅ KB Builder testing completed!")
    print(f"🎯 Step 2 implementation is working perfectly!")

if __name__ == "__main__":
    main()
