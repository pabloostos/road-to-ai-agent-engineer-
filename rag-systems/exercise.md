# Exercise: Build a Simple RAG System

## Objective
Build a complete RAG (Retrieval-Augmented Generation) system from scratch that demonstrates all the key concepts from the lecture. You'll create a knowledge base about AI topics and build a Q&A system that can answer questions with citations.

## 🎯 Learning Goals
- **Document Chunking**: Split documents into meaningful pieces
- **Embedding Generation**: Convert text chunks to vectors
- **Vector Search**: Find relevant chunks for queries
- **Prompt Engineering**: Create effective RAG prompts
- **Answer Generation**: Generate grounded responses with citations

## 📁 Project Structure
```
rag-systems/
├── data/                   # Raw documents (.txt files)
├── chunks/                 # Chunked text (JSONL format)
├── embeddings/             # Vector embeddings (JSONL format)
├── src/                    # Source code
│   ├── 01_chunker.py      # Document chunking
│   ├── 02_embedder.py     # Embedding generation
│   ├── 03_retriever.py    # Vector search
│   ├── 04_generator.py    # RAG answer generation
│   └── rag_system.py      # Complete RAG system
├── results/                # Output files
└── README.md
```

## 🚀 Exercise Steps

### Step 1: Document Chunking (`01_chunker.py`)
**Goal**: Split documents into semantically meaningful chunks

**Requirements**:
- Implement sliding window chunking (500 tokens, 50 token overlap)
- Preserve document structure and metadata
- Handle different document formats
- Output chunks in JSONL format

**Sample Data**: Create 3-5 text files about AI topics:
- `ai_basics.txt` - Introduction to AI
- `machine_learning.txt` - ML fundamentals
- `deep_learning.txt` - Neural networks
- `nlp.txt` - Natural language processing

### Step 2: Embedding Generation (`02_embedder.py`)
**Goal**: Convert text chunks to vector embeddings

**Requirements**:
- Use Sentence Transformers (`all-MiniLM-L6-v2`) - **FREE**
- Implement batch processing for efficiency
- Add metadata (doc_id, chunk_id, timestamp)
- Cache embeddings to avoid re-computation
- Handle API errors gracefully

### Step 3: Vector Search (`03_retriever.py`)
**Goal**: Find most relevant chunks for a query

**Requirements**:
- Implement cosine similarity search
- Return top-k most similar chunks
- Include similarity scores and metadata
- Support different search parameters (k, threshold)

### Step 4: RAG Answer Generation (`04_generator.py`)
**Goal**: Generate grounded answers with citations

**Requirements**:
- Create effective system and user prompts
- Retrieve relevant context chunks
- Generate answers using OpenRouter's free Mistral model
- Include proper citations (doc_id#chunk_id)
- Handle cases with insufficient context

### Step 5: Complete RAG System (`rag_system.py`)
**Goal**: Integrate all components into a working system

**Requirements**:
- Single interface for the entire RAG pipeline
- Interactive Q&A mode
- Batch processing for multiple questions
- Logging and evaluation metrics
- Cost tracking and optimization

## 📋 Sample Questions to Test
1. "What is artificial intelligence?"
2. "How do neural networks work?"
3. "What are the main types of machine learning?"
4. "How does natural language processing work?"
5. "What is the difference between AI and ML?"

## 🎯 Success Criteria
✅ **Chunking**: Documents properly split into meaningful chunks  
✅ **Embeddings**: Chunks converted to vectors with metadata  
✅ **Retrieval**: Relevant chunks found for test queries  
✅ **Generation**: Grounded answers with proper citations  
✅ **Integration**: Complete pipeline working end-to-end  
✅ **Error Handling**: Graceful handling of edge cases  

## 💡 Bonus Challenges
- **Hybrid Search**: Combine vector search with keyword matching
- **Chunk Optimization**: Implement smart chunking strategies
- **Caching System**: Cache embeddings and retrieval results
- **Evaluation Metrics**: Track answer quality and citation accuracy
- **Web Interface**: Simple web UI for the RAG system

## 🔧 Technical Requirements
- **APIs**: OpenRouter for LLM generation (embeddings are free with Sentence Transformers)
- **Libraries**: `requests`, `numpy`, `json`, `pathlib`, `sentence-transformers`
- **Data Formats**: JSONL for chunks and embeddings
- **Error Handling**: Robust error handling and logging
- **Documentation**: Clear code comments and README

## 📊 Expected Output
1. **Chunked Documents**: `chunks/chunks.jsonl`
2. **Embeddings**: `embeddings/embeddings.jsonl`
3. **Search Results**: `results/searches.jsonl`
4. **Q&A Results**: `results/answers.jsonl`
5. **System Logs**: `results/rag_system.log`

## 🎓 Learning Outcomes
By completing this exercise, you'll understand:
- How to build a complete RAG pipeline
- Best practices for document chunking
- Effective vector search implementation
- Prompt engineering for RAG systems
- Cost optimization and performance tuning
- Real-world RAG system deployment considerations

## 🚀 Getting Started
1. Set up the project structure
2. Create sample documents in `data/`
3. Implement each component step by step
4. Test with sample questions
5. Optimize and improve the system

## ✅ Complete Implementation Status
**All steps have been implemented and tested!**

### 🎯 Quick Test Commands
```bash
# Test individual steps
python src/01_chunker.py
python src/02_embedder.py  
python src/03_retriever.py
python src/04_generator.py

# Test complete system
python src/rag_system.py
```

### 🆓 Free Implementation Features
- ✅ **Free Embeddings**: Sentence Transformers for local generation
- ✅ **Free LLM**: OpenRouter's Mistral model for answers
- ✅ **Demo Mode**: Works without API keys for learning
- ✅ **Complete Pipeline**: All 4 RAG steps working
- ✅ **Citation Support**: (doc_id#chunk_id) format
- ✅ **Production Ready**: Scalable and well-documented

**Ready to build your first RAG system? Let's get started!** 🎯✨
