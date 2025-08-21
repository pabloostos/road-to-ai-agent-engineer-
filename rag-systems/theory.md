# 🎓 Masterclass: Retrieval-Augmented Generation (RAG)

**30 minutes — Theory → Practice → Production**

## 1) Why RAG matters (3 min)

LLMs are powerful, but:

- **Stale knowledge**: models don't "know" your latest docs.
- **Hallucinations**: confident but incorrect answers.
- **Context limits**: you can't stuff an entire knowledge base into one prompt.

RAG solves this by fetching relevant, authoritative context at query time and grounding the model's answer in that context.

- **RAG = Retriever + Generator**
- **Retriever** finds relevant passages → **Generator (LLM)** writes the answer using those passages.

### Benefits

- Higher factual accuracy & explainability (citations).
- Domain adaptation without fine-tuning.
- Lower cost vs. training: index once, retrieve many times.

## 2) RAG architecture (5 min)

```
User Query
   │
   ▼
[Embed Query] ──► [Vector Search: Retriever] ──► Top-k Chunks + Metadata
                                                     │
                                                     ▼
                                        [Prompt Augmentation]
                                                     │
                                                     ▼
                                          [Generator (LLM)]
                                                     │
                                                     ▼
                                          Grounded Answer (+ citations)
```

### Core components

- **Chunker**: splits documents into semantically meaningful pieces (e.g., 300–800 tokens) with overlap.
- **Embedder**: turns text into vectors (e.g., OpenAI embeddings).
- **Vector Index**: stores vectors + metadata and supports fast similarity search.
- **Prompt Assembler**: injects retrieved chunks into a system/user prompt template.
- **Generator**: the LLM that crafts the final answer.

## 3) Key concepts (6 min)

### 3.1 Document chunking

- **Why**: improves retrieval granularity and recall.
- **How**: sliding window (e.g., 500 tokens, 20–80 token overlap).
- **Heuristics**: split on headings/paragraphs; keep tables/code blocks intact.

### 3.2 Embeddings

- Dense vectors representing meaning; similar meanings → nearby vectors.
- Distance metrics: cosine (most common), dot-product, Euclidean.

### 3.3 Retrievers

- Exact-NN (small data) vs ANN (HNSW/IVF for scale).
- Hybrid (BM25 + vectors) for robustness to rare terms/symbols.

### 3.4 Prompt augmentation

Insert retrieved chunks into a strict template:

- role & tone
- task
- context block (read-only)
- output format (e.g., JSON/Markdown)
- refusal rules ("if insufficient context, say so")

## 4) Practical walkthrough: build a minimal RAG (10 min)

### 4.1 Project layout

```
rag-example/
  data/                     # your raw docs (.md, .txt, .pdf→txt)
  chunks/                   # chunked text (JSONL)
  embeddings/               # vectors + metadata (JSON/NPY)
  src/
    01_chunk.py
    02_embed.py
    03_search.py
    04_rag_answer.py
  results/
    searches.jsonl
    answers.jsonl
  README.md
```

### 4.2 Chunking (src/01_chunk.py)

```python
import os, json, re
from pathlib import Path

DATA_DIR = Path("rag-example/data")
CHUNK_DIR = Path("rag-example/chunks")
CHUNK_DIR.mkdir(parents=True, exist_ok=True)

def simple_tokenize(text):
    return re.findall(r"\S+|\n", text)

def chunk_text(text, max_tokens=500, overlap=50):
    tokens = simple_tokenize(text)
    chunks = []
    i = 0
    while i < len(tokens):
        window = tokens[i:i+max_tokens]
        chunks.append("".join(w if w == "\n" else w + " " for w in window).strip())
        i += max_tokens - overlap
    return chunks

def main():
    out = []
    for p in DATA_DIR.glob("*.txt"):
        content = p.read_text(encoding="utf-8")
        for j, chunk in enumerate(chunk_text(content)):
            out.append({"doc_id": p.stem, "chunk_id": j, "text": chunk})
    with open(CHUNK_DIR / "chunks.jsonl", "w", encoding="utf-8") as f:
        for row in out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(out)} chunks")

if __name__ == "__main__":
    main()
```

### 4.3 Embedding with OpenAI (src/02_embed.py)

```python
import os, json
from pathlib import Path
from openai import OpenAI

CHUNK_FILE = Path("rag-example/chunks/chunks.jsonl")
EMB_DIR = Path("rag-example/embeddings")
EMB_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-ada-002"  # or your preferred embedding model

def embed_batch(texts):
    resp = client.embeddings.create(model=MODEL, input=texts)
    return [d.embedding for d in resp.data]

def main(batch_size=64):
    records, batch = [], []
    with open(CHUNK_FILE, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            records.append(rec)
    embeddings = []
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        vectors = embed_batch([r["text"] for r in batch])
        for r, v in zip(batch, vectors):
            r["embedding"] = v
            embeddings.append(r)
    with open(EMB_DIR / "embeddings.jsonl", "w", encoding="utf-8") as f:
        for r in embeddings:
            f.write(json.dumps(r) + "\n")
    print(f"Embedded {len(embeddings)} chunks")

if __name__ == "__main__":
    main()
```

**Tip**: Cache embeddings (hash the text) to avoid recompute costs.

