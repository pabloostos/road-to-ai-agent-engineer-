# Exercise: Universal Knowledge Base Framework

## 🎯 Objective
Build a **flexible Knowledge Base framework** that can automatically process any text files and create searchable knowledge bases. This framework will be reusable for any domain or content type.

## 🚀 Key Innovation
Instead of building a single knowledge base, we'll create a **universal framework** that can:
- Accept any `.txt` files as input
- Automatically process and embed them
- Create searchable knowledge bases
- Support multiple knowledge bases simultaneously
- Provide a simple interface for querying

## 📁 Project Structure
```
knowledge-base-framework/
├── theory.md                    # Knowledge Base theory
├── exercise.md                  # This file
├── requirements.txt             # Dependencies
├── README.md                   # Documentation
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
│   ├── ai_knowledge/
│   ├── cooking_recipes/
│   └── company_policies/
└── examples/                   # Example usage
```

## 🎯 Exercise Steps

### Step 1: Universal Knowledge Base Framework (`kb_framework.py`)
**Goal**: Create a flexible framework that can handle any text content

**Features**:
- **Auto-detection**: Automatically process any `.txt` files
- **Flexible chunking**: Configurable chunk sizes and overlap
- **Free embeddings**: Use Sentence Transformers for cost-free processing
- **Metadata tracking**: Store source, timestamp, chunk info
- **Multiple formats**: Support different input structures

### Step 2: Knowledge Base Builder (`kb_builder.py`)
**Goal**: Build knowledge bases from any text files

**Features**:
- **Batch processing**: Process multiple files at once
- **Progress tracking**: Show processing status
- **Error handling**: Graceful handling of file issues
- **Validation**: Check file integrity and content
- **Optimization**: Efficient embedding generation

### Step 3: Query Interface (`kb_query.py`)
**Goal**: Provide a simple interface for querying any knowledge base

**Features**:
- **Universal queries**: Query any knowledge base
- **Semantic search**: Find relevant content using embeddings
- **Similarity scoring**: Rank results by relevance
- **Context retrieval**: Get surrounding context
- **Batch queries**: Query multiple knowledge bases

### Step 4: Multi-KB Manager (`kb_manager.py`)
**Goal**: Manage multiple knowledge bases simultaneously

**Features**:
- **KB registration**: Register new knowledge bases
- **KB switching**: Switch between different knowledge bases
- **KB comparison**: Compare results across knowledge bases
- **KB statistics**: Show KB size, coverage, etc.
- **KB updates**: Update existing knowledge bases

## 📋 Sample Data Sets

### 1. AI Knowledge Base (`data/ai_knowledge/`)
```
ai_basics.txt
machine_learning.txt
deep_learning.txt
natural_language_processing.txt
computer_vision.txt
```

### 2. Cooking Recipes (`data/cooking_recipes/`)
```
italian_recipes.txt
baking_basics.txt
quick_meals.txt
healthy_cooking.txt
```

### 3. Company Policies (`data/company_policies/`)
```
hr_policies.txt
it_policies.txt
security_policies.txt
remote_work_policies.txt
```

## 🎯 Implementation Requirements

### Core Framework Class
```python
class UniversalKnowledgeBase:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        # Initialize with free Sentence Transformers
    
    def create_knowledge_base(self, name, data_dir):
        # Process all .txt files in data_dir
        # Generate embeddings and store
    
    def query_knowledge_base(self, name, query, top_k=3):
        # Query specific knowledge base
    
    def list_knowledge_bases(self):
        # List all available knowledge bases
    
    def get_kb_stats(self, name):
        # Get statistics about a knowledge base
```

### Key Features
- ✅ **Free Embeddings**: Sentence Transformers for cost-free processing
- ✅ **Universal Input**: Accept any `.txt` files
- ✅ **Multiple KBs**: Support many knowledge bases
- ✅ **Simple Interface**: Easy-to-use query system
- ✅ **Metadata Tracking**: Full source and context tracking
- ✅ **Scalable**: Can handle large document collections

## 🚀 Usage Examples

### Create a Knowledge Base
```python
from src.kb_framework import UniversalKnowledgeBase

# Initialize framework
kb = UniversalKnowledgeBase()

# Create AI knowledge base
kb.create_knowledge_base("ai_knowledge", "data/ai_knowledge/")

# Create cooking knowledge base
kb.create_knowledge_base("cooking_recipes", "data/cooking_recipes/")
```

### Query Knowledge Bases
```python
# Query AI knowledge base
results = kb.query_knowledge_base("ai_knowledge", "What is machine learning?")

# Query cooking knowledge base
results = kb.query_knowledge_base("cooking_recipes", "How to make pasta?")

# List all knowledge bases
kb.list_knowledge_bases()
```

## 🎯 Success Criteria
✅ **Universal Processing**: Can handle any `.txt` files  
✅ **Multiple KBs**: Support many knowledge bases simultaneously  
✅ **Free Embeddings**: Use Sentence Transformers (no API costs)  
✅ **Simple Interface**: Easy to create and query knowledge bases  
✅ **Metadata Tracking**: Full source and context information  
✅ **Scalable**: Can process large document collections  

## 💡 Bonus Challenges
- **Web Interface**: Simple web UI for managing and querying KBs
- **KB Analytics**: Track query patterns and popular topics
- **Auto-updates**: Automatically update KBs when files change
- **KB Export**: Export knowledge bases to different formats
- **Advanced Search**: Add filters, date ranges, and categories

## 🔧 Technical Requirements
- **Embeddings**: Sentence Transformers (free)
- **Storage**: JSONL format for efficiency
- **Search**: Cosine similarity with configurable thresholds
- **Processing**: Batch processing for large files
- **Error Handling**: Robust error handling and logging

## 📊 Expected Output
1. **Universal Framework**: Reusable KB creation system
2. **Multiple Knowledge Bases**: AI, cooking, policies, etc.
3. **Query Interface**: Simple way to search any KB
4. **Management Tools**: Tools to manage multiple KBs
5. **Documentation**: Clear usage examples and guides

## 🎓 Learning Outcomes
By completing this exercise, you'll understand:
- How to build flexible, reusable AI systems
- Best practices for knowledge base design
- Multi-domain knowledge management
- Scalable embedding and search systems
- Framework architecture and design patterns

## 🚀 Getting Started
1. Set up the project structure
2. Create sample data directories
3. Implement the universal framework
4. Test with different knowledge domains
5. Build the management interface

**Ready to build a universal knowledge base framework? Let's create something that can handle any domain!** 🎯✨
