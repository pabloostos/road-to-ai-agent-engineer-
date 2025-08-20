#!/usr/bin/env python3
"""
Embeddings Creation & Similarity Search System
==============================================
Complete System: Parts 2, 3, and 4

This module demonstrates:
- Part 2: Similarity Search Engine
- Part 3: Text Clustering  
- Part 4: Cost Analysis
"""

import numpy as np
from typing import List, Dict, Any, Tuple
import json
from collections import defaultdict


class SimilaritySearchEngine:
    """
    Part 2: Similarity Search Engine
    
    This class handles:
    - Calculating cosine similarity between vectors
    - Finding top-k most similar texts
    - Performing semantic search
    """
    
    def __init__(self):
        """Initialize the similarity search engine"""
        self.embeddings_database = []  # Store our embeddings
        print("✅ SimilaritySearchEngine initialized")
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Formula: cos(θ) = (A·B) / (||A|| × ||B||)
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        # Calculate dot product
        dot_product = np.dot(vec1, vec2)
        
        # Calculate magnitudes
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        return float(similarity)
    
    def add_embedding(self, text: str, embedding: List[float]):
        """Add a text and its embedding to the database"""
        self.embeddings_database.append({
            "text": text,
            "embedding": embedding
        })
        print(f"✅ Added: '{text[:30]}...'")
    
    def find_similar_texts(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """
        Find the top-k most similar texts to a query
        
        Args:
            query_embedding: The embedding of the query text
            top_k: Number of similar texts to return
            
        Returns:
            List of dictionaries with text and similarity score
        """
        print(f"\n🔍 Finding top {top_k} similar texts...")
        
        similarities = []
        
        # Calculate similarity with each text in database
        for item in self.embeddings_database:
            similarity = self.cosine_similarity(query_embedding, item["embedding"])
            similarities.append({
                "text": item["text"],
                "similarity": similarity
            })
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top-k results
        top_results = similarities[:top_k]
        
        print(f"📊 Top {top_k} results:")
        for i, result in enumerate(top_results, 1):
            print(f"   {i}. Similarity: {result['similarity']:.4f} - '{result['text'][:50]}...'")
        
        return top_results
    
    def semantic_search(self, query_text: str, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """
        Perform semantic search (wrapper around find_similar_texts)
        
        Args:
            query_text: The original query text
            query_embedding: The embedding of the query
            top_k: Number of results to return
            
        Returns:
            List of similar texts with scores
        """
        print(f"\n🎯 Semantic Search for: '{query_text}'")
        
        results = self.find_similar_texts(query_embedding, top_k)
        
        # Add query info to results
        for result in results:
            result["query"] = query_text
        
        return results


class TextClustering:
    """
    Part 3: Text Clustering System
    
    This class handles:
    - Grouping similar texts together
    - Identifying clusters of related content
    - Providing cluster summaries
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        """Initialize the clustering system"""
        self.similarity_threshold = similarity_threshold
        self.clusters = []
        print(f"✅ TextClustering initialized (threshold: {similarity_threshold})")
    
    def cluster_texts(self, embeddings_data: List[Dict]) -> List[Dict]:
        """
        Group similar texts into clusters
        
        Args:
            embeddings_data: List of dicts with 'text' and 'embedding' keys
            
        Returns:
            List of clusters with texts and metadata
        """
        print(f"\n🔗 Clustering {len(embeddings_data)} texts...")
        
        # Reset clusters
        self.clusters = []
        processed_indices = set()
        
        # Simple clustering algorithm: find groups of similar texts
        for i, item1 in enumerate(embeddings_data):
            if i in processed_indices:
                continue
            
            # Start a new cluster
            cluster = {
                "cluster_id": len(self.clusters),
                "texts": [item1["text"]],
                "embeddings": [item1["embedding"]],
                "size": 1,
                "average_similarity": 1.0
            }
            
            processed_indices.add(i)
            
            # Find similar texts
            for j, item2 in enumerate(embeddings_data):
                if j in processed_indices:
                    continue
                
                # Calculate similarity
                similarity = self._cosine_similarity(item1["embedding"], item2["embedding"])
                
                if similarity >= self.similarity_threshold:
                    cluster["texts"].append(item2["text"])
                    cluster["embeddings"].append(item2["embedding"])
                    cluster["size"] += 1
                    processed_indices.add(j)
            
            # Calculate cluster statistics
            cluster["average_similarity"] = self._calculate_cluster_similarity(cluster["embeddings"])
            cluster["summary"] = self._generate_cluster_summary(cluster["texts"])
            
            self.clusters.append(cluster)
        
        print(f"📊 Found {len(self.clusters)} clusters:")
        for cluster in self.clusters:
            print(f"   Cluster {cluster['cluster_id']}: {cluster['size']} texts, "
                  f"avg similarity: {cluster['average_similarity']:.3f}")
        
        return self.clusters
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return float(dot_product / (magnitude1 * magnitude2))
    
    def _calculate_cluster_similarity(self, embeddings: List[List[float]]) -> float:
        """Calculate average similarity within a cluster"""
        if len(embeddings) <= 1:
            return 1.0
        
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = self._cosine_similarity(embeddings[i], embeddings[j])
                similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 1.0
    
    def _generate_cluster_summary(self, texts: List[str]) -> str:
        """Generate a summary for a cluster of texts"""
        if not texts:
            return "Empty cluster"
        
        # Simple summary: first few words of first text + count
        first_text = texts[0]
        words = first_text.split()[:3]
        summary = " ".join(words) + "..."
        
        return f"{summary} ({len(texts)} texts)"
    
    def get_cluster_summary(self) -> Dict[str, Any]:
        """Get overall clustering summary"""
        if not self.clusters:
            return {"error": "No clusters found"}
        
        return {
            "total_clusters": len(self.clusters),
            "total_texts": sum(cluster["size"] for cluster in self.clusters),
            "average_cluster_size": np.mean([cluster["size"] for cluster in self.clusters]),
            "largest_cluster": max(self.clusters, key=lambda x: x["size"])["size"],
            "smallest_cluster": min(self.clusters, key=lambda x: x["size"])["size"],
            "average_similarity": np.mean([cluster["average_similarity"] for cluster in self.clusters])
        }


class CostAnalyzer:
    """
    Part 4: Cost Analysis System
    
    This class handles:
    - Tracking token usage and costs
    - Providing cost optimization recommendations
    - Generating cost reports
    """
    
    def __init__(self):
        """Initialize the cost analyzer"""
        self.cost_data = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "requests_by_type": defaultdict(int),
            "cost_by_type": defaultdict(float)
        }
        
        # Cost per 1K tokens (OpenAI ada-002 pricing)
        self.cost_per_1k_tokens = 0.0001  # $0.0001 per 1K tokens
        
        print("✅ CostAnalyzer initialized")
    
    def add_request(self, request_type: str, tokens: int, cost_usd: float = None):
        """Add a request to the cost tracker"""
        if cost_usd is None:
            cost_usd = (tokens / 1000) * self.cost_per_1k_tokens
        
        self.cost_data["total_requests"] += 1
        self.cost_data["total_tokens"] += tokens
        self.cost_data["total_cost_usd"] += cost_usd
        self.cost_data["requests_by_type"][request_type] += 1
        self.cost_data["cost_by_type"][request_type] += cost_usd
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary"""
        if self.cost_data["total_requests"] == 0:
            return {"message": "No requests tracked yet"}
        
        return {
            "total_requests": self.cost_data["total_requests"],
            "total_tokens": self.cost_data["total_tokens"],
            "total_cost_usd": round(self.cost_data["total_cost_usd"], 6),
            "average_cost_per_request": round(
                self.cost_data["total_cost_usd"] / self.cost_data["total_requests"], 6
            ),
            "average_tokens_per_request": round(
                self.cost_data["total_tokens"] / self.cost_data["total_requests"], 1
            ),
            "requests_by_type": dict(self.cost_data["requests_by_type"]),
            "cost_by_type": {k: round(v, 6) for k, v in self.cost_data["cost_by_type"].items()}
        }
    
    def get_optimization_recommendations(self) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        if self.cost_data["total_requests"] == 0:
            return ["No data available for recommendations"]
        
        # Check for high token usage
        avg_tokens = self.cost_data["total_tokens"] / self.cost_data["total_requests"]
        if avg_tokens > 1000:
            recommendations.append("Consider shorter texts to reduce token usage")
        
        # Check for high costs
        if self.cost_data["total_cost_usd"] > 0.01:
            recommendations.append("Monitor costs closely - consider caching embeddings")
        
        # Check request distribution
        if len(self.cost_data["requests_by_type"]) > 1:
            recommendations.append("Consider batching similar requests to reduce API calls")
        
        if not recommendations:
            recommendations.append("Cost usage looks optimal!")
        
        return recommendations
    
    def generate_cost_report(self) -> str:
        """Generate a formatted cost report"""
        summary = self.get_cost_summary()
        recommendations = self.get_optimization_recommendations()
        
        report = f"""
💰 COST ANALYSIS REPORT
{'='*50}
📊 Summary:
   Total Requests: {summary.get('total_requests', 0)}
   Total Tokens: {summary.get('total_tokens', 0):,}
   Total Cost: ${summary.get('total_cost_usd', 0):.6f}
   Avg Cost/Request: ${summary.get('average_cost_per_request', 0):.6f}
   Avg Tokens/Request: {summary.get('average_tokens_per_request', 0):.1f}

📈 Breakdown by Type:
"""
        
        for req_type, count in summary.get('requests_by_type', {}).items():
            cost = summary.get('cost_by_type', {}).get(req_type, 0)
            report += f"   {req_type}: {count} requests, ${cost:.6f}\n"
        
        report += f"""
💡 Optimization Recommendations:
"""
        
        for rec in recommendations:
            report += f"   • {rec}\n"
        
        return report


def create_mock_embeddings():
    """
    Create mock embeddings for demonstration
    
    We'll create simple 3-dimensional vectors that represent:
    - AI/ML topics (high values in position 0)
    - Programming topics (high values in position 1) 
    - Geography topics (high values in position 2)
    """
    print("🎲 Creating mock embeddings...")
    
    # Sample texts with their mock embeddings
    texts_and_embeddings = [
        # AI/ML texts (high in position 0)
        ("Artificial Intelligence is transforming technology", [0.9, 0.1, 0.0]),
        ("Machine learning algorithms predict trends", [0.8, 0.2, 0.0]),
        ("Deep learning requires large datasets", [0.85, 0.15, 0.0]),
        
        # Programming texts (high in position 1)
        ("Python programming is essential for data science", [0.3, 0.9, 0.0]),
        ("JavaScript is widely used for web development", [0.1, 0.8, 0.1]),
        ("Code optimization improves performance", [0.2, 0.85, 0.0]),
        
        # Geography texts (high in position 2)
        ("The weather in Galicia is often rainy", [0.0, 0.1, 0.9]),
        ("Barcelona is a beautiful city in Catalonia", [0.0, 0.0, 0.8]),
        ("Spanish cuisine includes paella and tapas", [0.0, 0.1, 0.85])
    ]
    
    return texts_and_embeddings


def test_complete_system():
    """Test all parts of the embeddings system"""
    print("🧪 Testing Complete Embeddings System...")
    
    # Create mock data
    texts_and_embeddings = create_mock_embeddings()
    
    # Initialize all components
    search_engine = SimilaritySearchEngine()
    clustering = TextClustering(similarity_threshold=0.6)
    cost_analyzer = CostAnalyzer()
    
    # Add embeddings to search engine
    for text, embedding in texts_and_embeddings:
        search_engine.add_embedding(text, embedding)
        # Simulate cost tracking (mock data)
        cost_analyzer.add_request("embedding_generation", len(text.split()) * 2)
    
    print(f"\n📚 Database loaded with {len(search_engine.embeddings_database)} texts")
    
    # Part 2: Test similarity search
    print(f"\n{'='*60}")
    print("🎯 PART 2: SIMILARITY SEARCH")
    print(f"{'='*60}")
    
    test_queries = [
        ("AI and machine learning", [0.9, 0.1, 0.0]),
        ("Programming in Python", [0.2, 0.9, 0.0]),
        ("Travel to Spain", [0.0, 0.0, 0.9])
    ]
    
    for query_text, query_embedding in test_queries:
        results = search_engine.semantic_search(query_text, query_embedding, top_k=3)
        cost_analyzer.add_request("similarity_search", len(query_text.split()) * 2)
    
    # Part 3: Test clustering
    print(f"\n{'='*60}")
    print("🔗 PART 3: TEXT CLUSTERING")
    print(f"{'='*60}")
    
    clusters = clustering.cluster_texts(search_engine.embeddings_database)
    cluster_summary = clustering.get_cluster_summary()
    
    print(f"\n📊 Clustering Summary:")
    for key, value in cluster_summary.items():
        print(f"   {key}: {value}")
    
    # Part 4: Test cost analysis
    print(f"\n{'='*60}")
    print("💰 PART 4: COST ANALYSIS")
    print(f"{'='*60}")
    
    cost_report = cost_analyzer.generate_cost_report()
    print(cost_report)
    
    return search_engine, clustering, cost_analyzer


if __name__ == "__main__":
    print("🎓 Embeddings Creation - Complete System (Parts 2, 3, 4)")
    print("=" * 60)
    
    # Run complete test
    search_engine, clustering, cost_analyzer = test_complete_system()
    
    print(f"\n✅ Complete system test finished successfully!")
    print(f"   All parts working: Similarity Search, Clustering, Cost Analysis")
