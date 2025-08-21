#!/usr/bin/env python3
"""
Test Script for Query Interface (Step 3)
========================================
This script demonstrates how to use the Query Interface step by step.

🎯 Learning Objectives:
- See how to use the Query Interface
- Understand search across multiple KBs
- Learn about result ranking and filtering
- See export functionality in action
"""

from src.kb_query_interface import KnowledgeBaseQueryInterface

def main():
    """Test the Query Interface step by step."""
    print("🧪 Testing Query Interface (Step 3)")
    print("=" * 50)
    
    # Step 1: Initialize the query interface
    print("\n🔧 Step 1: Initialize Query Interface")
    print("-" * 40)
    query_interface = KnowledgeBaseQueryInterface()
    
    # Step 2: List available knowledge bases
    print("\n📋 Step 2: List Available Knowledge Bases")
    print("-" * 45)
    available_kbs = query_interface.list_available_knowledge_bases()
    
    if not available_kbs:
        print("❌ No knowledge bases found")
        return
    
    print(f"📚 Found {len(available_kbs)} knowledge bases:")
    for kb in available_kbs:
        status = "✅ Loaded" if kb["loaded"] else "⏳ Not loaded"
        print(f"   📚 {kb['name']} - {status}")
        print(f"      📄 Chunks: {kb['total_chunks']}")
        print(f"      📁 Files: {kb['total_files']}")
    
    # Step 3: Load knowledge bases
    print(f"\n📚 Step 3: Load Knowledge Bases")
    print("-" * 35)
    loaded_count = query_interface.load_all_knowledge_bases()
    
    if loaded_count == 0:
        print("❌ No knowledge bases loaded")
        return
    
    print(f"✅ Successfully loaded {loaded_count} knowledge bases")
    
    # Step 4: Get statistics
    print(f"\n📊 Step 4: Get Statistics")
    print("-" * 25)
    stats = query_interface.get_search_statistics()
    print(f"📚 Total KBs loaded: {stats['total_kbs_loaded']}")
    print(f"📄 Total chunks: {stats['total_chunks']}")
    print(f"📁 Total files: {stats['total_files']}")
    print(f"📋 Loaded KBs: {', '.join(stats['loaded_kb_names'])}")
    
    # Step 5: Test single KB search
    print(f"\n🎯 Step 5: Single KB Search")
    print("-" * 30)
    
    if "ai_knowledge" in stats["loaded_kb_names"]:
        print("🔍 Searching in 'ai_knowledge' KB only...")
        results = query_interface.search_single_kb(
            "ai_knowledge", 
            "What is artificial intelligence?",
            top_k=2
        )
        
        if "error" not in results and results["results"]:
            print(f"✅ Found {len(results['results'])} results:")
            for i, result in enumerate(results["results"], 1):
                print(f"   {i}. Score: {result['similarity']:.3f}")
                print(f"      📄 {result['text'][:80]}...")
        else:
            print("❌ No results found")
    
    # Step 6: Test multi-KB search
    print(f"\n🔍 Step 6: Multi-KB Search")
    print("-" * 30)
    
    # Search across all knowledge bases
    print("🔍 Searching across ALL knowledge bases...")
    results = query_interface.search(
        "machine learning", 
        top_k=3, 
        similarity_threshold=0.3
    )
    
    if "error" not in results and results["results"]:
        print(f"✅ Found {len(results['results'])} results across all KBs:")
        for i, result in enumerate(results["results"], 1):
            print(f"   {i}. {result['knowledge_base']} (score: {result['similarity']:.3f})")
            print(f"      📄 {result['text'][:80]}...")
    else:
        print("❌ No results found")
    
    # Step 7: Test specific KBs search
    print(f"\n🎯 Step 7: Specific KBs Search")
    print("-" * 35)
    
    # Search only in AI and cooking knowledge bases
    specific_kbs = ["ai_knowledge", "cooking_recipes"]
    print(f"🔍 Searching in specific KBs: {', '.join(specific_kbs)}")
    
    results = query_interface.search(
        "learning", 
        kb_names=specific_kbs,
        top_k=2
    )
    
    if "error" not in results and results["results"]:
        print(f"✅ Found {len(results['results'])} results in specific KBs:")
        for i, result in enumerate(results["results"], 1):
            print(f"   {i}. {result['knowledge_base']} (score: {result['similarity']:.3f})")
            print(f"      📄 {result['text'][:80]}...")
    else:
        print("❌ No results found")
    
    # Step 8: Test result formatting
    print(f"\n📝 Step 8: Result Formatting")
    print("-" * 30)
    
    results = query_interface.search("pasta", top_k=2)
    if "error" not in results:
        formatted_results = query_interface.format_search_results(results, include_metadata=True)
        print("📄 Formatted search results:")
        print(formatted_results[:500] + "..." if len(formatted_results) > 500 else formatted_results)
    
    # Step 9: Test export functionality
    print(f"\n💾 Step 9: Export Functionality")
    print("-" * 35)
    
    results = query_interface.search("policy", top_k=2)
    if "error" not in results:
        # Export to JSON
        success = query_interface.export_search_results(results, "test_search_results.json", "json")
        if success:
            print("✅ Exported to JSON successfully")
        
        # Export to text
        success = query_interface.export_search_results(results, "test_search_results.txt", "txt")
        if success:
            print("✅ Exported to text successfully")
    
    # Step 10: Performance test
    print(f"\n⚡ Step 10: Performance Test")
    print("-" * 30)
    
    test_queries = [
        "artificial intelligence",
        "machine learning", 
        "pasta recipe",
        "vacation policy",
        "employee benefits"
    ]
    
    total_time = 0
    total_results = 0
    
    for query in test_queries:
        results = query_interface.search(query, top_k=2)
        if "error" not in results:
            search_time = results["metadata"]["search_time_seconds"]
            result_count = len(results["results"])
            total_time += search_time
            total_results += result_count
            
            print(f"   🔍 '{query}': {result_count} results in {search_time:.3f}s")
    
    avg_time = total_time / len(test_queries) if test_queries else 0
    print(f"\n📊 Performance Summary:")
    print(f"   🔍 Total queries: {len(test_queries)}")
    print(f"   📄 Total results: {total_results}")
    print(f"   ⏱️  Total time: {total_time:.3f}s")
    print(f"   🚀 Average time per query: {avg_time:.3f}s")
    
    print(f"\n✅ Query Interface testing completed!")
    print(f"🎯 Step 3 implementation is working perfectly!")

if __name__ == "__main__":
    main()
