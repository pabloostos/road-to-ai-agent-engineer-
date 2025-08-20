# Exercise: Embeddings Creation & Similarity Search System

## Objective
Build a comprehensive embeddings system that demonstrates:
1. **Embedding Generation** - Create embeddings for a collection of texts
2. **Similarity Search** - Find the most similar texts to a query
3. **Clustering Analysis** - Group similar texts together
4. **Cost Monitoring** - Track token usage and costs

## Requirements
- **API:** OpenAI Embeddings API
- **Libraries:** `openai`, `numpy`, `json`, `datetime`, `python-dotenv`
- **Skills:** Vector operations, similarity metrics, data processing

## Exercise Structure

### Part 1: Embedding Generator
Create a class that:
- Generates embeddings for input texts
- Stores them with metadata (text, timestamp, token count)
- Implements caching to avoid re-computing existing embeddings
- Tracks costs per embedding

### Part 2: Similarity Search Engine
Implement functions to:
- Calculate cosine similarity between vectors
- Find top-k most similar texts to a query
- Perform semantic search across the embedding database

### Part 3: Text Clustering
Create a simple clustering system that:
- Groups similar texts together
- Identifies clusters of related content
- Provides cluster summaries

### Part 4: Cost Analysis
Track and report:
- Total tokens used
- Total cost incurred
- Average cost per embedding
- Cost optimization recommendations

## Sample Dataset
Use this collection of texts for testing:

```python
sample_texts = [
    "Artificial Intelligence is transforming modern technology",
    "Machine learning algorithms can predict future trends",
    "Deep learning models require large amounts of data",
    "Natural language processing enables human-computer interaction",
    "Computer vision helps machines understand visual information",
    "The weather in Galicia is often rainy and green",
    "Spanish cuisine includes paella and tapas",
    "Barcelona is a beautiful city in Catalonia",
    "Python programming is essential for data science",
    "JavaScript is widely used for web development"
]
```

## Expected Deliverables
1. **Main Script** - Complete embeddings system
2. **Sample Output** - Similarity search results
3. **Cost Report** - Token usage and cost analysis
4. **Clustering Results** - Grouped similar texts

## Bonus Challenges
- **Performance Optimization** - Batch processing for multiple texts
- **Alternative Models** - Try different embedding models
- **Visualization** - Plot embeddings in 2D space using PCA
- **Real-time Search** - Build a simple search interface

## Success Criteria
✅ Generate embeddings for all sample texts  
✅ Perform similarity search with meaningful results  
✅ Group texts into logical clusters  
✅ Track and report costs accurately  
✅ Handle errors gracefully  

## Learning Outcomes
By completing this exercise, you'll understand:
- How to generate and store embeddings efficiently
- Methods for measuring semantic similarity
- Techniques for organizing and searching vector data
- Cost management strategies for embedding APIs
- Real-world applications of embedding technology
