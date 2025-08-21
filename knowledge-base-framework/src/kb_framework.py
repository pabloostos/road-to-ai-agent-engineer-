#!/usr/bin/env python3
"""
Step 1: Universal Knowledge Base Framework
=========================================
Main framework class that can create and query knowledge bases from any text files.
This framework is designed to be reusable for any domain or content type.

Key Features:
- Accept any .txt files as input
- Automatically process and embed them using Sentence Transformers (FREE)
- Create searchable knowledge bases
- Support multiple knowledge bases simultaneously
- Provide a simple interface for querying
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import tiktoken

from sentence_transformers import SentenceTransformer

class UniversalKnowledgeBase:
    """
    Universal Knowledge Base Framework
    
    This class provides a flexible framework for creating and querying knowledge bases
    from any text files. It uses Sentence Transformers for free embedding generation
    and supports multiple knowledge bases simultaneously.
    
    🎯 Key Innovations:
    - FREE embeddings using Sentence Transformers (no API costs)
    - Universal input: accepts any .txt files
    - Multiple knowledge bases: can handle many domains
    - Simple interface: easy to create and query
    - Metadata tracking: full source and context information
    """
    
    def __init__(self, 
                 embedding_model: str = "all-MiniLM-L6-v2",
                 chunk_size: int = 500,
                 overlap_size: int = 50,
                 similarity_threshold: float = 0.3):
        """
        Initialize the Universal Knowledge Base Framework.
        
        Args:
            embedding_model: Sentence Transformers model name (FREE)
            chunk_size: Maximum tokens per chunk
            overlap_size: Token overlap between chunks  
            similarity_threshold: Minimum similarity for retrieval
            
        🎯 Why these parameters matter:
        - embedding_model: "all-MiniLM-L6-v2" is free, fast, and produces 384-dim vectors
        - chunk_size: 500 tokens is optimal for most content (not too short, not too long)
        - overlap_size: 50 tokens ensures context is preserved across chunk boundaries
        - similarity_threshold: 0.3 filters out low-quality matches
        """
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.similarity_threshold = similarity_threshold
        
        # 🔧 Initialize Sentence Transformers (FREE - no API costs!)
        print(f"🔧 Initializing embedding model: {embedding_model}")
        print("   💡 This is FREE - no API costs for embeddings!")
        self.sentence_model = SentenceTransformer(embedding_model)
        self.embedding_dimension = self.sentence_model.get_sentence_embedding_dimension()
        
        # 🔤 Initialize tokenizer for chunking
        # We use tiktoken for consistent tokenization (same as GPT models)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # 📚 Storage for knowledge bases in memory
        self.knowledge_bases = {}
        self.kb_metadata = {}
        
        # 📁 Base directory for storing knowledge bases on disk
        self.kb_base_dir = Path("knowledge_bases")
        self.kb_base_dir.mkdir(exist_ok=True)
        
        print(f"✅ Framework initialized successfully!")
        print(f"   📊 Embedding dimension: {self.embedding_dimension}")
        print(f"   📁 Storage directory: {self.kb_base_dir}")
        print(f"   🔤 Tokenizer: cl100k_base (GPT-compatible)")
    
    def create_knowledge_base(self, name: str, data_dir: str) -> bool:
        """
        Create a knowledge base from text files in a directory.
        
        This is the main method that orchestrates the entire KB creation process:
        1. Find all .txt files in the directory
        2. Process each file into chunks
        3. Generate embeddings for each chunk
        4. Store everything with metadata
        
        Args:
            name: Name of the knowledge base (e.g., "ai_knowledge", "cooking_recipes")
            data_dir: Directory containing .txt files
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n🚀 Creating knowledge base: {name}")
        print("=" * 50)
        
        # 🔍 Step 1: Validate inputs
        data_path = Path(data_dir)
        if not data_path.exists():
            print(f"❌ Data directory not found: {data_dir}")
            return False
        
        # 📄 Step 2: Find all .txt files
        txt_files = list(data_path.glob("*.txt"))
        if not txt_files:
            print(f"❌ No .txt files found in: {data_dir}")
            return False
        
        print(f"📄 Found {len(txt_files)} text files:")
        for file_path in txt_files:
            print(f"   • {file_path.name}")
        
        # 📁 Step 3: Create knowledge base directory
        kb_dir = self.kb_base_dir / name
        kb_dir.mkdir(exist_ok=True)
        
        # 🔄 Step 4: Process all files
        all_chunks = []
        all_embeddings = []
        
        for file_path in txt_files:
            print(f"\n📖 Processing: {file_path.name}")
            
            # Process file into chunks
            chunks = self._process_file(file_path)
            all_chunks.extend(chunks)
            
            # Generate embeddings for chunks
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = self._generate_embeddings(chunk_texts)
            all_embeddings.extend(embeddings)
            
            print(f"   ✅ Created {len(chunks)} chunks, {len(embeddings)} embeddings")
        
        # 💾 Step 5: Save knowledge base metadata
        kb_data = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dimension,
            "chunk_size": self.chunk_size,
            "overlap_size": self.overlap_size,
            "total_files": len(txt_files),
            "total_chunks": len(all_chunks),
            "files": [f.name for f in txt_files]
        }
        
        # Save metadata to JSON file
        with open(kb_dir / "metadata.json", "w") as f:
            json.dump(kb_data, f, indent=2)
        
        # 💾 Step 6: Save chunks and embeddings
        # We use JSONL format for efficient storage and streaming
        with open(kb_dir / "chunks.jsonl", "w") as f:
            for chunk in all_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        with open(kb_dir / "embeddings.jsonl", "w") as f:
            for chunk, embedding in zip(all_chunks, all_embeddings):
                chunk["embedding"] = embedding
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        # 🧠 Step 7: Store in memory for quick access
        self.knowledge_bases[name] = {
            "chunks": all_chunks,
            "embeddings": np.array(all_embeddings, dtype=np.float32),
            "metadata": kb_data
        }
        
        # 📊 Step 8: Print summary
        print(f"\n✅ Knowledge base '{name}' created successfully!")
        print(f"   📊 Files processed: {len(txt_files)}")
        print(f"   📄 Total chunks: {len(all_chunks)}")
        print(f"   🔢 Total embeddings: {len(all_embeddings)}")
        print(f"   💾 Storage location: {kb_dir}")
        print(f"   🧠 Loaded in memory: Yes")
        
        return True
    
    def _process_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Process a single text file into chunks with metadata.
        
        This method handles the core text processing:
        1. Read the file content
        2. Split it into overlapping chunks
        3. Add metadata to each chunk
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of chunk dictionaries with metadata
        """
        # 📖 Read file content
        content = file_path.read_text(encoding="utf-8")
        
        # ✂️ Split into chunks
        chunks = self._chunk_text(content)
        
        # 🏷️ Add metadata to each chunk
        chunk_records = []
        for i, chunk_text in enumerate(chunks):
            chunk_record = {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "chunk_id": i,
                "text": chunk_text,
                "tokens": len(self.tokenizer.encode(chunk_text)),
                "created_at": datetime.now().isoformat()
            }
            chunk_records.append(chunk_record)
        
        return chunk_records
    
    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        This is a crucial method that determines how we break down text:
        - Uses tiktoken for consistent tokenization
        - Creates overlapping chunks to preserve context
        - Handles edge cases gracefully
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        # 🔤 Tokenize the text using tiktoken (same as GPT models)
        tokens = self.tokenizer.encode(text)
        
        chunks = []
        i = 0
        
        while i < len(tokens):
            # 📦 Get chunk tokens (up to chunk_size)
            chunk_tokens = tokens[i:i + self.chunk_size]
            
            # 🔄 Decode back to text
            chunk_text = self.tokenizer.decode(chunk_tokens).strip()
            
            # ✅ Only add non-empty chunks
            if chunk_text:
                chunks.append(chunk_text)
            
            # ➡️ Move to next chunk with overlap
            # This ensures context is preserved across chunk boundaries
            i += self.chunk_size - self.overlap_size
        
        return chunks
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        This method uses Sentence Transformers to create vector representations:
        - FREE: No API costs
        - Fast: Local processing
        - Consistent: Same model for all embeddings
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors (384-dimensional for all-MiniLM-L6-v2)
        """
        # 🔢 Generate embeddings using Sentence Transformers (FREE!)
        embeddings = self.sentence_model.encode(texts, convert_to_numpy=False)
        
        # 🔄 Convert to list format for storage
        return [embedding.tolist() for embedding in embeddings]
    
    def query_knowledge_base(self, name: str, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Query a knowledge base with a question.
        
        This method implements semantic search:
        1. Generate embedding for the query
        2. Calculate similarity with all chunks
        3. Return top-k most similar results
        
        Args:
            name: Name of the knowledge base
            query: Query text
            top_k: Number of top results to return
            
        Returns:
            Dictionary with query results and metadata
        """
        # 🔍 Check if knowledge base exists
        if name not in self.knowledge_bases:
            return {
                "error": f"Knowledge base '{name}' not found. Available: {list(self.knowledge_bases.keys())}",
                "results": [],
                "metadata": {}
            }
        
        # 📚 Get knowledge base data
        kb_data = self.knowledge_bases[name]
        chunks = kb_data["chunks"]
        embeddings = kb_data["embeddings"]
        
        # 🔢 Generate query embedding
        query_embedding = self.sentence_model.encode([query], convert_to_numpy=True)[0]
        
        # 🎯 Calculate similarities with all chunks
        similarities = []
        for i, chunk_embedding in enumerate(embeddings):
            similarity = self._cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((i, similarity))
        
        # 📊 Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 🏆 Get top results above threshold
        results = []
        for i, similarity in similarities[:top_k]:
            if similarity >= self.similarity_threshold:
                result = {
                    "rank": len(results) + 1,
                    "similarity": float(similarity),
                    "text": chunks[i]["text"],
                    "file_name": chunks[i]["file_name"],
                    "chunk_id": chunks[i]["chunk_id"],
                    "tokens": chunks[i]["tokens"]
                }
                results.append(result)
        
        # 📋 Prepare response metadata
        metadata = {
            "knowledge_base": name,
            "query": query,
            "total_chunks": len(chunks),
            "results_returned": len(results),
            "top_similarity": float(similarities[0][1]) if similarities else 0.0,
            "similarity_threshold": self.similarity_threshold,
            "query_timestamp": datetime.now().isoformat()
        }
        
        return {
            "results": results,
            "metadata": metadata
        }
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Cosine similarity measures the angle between vectors:
        - Range: -1 to 1 (1 = identical, 0 = orthogonal, -1 = opposite)
        - Normalized: Handles different vector magnitudes
        - Efficient: Fast computation with NumPy
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # 📏 Normalize vectors (unit length)
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)  # +1e-8 prevents division by zero
        vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
        
        # 🔢 Calculate cosine similarity (dot product of normalized vectors)
        return float(np.dot(vec1_norm, vec2_norm))
    
    def list_knowledge_bases(self) -> List[Dict[str, Any]]:
        """
        List all available knowledge bases.
        
        Returns:
            List of knowledge base information
        """
        kb_list = []
        
        for name, kb_data in self.knowledge_bases.items():
            kb_info = {
                "name": name,
                "total_chunks": len(kb_data["chunks"]),
                "embedding_model": kb_data["metadata"]["embedding_model"],
                "embedding_dimension": kb_data["metadata"]["embedding_dimension"],
                "total_files": kb_data["metadata"]["total_files"],
                "created_at": kb_data["metadata"]["created_at"]
            }
            kb_list.append(kb_info)
        
        return kb_list
    
    def get_kb_stats(self, name: str) -> Dict[str, Any]:
        """
        Get detailed statistics about a knowledge base.
        
        Args:
            name: Name of the knowledge base
            
        Returns:
            Dictionary with KB statistics
        """
        if name not in self.knowledge_bases:
            return {"error": f"Knowledge base '{name}' not found"}
        
        kb_data = self.knowledge_bases[name]
        chunks = kb_data["chunks"]
        
        # 📊 Calculate statistics
        total_tokens = sum(chunk["tokens"] for chunk in chunks)
        avg_tokens_per_chunk = total_tokens / len(chunks) if chunks else 0
        
        # 📁 File statistics
        file_counts = {}
        for chunk in chunks:
            file_name = chunk["file_name"]
            file_counts[file_name] = file_counts.get(file_name, 0) + 1
        
        stats = {
            "name": name,
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "average_tokens_per_chunk": round(avg_tokens_per_chunk, 2),
            "files": file_counts,
            "embedding_model": kb_data["metadata"]["embedding_model"],
            "embedding_dimension": kb_data["metadata"]["embedding_dimension"],
            "created_at": kb_data["metadata"]["created_at"]
        }
        
        return stats
    
    def load_existing_knowledge_bases(self) -> int:
        """
        Load existing knowledge bases from disk.
        
        This method allows us to load previously created KBs without recreating them.
        
        Returns:
            Number of knowledge bases loaded
        """
        loaded_count = 0
        
        for kb_dir in self.kb_base_dir.iterdir():
            if kb_dir.is_dir():
                kb_name = kb_dir.name
                metadata_file = kb_dir / "metadata.json"
                embeddings_file = kb_dir / "embeddings.jsonl"
                
                if metadata_file.exists() and embeddings_file.exists():
                    try:
                        # 📋 Load metadata
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                        
                        # 📄 Load chunks and embeddings
                        chunks = []
                        embeddings_list = []
                        
                        with open(embeddings_file, "r") as f:
                            for line in f:
                                chunk_data = json.loads(line.strip())
                                embedding = chunk_data.pop("embedding")
                                chunks.append(chunk_data)
                                embeddings_list.append(embedding)
                        
                        # 🧠 Store in memory
                        self.knowledge_bases[kb_name] = {
                            "chunks": chunks,
                            "embeddings": np.array(embeddings_list, dtype=np.float32),
                            "metadata": metadata
                        }
                        
                        loaded_count += 1
                        print(f"📚 Loaded existing KB: {kb_name} ({len(chunks)} chunks)")
                        
                    except Exception as e:
                        print(f"⚠️  Error loading KB {kb_name}: {e}")
        
        return loaded_count

def main():
    """Demo the Universal Knowledge Base Framework."""
    print("🎯 Universal Knowledge Base Framework Demo")
    print("=" * 60)
    
    # 🔧 Initialize framework
    kb = UniversalKnowledgeBase()
    
    # 📚 Load existing knowledge bases
    loaded_count = kb.load_existing_knowledge_bases()
    print(f"📚 Loaded {loaded_count} existing knowledge bases")
    
    # 📋 List available knowledge bases
    kbs = kb.list_knowledge_bases()
    print(f"\n📋 Available Knowledge Bases:")
    for kb_info in kbs:
        print(f"   • {kb_info['name']}: {kb_info['total_chunks']} chunks")
    
    if kbs:
        # 🔍 Demo queries
        print(f"\n🔍 Demo Queries:")
        print("-" * 30)
        
        # Query AI knowledge base
        if "ai_knowledge" in [kb["name"] for kb in kbs]:
            print("\n❓ Query: What is machine learning?")
            results = kb.query_knowledge_base("ai_knowledge", "What is machine learning?")
            if "error" not in results:
                for result in results["results"][:2]:
                    print(f"   📄 {result['file_name']} (score: {result['similarity']:.3f})")
                    print(f"      {result['text'][:100]}...")
        
        # Query cooking knowledge base
        if "cooking_recipes" in [kb["name"] for kb in kbs]:
            print("\n❓ Query: How to make pasta?")
            results = kb.query_knowledge_base("cooking_recipes", "How to make pasta?")
            if "error" not in results:
                for result in results["results"][:2]:
                    print(f"   📄 {result['file_name']} (score: {result['similarity']:.3f})")
                    print(f"      {result['text'][:100]}...")
    
    print(f"\n✅ Framework demo completed!")

if __name__ == "__main__":
    main()
