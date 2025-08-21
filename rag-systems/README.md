# RAG Systems Module

## Overview
This module covers **Retrieval-Augmented Generation (RAG)** - one of the most powerful techniques in modern AI. Learn how to build systems that combine the knowledge retrieval capabilities of vector search with the generative power of large language models.

## 🎯 Learning Objectives
- Understand why RAG matters and when to use it
- Master the complete RAG architecture and components
- Build a working RAG system from scratch
- Implement document chunking, embedding, retrieval, and generation
- Apply best practices for production RAG systems

## 📁 Module Structure
```
rag-systems/
├── theory.md              # Comprehensive RAG theory and concepts
├── exercise.md            # Hands-on exercise instructions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env.example          # Environment variables template
├── data/                 # Raw documents for processing
├── chunks/               # Chunked text (JSONL format)
├── embeddings/           # Vector embeddings (JSONL format)
├── src/                  # Source code
│   ├── 01_chunker.py    # Document chunking
│   ├── 02_embedder.py   # Embedding generation
│   ├── 03_retriever.py  # Vector search
│   ├── 04_generator.py  # RAG answer generation
│   └── rag_system.py    # Complete RAG system
├── results/              # Output files and logs
├── examples/             # Example implementations
└── tests/               # Unit tests
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Add your OpenRouter API key to .env
echo "OPENROUTER_API_KEY=your_api_key_here" >> .env
```

### 2. Prepare Sample Data
```bash
# Create sample documents in data/
echo "Artificial Intelligence is a branch of computer science..." > data/ai_basics.txt
echo "Machine Learning is a subset of AI..." > data/machine_learning.txt
```

### 3. Run the Exercise
```bash
cd src
python rag_system.py
```

## 📚 Key Concepts Covered

### RAG Fundamentals
- **Why RAG Matters** - Solving LLM limitations (stale knowledge, hallucinations, context limits)
- **RAG Architecture** - Retriever + Generator pipeline
- **Core Components** - Chunker, Embedder, Vector Index, Prompt Assembler, Generator

### Technical Implementation
- **Document Chunking** - Sliding window with overlap, semantic boundaries
- **Embedding Generation** - Vector representations using Sentence Transformers (free)
- **Vector Search** - Cosine similarity, top-k retrieval
- **Prompt Engineering** - Context injection, citation formatting
- **Answer Generation** - Grounded responses with citations using OpenRouter (free)

### Best Practices
- **Chunking Strategies** - 300-800 tokens with overlap
- **Metadata Management** - Document IDs, timestamps, source tracking
- **Prompt Design** - Clear constraints, citation requirements
- **Cost Optimization** - Caching, batch processing, model selection
- **Evaluation Metrics** - Answer quality, citation accuracy

## 🛠️ Tools & Technologies
- **Sentence Transformers** - Free local embedding generation (`all-MiniLM-L6-v2`)
- **OpenRouter API** - Free LLM generation (`mistralai/mistral-small-3.2-24b-instruct:free`)
- **NumPy** - Vector operations and similarity calculations
- **TikToken** - Token counting and text processing
- **JSONL** - Efficient data storage format
- **Pathlib** - File system operations

## 📊 Expected Outcomes
After completing this module, you'll be able to:
- ✅ Build a complete RAG pipeline from scratch
- ✅ Implement document chunking and embedding generation
- ✅ Create effective vector search and retrieval systems
- ✅ Generate grounded answers with proper citations
- ✅ Optimize RAG systems for cost and performance
- ✅ Deploy RAG systems in production environments

## 🔗 Related Modules
- **Embeddings Creation** - Vector representations and similarity
- **Vector Databases** - Scalable vector storage and search
- **Prompt Engineering** - Effective prompt design for RAG
- **Production Deployment** - Scaling RAG systems

## 💡 Real-World Applications
- **Documentation Q&A** - Company knowledge bases
- **Customer Support** - FAQ and troubleshooting systems
- **Research Assistants** - Academic paper analysis
- **Legal Document Analysis** - Contract and regulation search
- **Medical Information Systems** - Patient care and diagnosis support

## 🎓 Next Steps
After mastering RAG systems, explore:
1. **Advanced RAG** - Multi-modal, hierarchical, conversational RAG
2. **Hybrid Search** - Combining vector and keyword search
3. **RAG Evaluation** - Metrics and benchmarking frameworks
4. **Production RAG** - Scaling, monitoring, and optimization
5. **RAG vs Fine-tuning** - When to use each approach

## 🚀 Why RAG is Revolutionary
RAG represents a paradigm shift in AI applications by:
- **Bridging Knowledge Gaps** - Connecting LLMs to up-to-date information
- **Reducing Hallucinations** - Grounding responses in authoritative sources
- **Enabling Domain Adaptation** - No fine-tuning required for new domains
- **Providing Transparency** - Citations and source attribution
- **Lowering Costs** - Index once, retrieve many times

**Ready to build the future of AI-powered information retrieval?** 🎯✨
