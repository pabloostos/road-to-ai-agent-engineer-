"""
Simple Hybrid Search System
Combines BM25 keyword search with TF-IDF vector search
"""

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import json
from pathlib import Path


class HybridSearchSystem:
    """
    A simple hybrid search system that combines:
    - BM25 for keyword-based search
    - TF-IDF for vector-based search (simpler alternative to embeddings)
    """
    
    def __init__(self, documents: List[str]):
        """
        Initialize the hybrid search system
        
        Args:
            documents: List of document strings to search through
        """
        self.documents = documents
        self.doc_ids = [f"doc_{i}" for i in range(len(documents))]
        
        print(f"🔧 Initializing Hybrid Search System...")
        print(f"   📄 Documents: {len(documents)}")
        
        # Step 1: Initialize BM25 for keyword search
        print(f"   📝 Setting up BM25 keyword search...")
        self._setup_bm25()
        
        # Step 2: Initialize TF-IDF for vector search
        print(f"   🧠 Setting up TF-IDF vector search...")
        self._setup_tfidf()
        
        print(f"✅ Hybrid Search System ready!")
    
    def _setup_bm25(self):
        """Set up BM25 for keyword-based search"""
        # Tokenize documents for BM25 (simple word splitting)
        self.tokenized_docs = [doc.lower().split() for doc in self.documents]
        
        # Create BM25 model
        self.bm25 = BM25Okapi(self.tokenized_docs)
        
        print(f"      ✅ BM25 initialized with {len(self.documents)} documents")
    
    def _setup_tfidf(self):
        """Set up TF-IDF for vector-based search"""
        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        
        # Create TF-IDF matrix for all documents
        print(f"      🔄 Creating TF-IDF vectors for {len(self.documents)} documents...")
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)
        
        print(f"      ✅ TF-IDF search ready with {self.tfidf_matrix.shape[1]} features")
    
    def search(self, query: str, top_k: int = 5, alpha: float = 0.5, beta: float = 0.5) -> List[Dict]:
        """
        Perform hybrid search combining BM25 and TF-IDF search
        
        Args:
            query: Search query
            top_k: Number of results to return
            alpha: Weight for BM25 scores (0.0 to 1.0)
            beta: Weight for TF-IDF scores (0.0 to 1.0)
            
        Returns:
            List of search results with scores and metadata
        """
        print(f"\n🔍 Searching for: '{query}'")
        print(f"   ⚖️  Weights: BM25={alpha:.1f}, TF-IDF={beta:.1f}")
        
        # Step 1: Get BM25 scores
        print(f"   📝 Getting BM25 keyword scores...")
        bm25_scores = self._get_bm25_scores(query)
        
        # Step 2: Get TF-IDF scores
        print(f"   🧠 Getting TF-IDF vector scores...")
        tfidf_scores = self._get_tfidf_scores(query)
        
        # Step 3: Combine scores using hybrid fusion
        print(f"   🔄 Combining scores with hybrid fusion...")
        hybrid_scores = self._combine_scores(bm25_scores, tfidf_scores, alpha, beta)
        
        # Step 4: Get top results
        results = self._get_top_results(hybrid_scores, top_k, query)
        
        print(f"✅ Found {len(results)} results")
        return results
    
    def _get_bm25_scores(self, query: str) -> List[float]:
        """Get BM25 scores for the query"""
        # Tokenize query
        query_tokens = query.lower().split()
        
        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)
        
        # Normalize scores to 0-1 range
        if max(scores) > 0:
            scores = [score / max(scores) for score in scores]
        
        return scores
    
    def _get_tfidf_scores(self, query: str) -> List[float]:
        """Get TF-IDF scores for the query"""
        # Transform query to TF-IDF vector
        query_vector = self.tfidf_vectorizer.transform([query])
        
        # Calculate cosine similarity with all document vectors
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Convert to list and normalize to 0-1 range
        scores = similarities.tolist()
        
        return scores
    
    def _combine_scores(self, bm25_scores: List[float], tfidf_scores: List[float], 
                       alpha: float, beta: float) -> List[float]:
        """Combine BM25 and TF-IDF scores using weighted fusion"""
        hybrid_scores = []
        
        for i in range(len(self.documents)):
            # Hybrid score = α * BM25_score + β * TF-IDF_score
            hybrid_score = alpha * bm25_scores[i] + beta * tfidf_scores[i]
            hybrid_scores.append(hybrid_score)
        
        return hybrid_scores
    
    def _get_top_results(self, scores: List[float], top_k: int, query: str) -> List[Dict]:
        """Get top-k results with metadata"""
        # Create list of (doc_id, score) pairs
        doc_scores = list(zip(self.doc_ids, scores))
        
        # Sort by score (descending)
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top-k results
        results = []
        for i, (doc_id, score) in enumerate(doc_scores[:top_k]):
            doc_index = int(doc_id.split('_')[1])
            
            # Get individual scores for this document
            bm25_scores = self._get_bm25_scores(query)
            tfidf_scores = self._get_tfidf_scores(query)
            
            result = {
                'rank': i + 1,
                'doc_id': doc_id,
                'document': self.documents[doc_index],
                'hybrid_score': round(score, 4),
                'bm25_score': round(bm25_scores[doc_index], 4),
                'tfidf_score': round(tfidf_scores[doc_index], 4)
            }
            results.append(result)
        
        return results
    
    def compare_search_methods(self, query: str, top_k: int = 5) -> Dict:
        """
        Compare different search methods for the same query
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Dictionary with results from different methods
        """
        print(f"\n🔬 Comparing search methods for: '{query}'")
        
        # Pure BM25 search
        bm25_scores = self._get_bm25_scores(query)
        bm25_results = self._get_top_results(bm25_scores, top_k, query)
        
        # Pure TF-IDF search
        tfidf_scores = self._get_tfidf_scores(query)
        tfidf_results = self._get_top_results(tfidf_scores, top_k, query)
        
        # Hybrid search (equal weights)
        hybrid_results = self.search(query, top_k, alpha=0.5, beta=0.5)
        
        comparison = {
            'query': query,
            'bm25_results': bm25_results,
            'tfidf_results': tfidf_results,
            'hybrid_results': hybrid_results
        }
        
        return comparison


