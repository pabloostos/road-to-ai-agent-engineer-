#!/usr/bin/env python3
"""
Step 1: Document Chunking
=========================

This script splits documents into semantically meaningful chunks.
We'll use a simple sliding window approach with overlap to ensure
context is preserved across chunk boundaries.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

try:
    import tiktoken
except ImportError:
    print("❌ tiktoken not found. Install with: pip install tiktoken")
    exit(1)


class DocumentChunker:
    """Simple document chunker that splits text into overlapping chunks."""
    
    def __init__(self, max_tokens: int = 500, overlap_tokens: int = 50):
        """Initialize the chunker with configurable parameters."""
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")  # Same as GPT-4
        
        print(f"✅ DocumentChunker initialized")
        print(f"   Max tokens per chunk: {max_tokens}")
        print(f"   Overlap tokens: {overlap_tokens}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken."""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks using sliding window."""
        print(f"🔄 Chunking text ({self.count_tokens(text)} tokens)...")
        
        # Simple tokenization (split on whitespace, preserve newlines)
        tokens = re.findall(r"\S+|\n", text)
        chunks = []
        
        # Sliding window approach
        i = 0
        while i < len(tokens):
            # Take a window of max_tokens
            window = tokens[i:i + self.max_tokens]
            
            # Join tokens back into text
            chunk_text = ""
            for token in window:
                if token == "\n":
                    chunk_text += "\n"
                else:
                    chunk_text += token + " "
            
            chunk_text = chunk_text.strip()
            
            # Only add non-empty chunks
            if chunk_text:
                chunks.append(chunk_text)
            
            # Move window forward by step size
            i += self.max_tokens - self.overlap_tokens
        
        print(f"   ✅ Created {len(chunks)} chunks")
        return chunks
    
    def process_document(self, file_path: Path, doc_id: str = None) -> List[Dict[str, Any]]:
        """Process a single document file into chunks."""
        if doc_id is None:
            doc_id = file_path.stem
        
        print(f"\n📄 Processing document: {file_path.name}")
        
        try:
            # Read the document
            content = file_path.read_text(encoding="utf-8")
            
            # Chunk the text
            chunks = self.chunk_text(content)
            
            # Create chunk records with metadata
            chunk_records = []
            for i, chunk in enumerate(chunks):
                record = {
                    "doc_id": doc_id,
                    "chunk_id": i,
                    "text": chunk,
                    "tokens": self.count_tokens(chunk),
                    "timestamp": datetime.now().isoformat(),
                    "file_path": str(file_path)
                }
                chunk_records.append(record)
            
            print(f"   📊 Created {len(chunk_records)} chunks")
            return chunk_records
            
        except Exception as e:
            print(f"   ❌ Error processing {file_path.name}: {e}")
            return []
    
    def process_directory(self, data_dir: Path, output_file: Path) -> int:
        """Process all text files in a directory and save chunks to JSONL."""
        print(f"\n🚀 Processing directory: {data_dir}")
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        all_chunks = []
        
        # Process each text file
        for file_path in data_dir.glob("*.txt"):
            if file_path.is_file():
                chunks = self.process_document(file_path)
                all_chunks.extend(chunks)
        
        # Save to JSONL file
        print(f"\n💾 Saving {len(all_chunks)} chunks to {output_file}")
        
        with open(output_file, "w", encoding="utf-8") as f:
            for chunk in all_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        print(f"   ✅ Successfully saved chunks")
        
        # Print summary
        total_tokens = sum(chunk["tokens"] for chunk in all_chunks)
        print(f"\n📊 Summary: {len(all_chunks)} chunks, {total_tokens:,} total tokens")
        
        return len(all_chunks)


def main():
    """Main function to run the document chunking process."""
    print("🎓 RAG Systems - Step 1: Document Chunking")
    print("=" * 50)
    
    # Define paths
    data_dir = Path("data")
    chunks_dir = Path("chunks")
    output_file = chunks_dir / "chunks.jsonl"
    
    # Check if data directory exists
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Initialize chunker
    chunker = DocumentChunker(max_tokens=500, overlap_tokens=50)
    
    # Process documents
    total_chunks = chunker.process_directory(data_dir, output_file)
    
    if total_chunks > 0:
        print(f"\n✅ Step 1 completed successfully!")
        print(f"   Ready for Step 2: Embedding Generation")
    else:
        print(f"\n❌ No chunks created. Check your data files.")


if __name__ == "__main__":
    main()

