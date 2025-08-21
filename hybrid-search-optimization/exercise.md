# Exercise: Simple Hybrid Search System

## 🎯 Objective
Build a **simple hybrid search system** that combines BM25 keyword search with vector-based semantic search to demonstrate the power of hybrid approaches.

## 🚀 Key Innovation
Instead of using expensive APIs, we'll create a **FREE hybrid search system** using:
- **BM25** for keyword search (rank_bm25 library)
- **Sentence Transformers** for free embeddings
- **Simple in-memory storage** for demonstration

## 📁 Project Structure
```
hybrid-search-optimization/
├── theory.md                    # Hybrid search theory
├── exercise.md                  # This file
├── requirements.txt             # Dependencies
├── README.md                   # Documentation
├── src/                        # Source code
│   └── hybrid_search.py        # Main hybrid search system
├── data/                       # Sample documents
│   └── sample_docs.txt         # Test documents
└── results/                    # Search results
```

## 🎯 Exercise Steps

### Step 1: Simple Hybrid Search System (`hybrid_search.py`)
**Goal**: Create a hybrid search system that combines BM25 and vector search

**Features**:
- **BM25 Search**: Keyword-based search using rank_bm25
- **Vector Search**: Semantic search using Sentence Transformers (FREE)
- **Score Fusion**: Combine both scores with configurable weights
- **Simple Interface**: Easy-to-use search function
- **Evaluation**: Basic precision/recall metrics

**Requirements**:
- Use `rank_bm25` for keyword search
- Use `sentence-transformers` for free embeddings
- Implement score fusion: `final_score = α * bm25_score + β * vector_score`
- Support configurable weights (α, β)
- Return ranked results with scores

### Step 2: Sample Data & Testing
**Goal**: Test the hybrid search with realistic data

**Sample Documents** (create these):
```
"Affordable hybrid cars under $20,000 with great fuel economy"
"Electric vehicles with long battery life and fast charging"
"Cheap used cars in excellent condition for budget buyers"
"Luxury cars with hybrid engines and premium features"
"Compact SUVs with good safety ratings and reliability"
"Sports cars with high performance and modern technology"
```

**Test Queries**:
- "cheap hybrid vehicles" (should find hybrid cars)
- "electric cars with long range" (should find electric vehicles)
- "luxury vehicles with premium features" (should find luxury cars)
- "budget friendly transportation" (should find affordable options)

### Step 3: Optimization & Evaluation
**Goal**: Optimize the hybrid search parameters

**Tasks**:
- Test different weight combinations (α=0.3, β=0.7 vs α=0.7, β=0.3)
- Compare hybrid results vs pure BM25 vs pure vector search
- Calculate basic precision/recall for each approach
- Find the best weight combination for your test data

## 🔧 Technical Requirements
- **Libraries**: `rank_bm25`, `sentence-transformers`, `numpy`, `json`
- **Embeddings**: Use `all-MiniLM-L6-v2` (FREE)
- **Storage**: Simple in-memory storage for demo
- **Output**: Ranked results with scores and metadata

## 📊 Expected Output
1. **Hybrid Search System**: Complete implementation in `hybrid_search.py`
2. **Search Results**: Comparison of different approaches
3. **Optimization Report**: Best weight combination found
4. **Performance Metrics**: Precision/recall for each method

## 🎓 Learning Outcomes
By completing this exercise, you'll understand:
- How to combine keyword and semantic search effectively
- Score fusion strategies and weight optimization
- Trade-offs between different search approaches
- Basic evaluation metrics for search systems
- Real-world hybrid search implementation patterns

## 🚀 Getting Started
1. Set up the project structure
2. Create sample documents in `data/`
3. Implement the hybrid search system
4. Test with different queries and weights
5. Compare results and optimize parameters

## ✅ Success Criteria
- **Working hybrid search** that combines BM25 + vector search
- **Configurable weights** for score fusion
- **Ranked results** with meaningful scores
- **Performance comparison** between approaches
- **Optimization insights** for weight tuning

**Ready to build your first hybrid search system? Let's get started!** 🎯✨
