#!/usr/bin/env python3
"""
Step 3: Vector Search (Retriever)
=================================

This script implements vector search to find the most relevant chunks for a query.
We'll use cosine similarity to compare query embeddings with chunk embeddings.

Key Concepts:
- Cosine similarity for vector comparison
- Top-k retrieval
- Query embedding generation
- Similarity scoring and ranking
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ Missing dependencies. Install with: pip install sentence-transformers")
    exit(1)


class VectorRetriever:
    """
    Vector search retriever that finds similar chunks using cosine similarity.
    
    This class handles:
    - Loading embedded chunks from JSONL
    - Generating query embeddings
    - Computing cosine similarity
    - Returning top-k most similar chunks
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector retriever.
        
        Args:
            model_name: Sentence Transformers model to use (same as embedder)
        """
        self.model_name = model_name
        
        print(f"🔄 Loading Sentence Transformers model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Storage for our vector index
        self.texts = []
        self.metadata = []
        self.embeddings = None
        
        print(f"✅ VectorRetriever initialized")
        print(f"   Model: {model_name}")
        print(f"   Dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def load_index(self, embeddings_file: Path) -> bool:
        """
        Load the vector index from embeddings JSONL file.
        
        Args:
            embeddings_file: Path to embeddings JSONL file
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n📚 Loading vector index from: {embeddings_file}")
        
        if not embeddings_file.exists():
            print(f"   ❌ Embeddings file not found")
            return False
        
        try:
            # Load embedded chunks
            texts = []
            metadata = []
            embeddings_list = []
            
            with open(embeddings_file, "r", encoding="utf-8") as f:
                for line in f:
                    chunk = json.loads(line.strip())
                    
                    # Extract components
                    texts.append(chunk["text"])
                    metadata.append({
                        "doc_id": chunk["doc_id"],
                        "chunk_id": chunk["chunk_id"],
                        "tokens": chunk["tokens"],
                        "file_path": chunk["file_path"]
                    })
                    embeddings_list.append(chunk["embedding"])
            
            # Convert to numpy array for efficient computation
            self.texts = texts
            self.metadata = metadata
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
            
            print(f"   ✅ Loaded {len(self.texts)} chunks")
            print(f"   📊 Index shape: {self.embeddings.shape}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error loading index: {e}")
            return False
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a query text.
        
        Args:
            query: The query text to embed
            
        Returns:
            Query embedding as numpy array
        """
        # Generate embedding using the same model
        embedding = self.model.encode([query], convert_to_numpy=True)
        return embedding[0]  # Return first (and only) embedding
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0 to 1, where 1 is most similar)
        """
        # Normalize vectors
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
        
        # Compute cosine similarity
        similarity = np.dot(vec1_norm, vec2_norm)
        return float(similarity)
    
    def search(self, query: str, top_k: int = 3, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search for most similar chunks to a query.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            List of dictionaries with chunk info and similarity scores
        """
        if self.embeddings is None:
            print("❌ No index loaded. Call load_index() first.")
            return []
        
        print(f"\n🔍 Searching for: '{query}'")
        print(f"   Top-k: {top_k}, Threshold: {similarity_threshold}")
        
        # Generate query embedding
        query_embedding = self.embed_query(query)
        
        # Compute similarities with all chunks
        similarities = []
        for i, chunk_embedding in enumerate(self.embeddings):
            similarity = self.cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and take top-k
        results = []
        for i, similarity in similarities:
            if similarity >= similarity_threshold:
                result = {
                    "rank": len(results) + 1,
                    "similarity": similarity,
                    "text": self.texts[i],
                    "metadata": self.metadata[i],
                    "chunk_id": f"{self.metadata[i]['doc_id']}#{self.metadata[i]['chunk_id']}"
                }
                results.append(result)
                
                if len(results) >= top_k:
                    break
        
        # Print results
        print(f"   📊 Found {len(results)} results:")
        for result in results:
            print(f"      {result['rank']}. Score: {result['similarity']:.4f} - {result['chunk_id']}")
            print(f"         Text: {result['text'][:100]}...")
        
        return results
    
    def batch_search(self, queries: List[str], top_k: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for multiple queries at once.
        
        Args:
            queries: List of search queries
            top_k: Number of top results per query
            
        Returns:
            Dictionary mapping queries to their results
        """
        print(f"\n🚀 Batch search for {len(queries)} queries")
        
        results = {}
        for query in queries:
            results[query] = self.search(query, top_k=top_k)
        
        return results


def main():
    """Main function to test the vector retriever."""
    print("🎓 RAG Systems - Step 3: Vector Search")
    print("=" * 50)
    
    # Define paths
    embeddings_file = Path("embeddings/embeddings.jsonl")
    
    # Initialize retriever
    retriever = VectorRetriever(model_name="all-MiniLM-L6-v2")
    
    # Load index
    if not retriever.load_index(embeddings_file):
        print("❌ Failed to load index. Please run Step 2 (embedder) first.")
        return
    
    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What are the types of machine learning?",
        "Explain neural networks",
        "What is natural language processing?"
    ]
    
    print(f"\n🧪 Testing vector search with {len(test_queries)} queries")
    
    # Run searches
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print(f"{'='*60}")
        
        results = retriever.search(query, top_k=2, similarity_threshold=0.3)
        
        if results:
            print(f"\n🎯 Best match: {results[0]['chunk_id']} (score: {results[0]['similarity']:.4f})")
        else:
            print(f"\n❌ No results above threshold")
    
    print(f"\n✅ Step 3 completed successfully!")
    print(f"   Ready for Step 4: RAG Answer Generation")


if __name__ == "__main__":
    main()
