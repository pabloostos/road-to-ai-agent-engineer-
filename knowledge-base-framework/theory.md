📚 Masterclass: Building Custom Knowledge Bases (KBs) with Embeddings

Instructor: Professor of AI Engineering
Duration: 30 minutes
Focus: How to design, build, and query custom Knowledge Bases (KBs) using embeddings for AI applications.

## 1. Introduction

Welcome to today's lecture on Building Custom Knowledge Bases (KBs) for AI projects.
Knowledge Bases are the backbone of modern AI applications — from customer support chatbots to Retrieval-Augmented Generation (RAG) pipelines.

We will cover:

- What KBs are and why they matter.
- How embeddings empower KBs for semantic search and context retrieval.
- Step-by-step process of building and querying a KB.
- Best practices for storage, metadata, and maintenance.
- Real-world applications.

By the end, you will not only understand the theory but also build your own FAQ-based Knowledge Base with embeddings.

## 2. What is a Knowledge Base in AI?

A Knowledge Base (KB) is a collection of information that an AI system can access to provide accurate and contextually relevant answers.

- **Structured KBs**: Organized as databases (tables, fields). Examples: product catalogs, CRM systems.
- **Unstructured KBs**: Free-text sources like FAQs, manuals, support tickets, PDFs, web pages.

⚡ **Problem**: Traditional keyword search struggles with synonyms and semantic meaning.
⚡ **Solution**: Embeddings — numerical vector representations of text that capture semantic similarity.

**Example**:
- Query: "How can I reset my password?"
- KB Entry: "Steps to change account credentials"
- → A keyword search may fail. A semantic embedding search succeeds because it understands "reset password" ≈ "change credentials".

## 3. Why Embeddings Make KBs Powerful

- **Semantic Search**: Retrieve meaning, not just keywords.
- **Context Retrieval**: KBs can feed LLMs with relevant knowledge.
- **FAQ Systems**: Fast, accurate responses.
- **RAG Pipelines**: Ground LLM answers with facts.

💡 Embeddings allow KBs to handle long-tail knowledge — questions not explicitly written but semantically close.

## 4. Role of KBs in AI Applications

- **Chatbots**: Instant customer support powered by FAQs.
- **Customer Service**: Agent assist tools retrieving policies and procedures.
- **Knowledge Workers**: Internal search across documents.
- **RAG Systems**: LLMs querying KBs for grounded answers.

📌 Without KBs, LLMs may hallucinate. With KBs, they provide accurate, context-aware responses.

## 5. Key Components of Building a KB

### 5.1 Collecting and Cleaning Documents
- Sources: articles, FAQs, manuals, support logs.
- Clean text: remove noise (HTML tags, formatting issues).

### 5.2 Chunking Text
- Break documents into smaller, coherent segments (100–500 words).
- Prevents exceeding embedding model input limits.
- Preserves semantic meaning for retrieval.

### 5.3 Generating Embeddings
- Use OpenAI API (text-embedding-ada-002) or local models (SentenceTransformers).
- Each chunk → vector representation.

### 5.4 Storing Embeddings + Metadata
- Metadata: document title, author, date, source.
- Storage formats:
  - CSV/JSON: simple and local.
  - Vector Databases: Pinecone, Weaviate, FAISS (for scaling).

### 5.5 Querying with Semantic Similarity Search
- Convert user query → embedding.
- Compare query vector to stored embeddings.
- Retrieve top-k most relevant chunks.

## 6. Practical Example

We'll build a small FAQ Knowledge Base.

**Step 1: Prepare Data**

Create `faq_data.json`:
```json
[
  {"question": "How do I reset my password?", "answer": "Go to settings, click 'Account', then 'Reset password'."},
  {"question": "How do I update billing info?", "answer": "Navigate to billing settings and update your payment method."},
  {"question": "What is the refund policy?", "answer": "Refunds are available within 30 days of purchase."}
]
```

**Step 2: Generate Embeddings and Save**

```python
import openai, json, os
import pandas as pd

openai.api_key = "YOUR_API_KEY"

with open("faq_data.json") as f:
    faqs = json.load(f)

embeddings = []
for item in faqs:
    text = item["question"] + " " + item["answer"]
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    vector = response["data"][0]["embedding"]
    embeddings.append({"text": text, "vector": vector, "metadata": item})

df = pd.DataFrame(embeddings)
os.makedirs("kb-building", exist_ok=True)
df.to_csv("kb-building/faq_embeddings.csv", index=False)
```

**Step 3: Query the KB**

```python
from openai.embeddings_utils import cosine_similarity
import numpy as np

query = "How can I change my login credentials?"
query_embedding = openai.Embedding.create(
    input=query,
    model="text-embedding-ada-002"
)["data"][0]["embedding"]

# Compare against stored embeddings
df["similarity"] = df["vector"].apply(lambda v: cosine_similarity(v, query_embedding))
best_match = df.loc[df["similarity"].idxmax()]
print("Best Answer:", best_match["metadata"]["answer"])
```

✅ Query "change login credentials" → retrieves "reset password" answer.

## 7. Best Practices

- **Metadata Tagging**: Always store author, source, and timestamp.
- **Chunking Strategy**: Overlap chunks to preserve context.
- **Storage Choices**:
  - Small scale → CSV/JSON.
  - Medium/large scale → FAISS (local).
  - Production → Pinecone, Weaviate, Milvus.
- **Updating KBs**: Automate embedding regeneration when documents change.
- **Cost Control**: Minimize unnecessary re-embedding by tracking changes.

## 8. Real-World Examples

- **Notion AI**: Knowledge retrieval across personal docs.
- **Zendesk AI Bots**: Customer service powered by FAQs.
- **Legal/Healthcare AI**: Grounding LLMs in structured KBs for compliance.

## 9. Conclusion

Knowledge Bases powered by embeddings enable AI systems to retrieve meaning, not just words.
They form the foundation of:

- Smarter search engines.
- Reliable chatbots.
- RAG-powered AI assistants.

By mastering KB construction, you are building the infrastructure of intelligent agents.