### 4.4 Local similarity search (src/03_search.py)

```python
import json, numpy as np
from pathlib import Path
from openai import OpenAI
import os

EMB_FILE = Path("rag-example/embeddings/embeddings.jsonl")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMB_MODEL = "text-embedding-ada-002"

def load_index():
    texts, metas, vecs = [], [], []
    with open(EMB_FILE, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            texts.append(r["text"])
            metas.append({"doc_id": r["doc_id"], "chunk_id": r["chunk_id"]})
            vecs.append(r["embedding"])
    return texts, metas, np.array(vecs, dtype=np.float32)

def embed_query(q):
    return client.embeddings.create(model=EMB_MODEL, input=q).data[0].embedding

def top_k(query_vec, index_vecs, k=5):
    q = np.array(query_vec, dtype=np.float32)
    q = q / (np.linalg.norm(q) + 1e-8)
    idx = index_vecs / (np.linalg.norm(index_vecs, axis=1, keepdims=True) + 1e-8)
    sims = idx @ q
    top_idx = sims.argsort()[::-1][:k]
    return top_idx, sims[top_idx]

if __name__ == "__main__":
    texts, metas, vecs = load_index()
    q = "What does the warranty cover?"
    qv = embed_query(q)
    ids, scores = top_k(qv, vecs, k=3)
    for rank, (i, s) in enumerate(zip(ids, scores), 1):
        print(f"{rank}. score={s:.3f} doc={metas[i]['doc_id']} chunk={metas[i]['chunk_id']}")
        print(texts[i][:200], "...\n")
```

### 4.5 RAG answer generation (src/04_rag_answer.py)

```python
import os, json, numpy as np
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GEN_MODEL = "gpt-4o"  # or another chat/completions model

EMB_FILE = Path("rag-example/embeddings/embeddings.jsonl")
EMB_MODEL = "text-embedding-ada-002"

def load_index():
    texts, metas, vecs = [], [], []
    with open(EMB_FILE, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            texts.append(r["text"])
            metas.append({"doc_id": r["doc_id"], "chunk_id": r["chunk_id"]})
            vecs.append(r["embedding"])
    return texts, metas, np.array(vecs, dtype=np.float32)

def embed_query(q):
    return client.embeddings.create(model=EMB_MODEL, input=q).data[0].embedding

def retrieve(query, texts, metas, vecs, k=4):
    q = np.array(embed_query(query), dtype=np.float32)
    q /= (np.linalg.norm(q) + 1e-8)
    idx = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-8)
    sims = idx @ q
    top = sims.argsort()[::-1][:k]
    ctx = [{"text": texts[i], **metas[i], "score": float(sims[i])} for i in top]
    return ctx

SYSTEM = (
"You are a helpful assistant. Use ONLY the provided context to answer. "
"If the answer is not in the context, say 'Insufficient context.' "
"Always cite sources as (doc_id#chunk_id). Be concise."
)

def build_prompt(context_chunks, question):
    context_block = "\n\n".join(
        f"(score={c['score']:.3f}) [{c['doc_id']}#{c['chunk_id']}] {c['text']}"
        for c in context_chunks
    )
    user = f"""Question:
{question}

Context (do not invent facts, quote minimally):
{context_block}

Answer with a short paragraph and include citations like (doc#chunk)."""
    return user

def answer(question, k=4):
    texts, metas, vecs = load_index()
    ctx = retrieve(question, texts, metas, vecs, k=k)
    user_prompt = build_prompt(ctx, question)
    resp = client.chat.completions.create(
        model=GEN_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2
    )
    return resp.choices[0].message.content, ctx

if __name__ == "__main__":
    q = "How do I reset my device?"
    ans, ctx = answer(q)
    print(ans)
```

## 5) Best practices (4 min)

### Chunking

- 300–800 tokens with overlap; preserve headings/sections.
- Keep code/tables intact; avoid splitting mid-table.

### Metadata

- Store doc_id, source, section, updated_at, url.
- Enables filtering (e.g., only "docs/2025").

### Prompting

- Clear constraints: "Use only context; cite (doc#chunk); say 'Insufficient context' if missing."
- Enforce output schema (JSON) for downstream systems.

### Hybrid retrieval

- Keyword (BM25) + vectors to handle rare terms, numbers, code.

### Evaluation

- Track answer correctness & citation coverage.
- Log retrieval scores, positions, and whether cited chunks actually contain the facts.

### Cost & performance

- Cache embeddings and retrieval results for frequent queries.
- Use smaller models for retrieval; reserve larger models for final generation.
- Periodically re-embed changed docs only.

## 6) RAG vs. Fine-tuning (2 min)

| Aspect | RAG | Fine-tuning |
|--------|-----|-------------|
| Freshness | Live, updatable knowledge base | Fixed at train time |
| Data need | Unlabeled docs | Labeled pairs (costly) |
| Hallucinations | Reduced via grounding | Possible without explicit retrieval |
| Latency | Retrieval + generation (↑) | Single generation (↓) |
| Best for | Factual QA, docs, policy, FAQs | Style adaptation, structured tasks |

**Rule of thumb**: Start with RAG. Fine-tune when you need style/control and have supervision data.
