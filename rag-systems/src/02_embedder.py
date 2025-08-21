#!/usr/bin/env python3
"""
Step 2: Embedding Generation
============================

This script converts text chunks into vector embeddings using Sentence Transformers.
We'll use the 'all-MiniLM-L6-v2' model which is free, fast, and produces 384-dimensional vectors.

Key Concepts:
- Local embedding generation (no API costs)
- Batch processing for efficiency
- Metadata preservation
- JSONL output format
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("❌ Missing dependencies. Install with: pip install sentence-transformers numpy")
    exit(1)


class EmbeddingGenerator:
    """
    Generate embeddings for text chunks using Sentence Transformers.
    
    This class handles:
    - Loading and using Sentence Transformers model
    - Batch processing for efficiency
    - Metadata preservation
    - JSONL output formatting
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator.
        
        Args:
            model_name: Sentence Transformers model to use
        """
        self.model_name = model_name
        
        print(f"🔄 Loading Sentence Transformers model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Get model info
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        print(f"✅ EmbeddingGenerator initialized")
        print(f"   Model: {model_name}")
        print(f"   Dimension: {self.dimension}")
        print(f"   Device: {self.model.device}")
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each is a list of floats)
        """
        print(f"🔄 Generating embeddings for {len(texts)} texts...")
        
        start_time = time.time()
        
        # Generate embeddings using Sentence Transformers
        embeddings = self.model.encode(texts, convert_to_numpy=False)
        
        # Convert to list of lists for JSON serialization
        embeddings_list = [embedding.tolist() for embedding in embeddings]
        
        elapsed_time = time.time() - start_time
        print(f"   ✅ Generated {len(embeddings_list)} embeddings in {elapsed_time:.2f}s")
        print(f"   📊 Average time per text: {elapsed_time/len(texts):.3f}s")
        
        return embeddings_list
    
    def process_chunks(self, chunks_file: Path, output_file: Path, batch_size: int = 32) -> int:
        """
        Process chunks from JSONL file and generate embeddings.
        
        Args:
            chunks_file: Input JSONL file with chunks
            output_file: Output JSONL file with embeddings
            batch_size: Number of texts to process at once
            
        Returns:
            Number of embeddings generated
        """
        print(f"\n🚀 Processing chunks from: {chunks_file}")
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load chunks
        chunks = []
        with open(chunks_file, "r", encoding="utf-8") as f:
            for line in f:
                chunk = json.loads(line.strip())
                chunks.append(chunk)
        
        print(f"📊 Loaded {len(chunks)} chunks")
        
        # Extract texts for embedding
        texts = [chunk["text"] for chunk in chunks]
        
        # Generate embeddings in batches
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.embed_texts(batch_texts)
            all_embeddings.extend(batch_embeddings)
            
            print(f"   📦 Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        
        # Combine chunks with embeddings
        embedded_chunks = []
        for chunk, embedding in zip(chunks, all_embeddings):
            embedded_chunk = {
                **chunk,  # Keep all original metadata
                "embedding": embedding,
                "embedding_model": self.model_name,
                "embedding_dimension": self.dimension,
                "embedding_timestamp": datetime.now().isoformat()
            }
            embedded_chunks.append(embedded_chunk)
        
        # Save to JSONL file
        print(f"\n💾 Saving {len(embedded_chunks)} embedded chunks to {output_file}")
        
        with open(output_file, "w", encoding="utf-8") as f:
            for chunk in embedded_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        print(f"   ✅ Successfully saved embedded chunks")
        
        # Print summary
        total_tokens = sum(chunk["tokens"] for chunk in embedded_chunks)
        print(f"\n📊 Summary:")
        print(f"   Chunks processed: {len(embedded_chunks)}")
        print(f"   Total tokens: {total_tokens:,}")
        print(f"   Embedding dimension: {self.dimension}")
        print(f"   Model used: {self.model_name}")
        
        return len(embedded_chunks)


def main():
    """Main function to run the embedding generation process."""
    print("🎓 RAG Systems - Step 2: Embedding Generation")
    print("=" * 50)
    
    # Define paths
    chunks_file = Path("chunks/chunks.jsonl")
    embeddings_dir = Path("embeddings")
    output_file = embeddings_dir / "embeddings.jsonl"
    
    # Check if chunks file exists
    if not chunks_file.exists():
        print(f"❌ Chunks file not found: {chunks_file}")
        print(f"   Please run Step 1 (chunker) first")
        return
    
    # Initialize embedding generator
    embedder = EmbeddingGenerator(model_name="all-MiniLM-L6-v2")
    
    # Process chunks
    total_embeddings = embedder.process_chunks(chunks_file, output_file, batch_size=32)
    
    if total_embeddings > 0:
        print(f"\n✅ Step 2 completed successfully!")
        print(f"   Ready for Step 3: Vector Search")
        print(f"   Output file: {output_file}")
    else:
        print(f"\n❌ No embeddings generated. Check your chunks file.")


if __name__ == "__main__":
    main()