def load_documents(file_path: str) -> List[str]:
    """Load documents from a text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = [line.strip() for line in f if line.strip()]
    return documents


def save_results(results: Dict, file_path: str):
    """Save search results to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"💾 Results saved to: {file_path}")


def demo_hybrid_search():
    """Demo the hybrid search system"""
    print("🚀 HYBRID SEARCH SYSTEM DEMO")
    print("=" * 50)
    
    # Load sample documents
    data_file = Path(__file__).parent.parent / "data" / "sample_docs.txt"
    documents = load_documents(str(data_file))
    
    print(f"📄 Loaded {len(documents)} documents:")
    for i, doc in enumerate(documents[:3]):  # Show first 3
        print(f"   {i+1}. {doc}")
    if len(documents) > 3:
        print(f"   ... and {len(documents) - 3} more")
    
    # Initialize hybrid search system
    hybrid_search = HybridSearchSystem(documents)
    
    # Test queries
    test_queries = [
        "cheap hybrid vehicles",
        "electric cars with long range",
        "luxury vehicles with premium features",
        "budget friendly transportation"
    ]
    
    # Create results directory
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Test each query
    for i, query in enumerate(test_queries):
        print(f"\n{'='*60}")
        print(f"TEST {i+1}: {query}")
        print(f"{'='*60}")
        
        # Compare different search methods
        comparison = hybrid_search.compare_search_methods(query, top_k=3)
        
        # Save results
        results_file = results_dir / f"search_results_{i+1}.json"
        save_results(comparison, str(results_file))
        
        # Show top hybrid results
        print(f"\n🏆 TOP HYBRID RESULTS:")
        for result in comparison['hybrid_results']:
            print(f"   {result['rank']}. Score: {result['hybrid_score']}")
            print(f"      📄 {result['document']}")
            print(f"      📊 BM25: {result['bm25_score']}, TF-IDF: {result['tfidf_score']}")
            print()
    
    print("🎉 Demo completed! Check the results/ directory for detailed outputs.")


if __name__ == "__main__":
    demo_hybrid_search()
