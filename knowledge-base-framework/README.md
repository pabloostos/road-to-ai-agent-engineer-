# Knowledge Base Framework

## 🎯 Overview
A **universal Knowledge Base framework** that can automatically process any text files and create searchable knowledge bases. This framework is designed to be reusable for any domain or content type.

## 🚀 Key Features
- **Universal Input**: Accept any `.txt` files as input
- **Free Embeddings**: Use Sentence Transformers for cost-free processing
- **Multiple KBs**: Support many knowledge bases simultaneously
- **Simple Interface**: Easy-to-use query system
- **Metadata Tracking**: Full source and context information
- **Scalable**: Can handle large document collections

## 📁 Project Structure
```
knowledge-base-framework/
├── theory.md                    # Knowledge Base theory
├── exercise.md                  # Exercise instructions
├── requirements.txt             # Dependencies
├── README.md                   # This file
├── .env.example                # Environment variables
├── src/                        # Source code
│   ├── kb_framework.py         # Main framework class
│   ├── kb_builder.py           # Knowledge base builder
│   ├── kb_query.py             # Query interface
│   └── kb_manager.py           # Multi-KB manager
├── data/                       # Input text files
│   ├── ai_knowledge/           # AI knowledge base
│   ├── cooking_recipes/        # Cooking knowledge base
│   └── company_policies/       # Company policies KB
├── knowledge_bases/            # Generated knowledge bases
└── examples/                   # Example usage
```

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 2. Create Sample Data
```bash
# Create data directories
mkdir -p data/ai_knowledge data/cooking_recipes data/company_policies

# Add your .txt files to these directories
```

### 3. Basic Usage
```python
from src.kb_framework import UniversalKnowledgeBase

# Initialize framework
kb = UniversalKnowledgeBase()

# Create knowledge bases
kb.create_knowledge_base("ai_knowledge", "data/ai_knowledge/")
kb.create_knowledge_base("cooking_recipes", "data/cooking_recipes/")

# Query knowledge bases
results = kb.query_knowledge_base("ai_knowledge", "What is machine learning?")
print(results)
```

## 🎯 Core Components

### UniversalKnowledgeBase Class
The main framework class that handles:
- **Knowledge base creation** from text files
- **Semantic search** using embeddings
- **Multi-KB management** and switching
- **Metadata tracking** and statistics

### Key Methods
- `create_knowledge_base(name, data_dir)`: Create a new KB from text files
- `query_knowledge_base(name, query, top_k=3)`: Query a specific KB
- `list_knowledge_bases()`: List all available KBs
- `get_kb_stats(name)`: Get statistics about a KB

## 📊 Supported Data Formats

### Input Files
- **Text files** (`.txt`): Any plain text content
- **Structured content**: FAQs, manuals, articles, etc.
- **Multi-language**: Supports any language

### Output Format
- **JSONL**: Efficient storage of embeddings and metadata
- **Metadata**: Source file, timestamp, chunk information
- **Embeddings**: 384-dimensional vectors (Sentence Transformers)

## 🛠️ Technical Stack
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`) - **FREE**
- **Storage**: JSONL format for efficiency
- **Search**: Cosine similarity with configurable thresholds
- **Processing**: Batch processing for large files
- **Error Handling**: Robust error handling and logging

## 🎯 Use Cases

### 1. Company Knowledge Management
```python
# Create company policies KB
kb.create_knowledge_base("company_policies", "data/company_policies/")

# Query HR policies
results = kb.query_knowledge_base("company_policies", "What is the vacation policy?")
```

### 2. Educational Content
```python
# Create educational KB
kb.create_knowledge_base("educational_content", "data/educational/")

# Query course material
results = kb.query_knowledge_base("educational_content", "How does photosynthesis work?")
```

### 3. Customer Support
```python
# Create FAQ KB
kb.create_knowledge_base("customer_support", "data/faqs/")

# Query support questions
results = kb.query_knowledge_base("customer_support", "How do I reset my password?")
```

## 🚀 Advanced Features

### Multi-KB Querying
```python
# Query multiple knowledge bases
results = kb.query_multiple_kbs(
    ["ai_knowledge", "cooking_recipes"], 
    "What is the best approach?"
)
```

### KB Statistics
```python
# Get KB statistics
stats = kb.get_kb_stats("ai_knowledge")
print(f"Documents: {stats['documents']}")
print(f"Chunks: {stats['chunks']}")
print(f"Embeddings: {stats['embeddings']}")
```

### KB Management
```python
# List all knowledge bases
kbs = kb.list_knowledge_bases()

# Update existing KB
kb.update_knowledge_base("ai_knowledge", "data/ai_knowledge_updated/")
```

## 🎓 Learning Objectives
By using this framework, you'll understand:
- **Knowledge Base Design**: How to structure and organize knowledge
- **Embedding Systems**: Vector representations and similarity search
- **Multi-Domain Management**: Handling different types of content
- **Scalable Architecture**: Building reusable AI frameworks
- **Metadata Management**: Tracking sources and context

## 💡 Best Practices

### Data Organization
- **Consistent naming**: Use clear, descriptive names for KBs
- **Structured directories**: Organize input files logically
- **Metadata tracking**: Always include source and timestamp information

### Performance Optimization
- **Batch processing**: Process multiple files efficiently
- **Caching**: Cache embeddings to avoid re-computation
- **Chunking strategy**: Use appropriate chunk sizes for your content

### Quality Assurance
- **Content validation**: Check file integrity before processing
- **Similarity thresholds**: Use appropriate thresholds for your use case
- **Error handling**: Implement robust error handling and logging

## 🔗 Related Modules
- **RAG Systems**: Use KBs as part of RAG pipelines
- **Embeddings Creation**: Understand vector representations
- **Vector Databases**: Scale to production systems
- **Production Deployment**: Deploy KBs in production

## 🚀 Next Steps
After mastering this framework, explore:
1. **Web Interface**: Build a web UI for KB management
2. **Advanced Search**: Add filters and advanced querying
3. **KB Analytics**: Track usage patterns and insights
4. **Production Scaling**: Deploy to production environments
5. **Integration**: Integrate with other AI systems

## 🎯 Why This Framework Matters
This universal Knowledge Base framework represents a **paradigm shift** in AI development by:
- **Democratizing AI**: Making knowledge bases accessible to everyone
- **Reducing Costs**: Free embeddings eliminate API costs
- **Increasing Flexibility**: Handle any domain or content type
- **Improving Scalability**: Support multiple knowledge bases
- **Enhancing Reusability**: One framework for many use cases

**Ready to build universal knowledge bases for any domain?** 🎯✨
