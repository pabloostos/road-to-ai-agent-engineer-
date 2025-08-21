#!/usr/bin/env python3
"""
Step 4: RAG Answer Generation
============================
This script implements the final step of our RAG system.
It combines retrieval (from Step 3) with LLM generation to create
grounded answers using OpenRouter's free Mistral model.
"""
import os
import json
import numpy as np
import requests
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime

from sentence_transformers import SentenceTransformer

class RAGAnswerGenerator:
    """RAG system that retrieves relevant chunks and generates grounded answers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.texts = []
        self.metadata = []
        self.embeddings = None
        
        # OpenRouter configuration
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_base = "https://openrouter.ai/api/v1"
        self.model_name_llm = "mistralai/mistral-small-3.2-24b-instruct:free"
        
        if not self.api_key:
            print("⚠️  Warning: OPENROUTER_API_KEY not found in environment")
            print("   The system will work but won't generate actual answers")
    
    def load_index(self, embeddings_file: Path) -> bool:
        """Load the vector index from embeddings file."""
        if not embeddings_file.exists():
            print(f"❌ Embeddings file not found: {embeddings_file}")
            return False
            
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
        
        print(f"✅ Loaded {len(self.texts)} chunks into RAG index")
        return True
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for the query."""
        embedding = self.model.encode([query], convert_to_numpy=True)
        return embedding[0]
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
        return float(np.dot(vec1_norm, vec2_norm))
    
    def retrieve(self, query: str, top_k: int = 3, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """Retrieve the most relevant chunks for a query."""
        if self.embeddings is None:
            return []
        
        query_embedding = self.embed_query(query)
        similarities = []
        
        for i, chunk_embedding in enumerate(self.embeddings):
            similarity = self.cosine_similarity(query_embedding, chunk_embedding)
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
    
    def build_prompt(self, context_chunks: List[Dict], question: str) -> str:
        """Build a structured prompt with retrieved context."""
        # System prompt with clear instructions
        system_prompt = """You are a helpful AI assistant that answers questions based ONLY on the provided context. 

IMPORTANT RULES:
1. Use ONLY the information provided in the context
2. If the answer is not in the context, say "I don't have enough information to answer this question"
3. Always cite your sources using the format (doc_id#chunk_id)
4. Be concise but informative
5. Do not make up information or add external knowledge

Context information:"""

        # Format context chunks with scores and citations
        context_block = "\n\n".join([
            f"[Score: {chunk['similarity']:.3f}] [{chunk['chunk_id']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # User prompt with question
        user_prompt = f"""Question: {question}

Please answer based on the context above. Include citations like (doc_id#chunk_id) when referencing information."""
        
        return system_prompt, context_block, user_prompt
    
    def generate_answer(self, question: str, top_k: int = 3) -> Tuple[str, List[Dict], Dict]:
        """Generate a grounded answer using RAG."""
        # Step 1: Retrieve relevant chunks
        retrieved_chunks = self.retrieve(question, top_k=top_k, similarity_threshold=0.3)
        
        if not retrieved_chunks:
            return "I don't have enough information to answer this question.", [], {}
        
        # Step 2: Build the prompt
        system_prompt, context_block, user_prompt = self.build_prompt(retrieved_chunks, question)
        
        # Step 3: Generate answer using OpenRouter
        try:
            answer = self._call_openrouter(system_prompt, context_block, user_prompt)
        except Exception as e:
            print(f"⚠️  Error calling OpenRouter: {e}")
            answer = f"[DEMO MODE] Based on the retrieved context, here's what I found:\n\n"
            for chunk in retrieved_chunks:
                answer += f"• From {chunk['chunk_id']}: {chunk['text'][:100]}...\n"
            answer += "\n[Note: This is a demo response. Set OPENROUTER_API_KEY for real answers]"
        
        # Step 4: Prepare response metadata
        response_metadata = {
            "question": question,
            "retrieved_chunks": len(retrieved_chunks),
            "top_similarity": retrieved_chunks[0]["similarity"] if retrieved_chunks else 0.0,
            "model_used": self.model_name_llm,
            "timestamp": datetime.now().isoformat()
        }
        
        return answer, retrieved_chunks, response_metadata
    
    def _call_openrouter(self, system_prompt: str, context_block: str, user_prompt: str) -> str:
        """Call OpenRouter API to generate the answer."""
        if not self.api_key:
            raise Exception("OpenRouter API key not configured")
        
        # Combine system prompt and context
        full_system = f"{system_prompt}\n\n{context_block}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://rag-systems-demo.com",
            "X-Title": "RAG Systems Demo"
        }
        
        data = {
            "model": self.model_name_llm,
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
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
    
    def batch_answer(self, questions: List[str], top_k: int = 3) -> List[Dict[str, Any]]:
        """Generate answers for multiple questions."""
        results = []
        
        for question in questions:
            answer, chunks, metadata = self.generate_answer(question, top_k=top_k)
            results.append({
                "question": question,
                "answer": answer,
                "retrieved_chunks": chunks,
                "metadata": metadata
            })
        
        return results

def main():
    """Test the RAG answer generator."""
    print("🎯 Step 4: RAG Answer Generation")
    print("=" * 50)
    
    # Initialize the RAG system
    rag = RAGAnswerGenerator()
    
    # Load the embeddings index
    embeddings_file = Path("embeddings/embeddings.jsonl")
    if not rag.load_index(embeddings_file):
        print("❌ Failed to load embeddings. Run Step 2 first!")
        return
    
    # Test questions
    test_questions = [
        "What is artificial intelligence?",
        "What are the three types of machine learning?",
        "How does supervised learning work?",
        "What is natural language processing?",
        "Explain computer vision applications"
    ]
    
    print(f"\n🔍 Testing RAG with {len(test_questions)} questions...")
    print("Using OpenRouter's free Mistral model for generation")
    print("-" * 50)
    
    # Generate answers
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 30)
        
        answer, chunks, metadata = rag.generate_answer(question, top_k=2)
        
        print(f"📄 Answer: {answer}")
        print(f"🔗 Retrieved {len(chunks)} chunks")
        print(f"📊 Top similarity: {metadata['top_similarity']:.3f}")
        
        # Show retrieved chunks
        for chunk in chunks:
            print(f"   • {chunk['chunk_id']} (score: {chunk['similarity']:.3f})")
    
    print(f"\n✅ Step 4 completed successfully!")
    print("🎯 RAG system is now fully functional!")

if __name__ == "__main__":
    main()
