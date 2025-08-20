# 🎓 Masterclass: Embeddings Creation with the OpenAI API

## 1. Introduction

Welcome, everyone, to today's session on Embeddings Creation.
Embeddings are one of the cornerstone technologies of modern AI. Without them, applications like semantic search, recommendation engines, clustering, or Retrieval-Augmented Generation (RAG) would not be possible.

By the end of this lecture, you will not only understand the theory behind embeddings but also have practical skills to generate, store, and use embeddings in real projects.

## 2. What Are Embeddings?

- **Definition:** Embeddings are numerical vector representations of data (text, images, audio) where semantic similarity is preserved.
- **Idea:** Similar concepts → closer vectors in a high-dimensional space.

**Example:**
- "dog" and "puppy" → embeddings close together.
- "dog" and "car" → embeddings far apart.

💡 **Mathematical Foundation:**
- Embeddings are vectors in an n-dimensional space (OpenAI's text-embedding-ada-002 produces 1,536-dimensional vectors).
- Similarity is usually measured with:
  - Cosine similarity (angle between vectors).
  - Euclidean distance (straight-line distance).

## 3. Why Do Embeddings Matter?

- **Semantic Search:** Retrieve documents by meaning, not keywords.
- **Clustering:** Group similar texts or items together.
- **Recommendation Systems:** Suggest content similar to user interests.
- **RAG Pipelines:** Provide LLMs with context retrieved via embeddings.

## 4. Typical Use Cases

- **Search Engines:** Finding relevant articles beyond keyword matching.
- **Customer Support:** Match user questions to FAQs.
- **Recommendation Systems:** "Users who liked this also liked…"
- **Chatbots:** Enhance conversation by fetching relevant context.

## 5. Practical Example: Generating Embeddings with OpenAI

### Step 1: Install Dependencies
```bash
pip install openai
```

### Step 2: Generate Embeddings in Python
```python
from openai import OpenAI
import json
import os

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example texts
texts = [
    "Artificial Intelligence is transforming the world.",
    "Machine learning is a subset of AI.",
    "I love Galician landscapes!"
]

# Generate embeddings
embeddings = []
for text in texts:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    vector = response.data[0].embedding
    embeddings.append({"text": text, "embedding": vector})

# Save to folder
os.makedirs("embeddings-examples", exist_ok=True)
with open("embeddings-examples/embeddings.json", "w") as f:
    json.dump(embeddings, f, indent=2)
```

This script:
- Generates embeddings for sample texts.
- Stores them in embeddings-examples/embeddings.json.

## 6. Retrieval & Similarity Search

We can perform a similarity search using cosine similarity:

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Load stored embeddings
with open("embeddings-examples/embeddings.json") as f:
    data = json.load(f)

# Compare first and second sentence
sim = cosine_similarity(data[0]["embedding"], data[1]["embedding"])
print("Similarity between text 1 and 2:", sim)
```

## 7. Best Practices

### Model Choice
- Use text-embedding-ada-002 for general-purpose embeddings.
- Consider domain-specific models if available (e.g., biomedical).

### Normalization
- Normalize vectors (unit length) before comparison for consistency.

### Metadata Storage
- Always store the original text, timestamp, and other metadata with embeddings.

### Cost Management
- Embeddings are cheaper than text completions, but still scale with usage.
- Estimate cost = (#tokens × price per 1K tokens).
- Cache embeddings: don't recompute if the text already exists.

## 8. Alternatives to OpenAI

- **Sentence Transformers (Hugging Face):** Local embeddings, free to use.
- **FAISS:** Facebook's library for similarity search.
- **Weaviate / Milvus:** Vector databases with integrated embedding pipelines.

💡 **Tradeoff:** OpenAI provides scalability + quality, while local models provide cost efficiency + control.

## 9. Real-World Applications

- **Spotify:** Music recommendation using embeddings.
- **Google Search:** Semantic indexing.
- **Duolingo:** Embedding-based personalization of learning exercises.
