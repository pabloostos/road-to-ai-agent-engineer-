"""
Hybrid Search Optimization Demo
Shows how different weight combinations affect search performance
"""

import json
from pathlib import Path
from hybrid_search import HybridSearchSystem, load_documents


def test_weight_combinations():
    """Test different weight combinations for hybrid search"""
    print("🔬 HYBRID SEARCH OPTIMIZATION DEMO")
    print("=" * 50)
    
    # Load documents
    data_file = Path(__file__).parent.parent / "data" / "sample_docs.txt"
    documents = load_documents(str(data_file))
    
    # Initialize hybrid search system
    hybrid_search = HybridSearchSystem(documents)
    
    # Test query
    query = "cheap hybrid vehicles"
    
    # Different weight combinations to test
    weight_combinations = [
        (0.8, 0.2, "BM25-Heavy"),      # Mostly keyword search
        (0.6, 0.4, "BM25-Balanced"),   # Slightly more keyword
        (0.5, 0.5, "Equal-Weights"),   # Equal weights
        (0.4, 0.6, "TF-IDF-Balanced"), # Slightly more vector
        (0.2, 0.8, "TF-IDF-Heavy"),    # Mostly vector search
    ]
    
    print(f"\n🔍 Testing query: '{query}'")
    print(f"📊 Testing {len(weight_combinations)} weight combinations...")
    
    results = {}
    
    for alpha, beta, name in weight_combinations:
        print(f"\n⚖️  Testing {name} (α={alpha}, β={beta}):")
        
        # Perform search with these weights
        search_results = hybrid_search.search(query, top_k=3, alpha=alpha, beta=beta)
        
        # Store results
        results[name] = {
            'weights': {'alpha': alpha, 'beta': beta},
            'top_result': search_results[0] if search_results else None,
            'all_results': search_results
        }
        
        # Show top result
        if search_results:
            top = search_results[0]
            print(f"   🏆 Top result: {top['document']}")
            print(f"   📊 Score: {top['hybrid_score']} (BM25: {top['bm25_score']}, TF-IDF: {top['tfidf_score']})")
    
    # Save optimization results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    optimization_file = results_dir / "optimization_results.json"
    with open(optimization_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Optimization results saved to: {optimization_file}")
    
    # Show summary
    print(f"\n📈 OPTIMIZATION SUMMARY:")
    print(f"=" * 40)
    
    for name, data in results.items():
        if data['top_result']:
            top = data['top_result']
            weights = data['weights']
            print(f"   {name:15} | Score: {top['hybrid_score']:.4f} | Weights: α={weights['alpha']}, β={weights['beta']}")
            print(f"   {'':15} | Document: {top['document'][:50]}...")
            print()
    
    print("🎉 Optimization demo completed!")


def compare_search_methods():
    """Compare pure BM25, pure TF-IDF, and hybrid search"""
    print("\n🔬 SEARCH METHOD COMPARISON")
    print("=" * 40)
    
    # Load documents
    data_file = Path(__file__).parent.parent / "data" / "sample_docs.txt"
    documents = load_documents(str(data_file))
    
    # Initialize hybrid search system
    hybrid_search = HybridSearchSystem(documents)
    
    # Test queries
    test_queries = [
        "cheap hybrid vehicles",
        "electric cars with long range",
        "luxury vehicles with premium features"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Compare methods
        comparison = hybrid_search.compare_search_methods(query, top_k=3)
        
        # Show top result from each method
        print(f"   📝 BM25 Top: {comparison['bm25_results'][0]['document'][:40]}...")
        print(f"   🧠 TF-IDF Top: {comparison['tfidf_results'][0]['document'][:40]}...")
        print(f"   🔄 Hybrid Top: {comparison['hybrid_results'][0]['document'][:40]}...")
        
        # Check if hybrid found the best result
        hybrid_top = comparison['hybrid_results'][0]
        bm25_top = comparison['bm25_results'][0]
        tfidf_top = comparison['tfidf_results'][0]
        
        print(f"   🏆 Hybrid score: {hybrid_top['hybrid_score']:.4f}")
        print(f"   📊 BM25 score: {bm25_top['bm25_score']:.4f}, TF-IDF score: {tfidf_top['tfidf_score']:.4f}")


if __name__ == "__main__":
    # Run optimization demo
    test_weight_combinations()
    
    # Run method comparison
    compare_search_methods()
