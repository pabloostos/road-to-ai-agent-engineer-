#!/usr/bin/env python3
"""
Vector Search System with Pinecone
==================================

This module demonstrates how to build a complete vector search system using:
- OpenAI for generating embeddings
- Pinecone for vector storage and similarity search

Key Concepts:
- Vector embeddings represent text as numerical arrays
- Similarity search finds semantically related content
- Metadata storage enables rich querying capabilities
- Batch operations for efficient data management

Learning Objectives:
- Understand how vector databases work
- Generate and store embeddings
- Perform similarity searches
- Build real-world semantic search applications
"""

import os
import time
import uuid
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import required libraries
try:
    import openai
    import pinecone
    import numpy as np
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Please install: pip install openai pinecone-client numpy")
    exit(1)


class VectorSearchSystem:
    """
    A complete vector search system using OpenAI embeddings and Pinecone.
    
    This class demonstrates:
    1. Embedding generation using OpenAI
    2. Vector storage in Pinecone
    3. Similarity search functionality
    4. Metadata management
    5. Performance optimization
    
    Real-world applications:
    - Semantic search engines
    - Recommendation systems
    - RAG (Retrieval-Augmented Generation)
    - Content similarity analysis
    """
    
    def __init__(self, index_name: str = "ai-knowledge-base"):
        """
        Initialize the vector search system.
        
        Args:
            index_name (str): Name of the Pinecone index to use
        
        This sets up:
        - OpenAI client for embedding generation
        - Pinecone connection and index
        - Configuration for vector operations
        """
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize Pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        
        self.index_name = index_name
        self.embedding_model = "text-embedding-ada-002"
        self.dimension = 1536  # OpenAI ada-002 embedding dimension
        
        # Create or connect to index
        self._setup_index()
        
        print(f"🔍 Vector Search System Initialized")
        print(f"   Index: {index_name}")
        print(f"   Embedding Model: {self.embedding_model}")
        print(f"   Dimension: {self.dimension}")
        print(f"   OpenAI API: {'✅ Available' if os.getenv('OPENAI_API_KEY') else '❌ Not configured'}")
        print(f"   Pinecone API: {'✅ Available' if os.getenv('PINECONE_API_KEY') else '❌ Not configured'}")
    
    def _setup_index(self):
        """Create or connect to Pinecone index."""
        try:
            # Check if index exists
            if self.index_name not in pinecone.list_indexes():
                print(f"📦 Creating new index: {self.index_name}")
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine"  # Best for semantic similarity
                )
                # Wait for index to be ready
                time.sleep(10)
            
            # Connect to index
            self.index = pinecone.Index(self.index_name)
            print(f"✅ Connected to index: {self.index_name}")
            
        except Exception as e:
            print(f"❌ Failed to setup index: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using OpenAI.
        
        Args:
            text (str): Text to convert to embedding
            
        Returns:
            List[float]: Embedding vector (1536 dimensions for ada-002)
            
        Example:
            embedding = system.generate_embedding("Hello world")
            print(f"Embedding length: {len(embedding)}")  # 1536
        """
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            print(f"❌ Failed to generate embedding: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None):
        """
        Add multiple documents to the vector database.
        
        Args:
            documents (List[str]): List of text documents to add
            metadata (List[Dict]): Optional metadata for each document
            
        This function:
        1. Generates embeddings for all documents
        2. Creates unique IDs for each document
        3. Stores vectors with metadata in Pinecone
        4. Handles batch operations efficiently
        
        Example:
            docs = ["AI is amazing", "Machine learning is powerful"]
            system.add_documents(docs)
        """
        print(f"📝 Adding {len(documents)} documents to vector database...")
        
        try:
            # Generate embeddings for all documents
            print("   Generating embeddings...")
            embeddings = []
            for i, doc in enumerate(documents):
                print(f"     Processing document {i+1}/{len(documents)}: {doc[:50]}...")
                embedding = self.generate_embedding(doc)
                embeddings.append(embedding)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                # Create unique ID
                vector_id = str(uuid.uuid4())
                
                # Prepare metadata
                doc_metadata = {
                    "text": doc,
                    "index": i,
                    "length": len(doc)
                }
                
                # Add custom metadata if provided
                if metadata and i < len(metadata):
                    doc_metadata.update(metadata[i])
                
                # Create vector tuple (id, embedding, metadata)
                vector = (vector_id, embedding, doc_metadata)
                vectors.append(vector)
            
            # Upload to Pinecone in batches
            print("   Uploading to Pinecone...")
            batch_size = 100  # Pinecone recommended batch size
            
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
                print(f"     Uploaded batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size}")
            
            print(f"✅ Successfully added {len(documents)} documents")
            
        except Exception as e:
            print(f"❌ Failed to add documents: {e}")
            raise
    
    def search(self, query: str, top_k: int = 3, include_metadata: bool = True) -> List[Dict]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            include_metadata (bool): Whether to include metadata in results
            
        Returns:
            List[Dict]: List of search results with scores and metadata
            
        This function:
        1. Converts query to embedding
        2. Searches for similar vectors in Pinecone
        3. Returns ranked results with similarity scores
        
        Example:
            results = system.search("How do computers learn?")
            for result in results:
                print(f"Score: {result['score']:.3f}")
                print(f"Text: {result['metadata']['text']}")
        """
        print(f"🔍 Searching for: '{query}'")
        
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)
            
            # Search in Pinecone
            search_results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=include_metadata
            )
            
            # Format results
            results = []
            for match in search_results.matches:
                result = {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                results.append(result)
            
            print(f"✅ Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            raise
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector database index.
        
        Returns:
            Dict[str, Any]: Index statistics including total vectors, dimension, etc.
            
        Example:
            stats = system.get_index_stats()
            print(f"Total vectors: {stats['total_vector_count']}")
        """
        try:
            # Get index statistics
            stats = self.index.describe_index_stats()
            
            print(f"📊 Index Statistics:")
            print(f"   Total Vectors: {stats.total_vector_count}")
            print(f"   Dimension: {stats.dimension}")
            print(f"   Index Type: {stats.index_type}")
            
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_type": stats.index_type,
                "namespaces": stats.namespaces
            }
            
        except Exception as e:
            print(f"❌ Failed to get index stats: {e}")
            return {}
    
    def delete_index(self):
        """Delete the Pinecone index (use with caution!)."""
        try:
            pinecone.delete_index(self.index_name)
            print(f"🗑️  Deleted index: {self.index_name}")
        except Exception as e:
            print(f"❌ Failed to delete index: {e}")


def main():
    """
    Main function to demonstrate the vector search system.
    
    This runs a complete example showing:
    1. Creating a vector search system
    2. Adding AI knowledge base documents
    3. Performing semantic searches
    4. Analyzing search results
    """
    print("🚀 Vector Search System Demo")
    print("=" * 50)
    
    # Initialize the system
    system = VectorSearchSystem("ai-knowledge-demo")
    
    # Sample AI knowledge base documents
    ai_documents = [
        "Artificial Intelligence (AI) is the simulation of human intelligence in machines.",
        "Machine Learning is a subset of AI that enables computers to learn without explicit programming.",
        "Deep Learning uses neural networks with multiple layers to process complex patterns.",
        "Natural Language Processing (NLP) helps computers understand and generate human language.",
        "Computer Vision enables machines to interpret and analyze visual information.",
        "Reinforcement Learning teaches agents to make decisions through trial and error.",
        "Neural Networks are computing systems inspired by biological brain structures.",
        "Data Science combines statistics, programming, and domain expertise to extract insights.",
        "Big Data refers to extremely large datasets that require special processing techniques.",
        "Cloud Computing provides on-demand access to computing resources over the internet."
    ]
    
    # Add documents to vector database
    print("\n📝 Adding AI knowledge base documents...")
    system.add_documents(ai_documents)
    
    # Get index statistics
    print("\n📊 Index Statistics:")
    stats = system.get_index_stats()
    
    # Test search queries
    print("\n🔍 Testing Semantic Search:")
    test_queries = [
        "How do computers learn?",
        "What is neural network?",
        "Image recognition technology",
        "Teaching machines to make decisions",
        "Large datasets processing"
    ]
    
    for query in test_queries:
        print(f"\n--- Search: '{query}' ---")
        results = system.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result['score']:.3f}")
            print(f"     Text: {result['metadata']['text']}")
    
    print(f"\n🎉 Vector Search Demo Completed!")
    print(f"💡 Key Insights:")
    print(f"   - Semantic search finds related content even without exact keywords")
    print(f"   - Vector embeddings capture meaning, not just text")
    print(f"   - Similarity scores help rank relevance")
    print(f"   - Metadata enables rich querying and filtering")


if __name__ == "__main__":
    main()
