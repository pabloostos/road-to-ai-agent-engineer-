#!/usr/bin/env python3
"""
Complete RAG System
==================
This script combines all 4 steps of our RAG system into one comprehensive class.
It provides a simple interface for document processing and question answering.
"""
import os
import json
import numpy as np
import requests
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

from sentence_transformers import SentenceTransformer

class CompleteRAGSystem:
    """Complete RAG system that handles document processing and question answering."""
    
    def __init__(self, 
                 embedding_model: str = "all-MiniLM-L6-v2",
                 llm_model: str = "mistralai/mistral-small-3.2-24b-instruct:free",
                 max_tokens: int = 500,
                 overlap_tokens: int = 50):
        """
        Initialize the complete RAG system.
        
        Args:
            embedding_model: Sentence Transformers model for embeddings
            llm_model: OpenRouter model for answer generation
            max_tokens: Maximum tokens per chunk
            overlap_tokens: Overlap between chunks
        """
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        
        # Initialize components
        self.sentence_model = SentenceTransformer(embedding_model)
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_base = "https://openrouter.ai/api/v1"
        
        # Data storage
        self.texts = []
        self.metadata = []
        self.embeddings = None
        
        if not self.api_key:
            print("⚠️  Warning: OPENROUTER_API_KEY not found")
            print("   The system will work in demo mode")
    
    def process_documents(self, data_dir: Path, output_dir: Path) -> bool:
        """
        Process documents through the complete RAG pipeline.
        
        Args:
            data_dir: Directory containing .txt files
            output_dir: Directory to save processed data
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting complete RAG pipeline...")
        print("=" * 50)
        
        # Step 1: Chunk documents
        print("📄 Step 1: Document Chunking")
        chunks_file = output_dir / "chunks" / "chunks.jsonl"
        chunks_file.parent.mkdir(parents=True, exist_ok=True)
        
        all_chunks = []
        for file_path in data_dir.glob("*.txt"):
            content = file_path.read_text(encoding="utf-8")
            chunks = self._chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                chunk_record = {
                    "doc_id": file_path.stem,
                    "chunk_id": i,
                    "text": chunk,
                    "tokens": len(chunk.split()),
                    "timestamp": datetime.now().isoformat(),
                    "file_path": str(file_path)
                }
                all_chunks.append(chunk_record)
        
        # Save chunks
        with open(chunks_file, "w", encoding="utf-8") as f:
            for chunk in all_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        print(f"✅ Created {len(all_chunks)} chunks")
        
        # Step 2: Generate embeddings
        print("\n🔢 Step 2: Embedding Generation")
        embeddings_file = output_dir / "embeddings" / "embeddings.jsonl"
        embeddings_file.parent.mkdir(parents=True, exist_ok=True)
        
        texts = [chunk["text"] for chunk in all_chunks]
        embeddings = self.sentence_model.encode(texts, convert_to_numpy=False)
        
        embedded_chunks = []
        for chunk, embedding in zip(all_chunks, embeddings):
            embedded_chunk = {
                **chunk,
                "embedding": embedding.tolist(),
                "embedding_model": self.embedding_model,
                "embedding_dimension": self.sentence_model.get_sentence_embedding_dimension(),
                "embedding_timestamp": datetime.now().isoformat()
            }
            embedded_chunks.append(embedded_chunk)
        
        # Save embeddings
        with open(embeddings_file, "w", encoding="utf-8") as f:
            for chunk in embedded_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        
        print(f"✅ Generated embeddings for {len(embedded_chunks)} chunks")
        
        # Step 3: Load into memory for querying
        print("\n📚 Step 3: Loading Index")
        self._load_embeddings(embeddings_file)
        
        print("✅ RAG system ready for queries!")
        return True
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        tokens = text.split()
        chunks = []
        i = 0
        
        while i < len(tokens):
            window = tokens[i:i + self.max_tokens]
            chunk_text = " ".join(window).strip()
            if chunk_text:
                chunks.append(chunk_text)
            i += self.max_tokens - self.overlap_tokens
        
        return chunks
    
    def _load_embeddings(self, embeddings_file: Path):
        """Load embeddings into memory."""
        texts = []
        metadata = []
        embeddings_list = []
        
        with open(embeddings_file, "r", encoding="utf-8") as f:
            for line in f:
                chunk = json.loads(line.strip())
                texts.append(chunk["text"])
                metadata.append({
                    "doc_id": chunk["doc_id"],
                    "chunk_id": chunk["chunk_id"],
                    "tokens": chunk["tokens"],
                    "file_path": chunk["file_path"]
                })
                embeddings_list.append(chunk["embedding"])
        
        self.texts = texts
        self.metadata = metadata
        self.embeddings = np.array(embeddings_list, dtype=np.float32)
    
    def query(self, question: str, top_k: int = 3, similarity_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        Args:
            question: The question to ask
            top_k: Number of chunks to retrieve
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dict containing answer, retrieved chunks, and metadata
        """
        if self.embeddings is None:
            return {
                "error": "RAG system not initialized. Run process_documents() first.",
                "answer": None,
                "chunks": [],
                "metadata": {}
            }
        
        # Retrieve relevant chunks
        retrieved_chunks = self._retrieve(question, top_k, similarity_threshold)
        
        if not retrieved_chunks:
            return {
                "answer": "I don't have enough information to answer this question.",
                "chunks": [],
                "metadata": {
                    "question": question,
                    "retrieved_chunks": 0,
                    "top_similarity": 0.0,
                    "model_used": self.llm_model,
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        # Generate answer
        answer = self._generate_answer(question, retrieved_chunks)
        
        # Prepare metadata
        metadata = {
            "question": question,
            "retrieved_chunks": len(retrieved_chunks),
            "top_similarity": retrieved_chunks[0]["similarity"] if retrieved_chunks else 0.0,
            "model_used": self.llm_model,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "answer": answer,
            "chunks": retrieved_chunks,
            "metadata": metadata
        }
    
    def _retrieve(self, query: str, top_k: int, similarity_threshold: float) -> List[Dict]:
        """Retrieve relevant chunks for a query."""
        query_embedding = self.sentence_model.encode([query], convert_to_numpy=True)[0]
        similarities = []
        
        for i, chunk_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((i, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
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
        
        return results
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
        return float(np.dot(vec1_norm, vec2_norm))
    
    def _generate_answer(self, question: str, chunks: List[Dict]) -> str:
        """Generate answer using OpenRouter API."""
        # Build prompt
        system_prompt = """You are a helpful AI assistant that answers questions based ONLY on the provided context.

IMPORTANT RULES:
1. Use ONLY the information provided in the context
2. If the answer is not in the context, say "I don't have enough information to answer this question"
3. Always cite your sources using the format (doc_id#chunk_id)
4. Be concise but informative
5. Do not make up information or add external knowledge

Context information:"""

        context_block = "\n\n".join([
            f"[Score: {chunk['similarity']:.3f}] [{chunk['chunk_id']}]\n{chunk['text']}"
            for chunk in chunks
        ])
        
        user_prompt = f"""Question: {question}

Please answer based on the context above. Include citations like (doc_id#chunk_id) when referencing information."""
        
        # Call OpenRouter API
        try:
            if not self.api_key:
                # Demo mode
                answer = f"[DEMO MODE] Based on the retrieved context:\n\n"
                for chunk in chunks:
                    answer += f"• From {chunk['chunk_id']}: {chunk['text'][:150]}...\n"
                answer += "\n[Note: Set OPENROUTER_API_KEY for real answers]"
                return answer
            
            full_system = f"{system_prompt}\n\n{context_block}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://rag-systems-demo.com",
                "X-Title": "RAG Systems Demo"
            }
            
            data = {
                "model": self.llm_model,
                "messages": [
                    {"role": "system", "content": full_system},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API call failed: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Error generating answer: {e}")
            return f"[ERROR] Failed to generate answer: {str(e)}"
    
    def batch_query(self, questions: List[str], top_k: int = 3) -> List[Dict[str, Any]]:
        """Query multiple questions at once."""
        results = []
        for question in questions:
            result = self.query(question, top_k=top_k)
            results.append(result)
        return results

def main():
    """Demo the complete RAG system."""
    print("🎯 Complete RAG System Demo")
    print("=" * 50)
    
    # Initialize system
    rag = CompleteRAGSystem()
    
    # Check if we have processed data
    data_dir = Path("data")
    output_dir = Path(".")
    embeddings_file = output_dir / "embeddings" / "embeddings.jsonl"
    
    if not embeddings_file.exists():
        print("📄 Processing documents...")
        if not rag.process_documents(data_dir, output_dir):
            print("❌ Failed to process documents")
            return
    else:
        print("📚 Loading existing embeddings...")
        rag._load_embeddings(embeddings_file)
    
    # Test questions
    test_questions = [
        "What is artificial intelligence?",
        "What are the three types of machine learning?",
        "How does supervised learning work?",
        "What is natural language processing?",
        "Explain computer vision applications"
    ]
    
    print(f"\n🔍 Testing with {len(test_questions)} questions...")
    print("Using OpenRouter's free Mistral model")
    print("-" * 50)
    
    # Query the system
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 30)
        
        result = rag.query(question, top_k=2)
        
        print(f"📄 Answer: {result['answer']}")
        print(f"🔗 Retrieved {result['metadata']['retrieved_chunks']} chunks")
        print(f"📊 Top similarity: {result['metadata']['top_similarity']:.3f}")
        
        # Show retrieved chunks
        for chunk in result['chunks']:
            print(f"   • {chunk['chunk_id']} (score: {chunk['similarity']:.3f})")
    
    print(f"\n✅ Complete RAG system demo finished!")
    print("🎯 System is ready for production use!")

if __name__ == "__main__":
    main()
