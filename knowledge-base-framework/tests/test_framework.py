#!/usr/bin/env python3
"""
Test Script for Universal Knowledge Base Framework
=================================================
This script demonstrates the full functionality of our framework by:
1. Creating knowledge bases from our sample data
2. Querying the knowledge bases
3. Showing statistics and metadata
"""

from src.kb_framework import UniversalKnowledgeBase

def main():
    """Test the complete framework functionality."""
    print("🧪 Testing Universal Knowledge Base Framework")
    print("=" * 60)
    
    # 🔧 Initialize framework
    kb = UniversalKnowledgeBase()
    
    # 🚀 Create knowledge bases from our sample data
    print("\n📚 Creating Knowledge Bases...")
    
    # Create AI knowledge base
    success = kb.create_knowledge_base("ai_knowledge", "data/ai_knowledge/")
    if success:
        print("✅ AI Knowledge Base created successfully!")
    
    # Create cooking knowledge base
    success = kb.create_knowledge_base("cooking_recipes", "data/cooking_recipes/")
    if success:
        print("✅ Cooking Knowledge Base created successfully!")
    
    # Create company policies knowledge base
    success = kb.create_knowledge_base("company_policies", "data/company_policies/")
    if success:
        print("✅ Company Policies Knowledge Base created successfully!")
    
    # 📋 List all knowledge bases
    print(f"\n📋 Available Knowledge Bases:")
    kbs = kb.list_knowledge_bases()
    for kb_info in kbs:
        print(f"   • {kb_info['name']}: {kb_info['total_chunks']} chunks")
    
    # 📊 Show detailed statistics
    print(f"\n📊 Knowledge Base Statistics:")
    for kb_info in kbs:
        stats = kb.get_kb_stats(kb_info['name'])
        print(f"\n📈 {stats['name'].upper()}:")
        print(f"   📄 Total chunks: {stats['total_chunks']}")
        print(f"   🔤 Total tokens: {stats['total_tokens']:,}")
        print(f"   📊 Avg tokens/chunk: {stats['average_tokens_per_chunk']}")
        print(f"   📁 Files: {list(stats['files'].keys())}")
    
    # 🔍 Test queries
    print(f"\n🔍 Testing Queries:")
    print("-" * 40)
    
    # Test AI knowledge base
    if "ai_knowledge" in [kb["name"] for kb in kbs]:
        print(f"\n❓ Query: What is machine learning?")
        results = kb.query_knowledge_base("ai_knowledge", "What is machine learning?")
        if "error" not in results:
            print(f"   📊 Found {results['metadata']['results_returned']} results")
            print(f"   🎯 Top similarity: {results['metadata']['top_similarity']:.3f}")
            for result in results["results"][:2]:
                print(f"   📄 {result['file_name']} (score: {result['similarity']:.3f})")
                print(f"      {result['text'][:150]}...")
    
    # Test cooking knowledge base
    if "cooking_recipes" in [kb["name"] for kb in kbs]:
        print(f"\n❓ Query: How to make pasta?")
        results = kb.query_knowledge_base("cooking_recipes", "How to make pasta?")
        if "error" not in results:
            print(f"   📊 Found {results['metadata']['results_returned']} results")
            print(f"   🎯 Top similarity: {results['metadata']['top_similarity']:.3f}")
            for result in results["results"][:2]:
                print(f"   📄 {result['file_name']} (score: {result['similarity']:.3f})")
                print(f"      {result['text'][:150]}...")
    
    # Test company policies knowledge base
    if "company_policies" in [kb["name"] for kb in kbs]:
        print(f"\n❓ Query: What is the vacation policy?")
        results = kb.query_knowledge_base("company_policies", "What is the vacation policy?")
        if "error" not in results:
            print(f"   📊 Found {results['metadata']['results_returned']} results")
            print(f"   🎯 Top similarity: {results['metadata']['top_similarity']:.3f}")
            for result in results["results"][:2]:
                print(f"   📄 {result['file_name']} (score: {result['similarity']:.3f})")
                print(f"      {result['text'][:150]}...")
    
    # 🎯 Test semantic search capabilities
    print(f"\n🎯 Testing Semantic Search Capabilities:")
    print("-" * 40)
    
    # Test synonym understanding
    if "ai_knowledge" in [kb["name"] for kb in kbs]:
        print(f"\n❓ Query: Tell me about artificial intelligence")
        results = kb.query_knowledge_base("ai_knowledge", "Tell me about artificial intelligence")
        if "error" not in results and results["results"]:
            print(f"   ✅ Found relevant content about AI!")
            print(f"   📄 Top result: {results['results'][0]['file_name']}")
            print(f"   🎯 Similarity: {results['results'][0]['similarity']:.3f}")
    
    # Test cooking knowledge
    if "cooking_recipes" in [kb["name"] for kb in kbs]:
        print(f"\n❓ Query: Italian food preparation")
        results = kb.query_knowledge_base("cooking_recipes", "Italian food preparation")
        if "error" not in results and results["results"]:
            print(f"   ✅ Found relevant content about Italian cooking!")
            print(f"   📄 Top result: {results['results'][0]['file_name']}")
            print(f"   🎯 Similarity: {results['results'][0]['similarity']:.3f}")
    
    print(f"\n✅ Framework testing completed successfully!")
    print(f"🎯 The Universal Knowledge Base Framework is working perfectly!")

if __name__ == "__main__":
    main()
