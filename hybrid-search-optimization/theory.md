# 🎓 Masterclass: Hybrid Search & Optimization in AI Systems

**Duration: ~45 minutes**  
**Professor: AI Engineering Faculty**

---

## 1. Introduction

Welcome everyone! Today we'll explore **Hybrid Search & Optimization** — a critical component in modern AI systems where keyword-based search and vector-based semantic search are combined to achieve more robust and reliable results.

This lecture bridges traditional information retrieval (IR) with modern embedding-based retrieval, and we'll also dive into optimization strategies to ensure we get the best performance.

---

## 2. Why Search Matters in AI

In almost every intelligent system, from chatbots to search engines to Retrieval-Augmented Generation (RAG) pipelines, the retrieval step is crucial.

- **If retrieval fails, generation or recommendation will fail.**
- **Effective retrieval = relevant, accurate, and efficient results.**

---

## 3. Limitations of Pure Search Approaches

### 3.1 Keyword Search (BM25, inverted indexes)

**Strengths:**
- Fast, scalable (used in Elasticsearch, Lucene)
- Precise for exact matches

**Limitations:**
- Struggles with synonyms ("car" vs. "automobile")
- Sensitive to typos
- Doesn't capture semantic meaning

### 3.2 Vector Search (Semantic Embeddings)

**Strengths:**
- Captures meaning, not just words
- Handles synonyms, paraphrases, multilingual queries

**Limitations:**
- Can miss exact keyword matches (IDs, names, technical terms)
- Requires vector databases (Pinecone, FAISS, Weaviate)
- More computationally expensive

---

## 4. Why Hybrid Search?

Hybrid search combines keyword precision with semantic understanding.

**Example: Query = "Affordable hybrid cars under $20k"**
- **Keyword search** → Finds documents with "affordable" and "cars"
- **Vector search** → Finds semantically similar docs like "budget-friendly vehicles"
- **Hybrid search** → Combines both → best of both worlds

---

## 5. Hybrid Architectures

### Score Fusion (Weighted Combination)
Both searches return ranked lists → scores combined with a weight factor.

**Example:** `Final_Score = α * BM25_score + β * Embedding_score`

### Sequential Pipelines
First filter results using keyword search → rerank using semantic search

### Re-ranking Models
Use machine learning (e.g., cross-encoders) to rerank results after hybrid scoring

**Diagram:** Flow from query → keyword engine → vector engine → fusion → final results

---

## 6. Optimization Concepts

### 6.1 Parameters to Tune
- **top_k** → number of candidates retrieved
- **Weighting factors (α, β)** → how much weight to assign to keyword vs. semantic scores
- **Metadata filtering** → restrict by category, author, timestamp, etc.

### 6.2 Evaluation Metrics
- **Precision**: proportion of retrieved items that are relevant
- **Recall**: proportion of relevant items retrieved
- **F1-score**: harmonic mean of precision & recall
- **MRR (Mean Reciprocal Rank)**: how high the first correct result ranks
- **nDCG (Normalized Discounted Cumulative Gain)**: measures ranking quality

### 6.3 Trade-offs
- **Cost**: vector DBs can be expensive at scale
- **Latency**: keyword search = fast; semantic = slower
- **Quality**: hybrid improves robustness

---

## 7. Practical Example: Hybrid Search with Pinecone + BM25

We'll build a small hybrid pipeline.

### Step 1 – Setup & Data

```python
!pip install pinecone-client openai rank_bm25

import openai
import pinecone
from rank_bm25 import BM25Okapi

# Initialize Pinecone
pinecone.init(api_key="YOUR_API_KEY", environment="us-east1-gcp")
index = pinecone.Index("hybrid-search-demo")
```

### Step 2 – Create Embeddings

```python
documents = [
    "Affordable hybrid cars under $20,000",
    "Electric vehicles with long battery life",
    "Cheap used cars in excellent condition",
    "Luxury cars with hybrid engines"
]

# Create embeddings with OpenAI
embeddings = [openai.Embedding.create(input=doc, model="text-embedding-3-small")["data"][0]["embedding"] for doc in documents]

# Insert into Pinecone
for i, vec in enumerate(embeddings):
    index.upsert([(str(i), vec, {"text": documents[i]})])
```

### Step 3 – Keyword Search Baseline

```python
tokenized_corpus = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_corpus)

query = "cheap hybrid vehicles"
bm25_scores = bm25.get_scores(query.split(" "))
```

### Step 4 – Vector Search

```python
query_embedding = openai.Embedding.create(input=query, model="text-embedding-3-small")["data"][0]["embedding"]
vector_results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
```

### Step 5 – Fusion Scoring

```python
import numpy as np

alpha, beta = 0.5, 0.5  # weights
hybrid_scores = {}

# BM25 scores
for i, score in enumerate(bm25_scores):
    hybrid_scores[str(i)] = alpha * score

# Add vector scores
for match in vector_results["matches"]:
    hybrid_scores[match["id"]] = hybrid_scores.get(match["id"], 0) + beta * match["score"]

# Sort results
sorted_results = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
print(sorted_results)
```

📂 Save all scripts/results inside `hybrid-search/`.

---

## 8. Best Practices

- **Tune α vs. β weights** depending on domain
- **For rare keywords** (e.g., medical terms, part numbers) → rely more on keyword search
- **Use metadata filters** (date, author, category) for structured retrieval
- **For scaling**: use approximate nearest neighbor (ANN) search in Pinecone/FAISS

---

## 9. Real-World Applications

- **Google Search** → hybrid of BM25 + embeddings + rerankers
- **E-commerce** (Amazon, Zalando) → hybrid search for product discovery
- **Chatbots/RAG** → ensures both factual grounding and semantic coverage

---

## 10. Conclusion

- **Keyword search** = precision, fast, exact
- **Vector search** = semantic, robust, meaning-based
- **Hybrid search** = combines the strengths of both
- **Optimization** ensures efficiency, accuracy, and scalability

**Takeaway:** Hybrid search is the backbone of modern retrieval in AI systems, powering everything from RAG pipelines to search engines.
