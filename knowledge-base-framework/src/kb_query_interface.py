#!/usr/bin/env python3
"""
Step 3: Query Interface
=======================
Simple interface for searching and querying knowledge bases.

This module provides a user-friendly way to:
1. Search across multiple knowledge bases
2. Get relevant results with similarity scores
3. Filter and sort results
4. Export search results

🎯 Learning Objectives:
- Understand how to build a search interface
- Learn about result ranking and filtering
- See how to handle multiple knowledge bases
- Understand search result formatting
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from kb_framework import UniversalKnowledgeBase

class KnowledgeBaseQueryInterface:
    """
    Simple Knowledge Base Query Interface
    
    This class provides a user-friendly interface for searching knowledge bases.
    It handles loading multiple knowledge bases and provides simple search
    functionality with result ranking and filtering.
    
    🎯 Key Features:
    - Search across multiple knowledge bases
    - Rank results by similarity
    - Filter results by threshold
    - Export search results
    - Simple and intuitive API
    """
    
    def __init__(self, kb_base_dir: str = "knowledge_bases"):
        """
        Initialize the Query Interface.
        
        Args:
            kb_base_dir: Directory containing knowledge bases
        """
        self.kb_base_dir = Path(kb_base_dir)
        self.knowledge_bases = {}
        self.loaded_kbs = {}
        
        print("🔍 Query Interface initialized!")
        print(f"   📁 Knowledge bases directory: {self.kb_base_dir}")
    
    def list_available_knowledge_bases(self) -> List[Dict[str, Any]]:
        """
        List all available knowledge bases.
        
        Returns:
            List of knowledge base information
        """
        kb_list = []
        
        if not self.kb_base_dir.exists():
            return kb_list
        
        for kb_dir in self.kb_base_dir.iterdir():
            if kb_dir.is_dir():
                metadata_file = kb_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                        
                        kb_info = {
                            "name": metadata["name"],
                            "created_at": metadata["created_at"],
                            "total_chunks": metadata["total_chunks"],
                            "total_files": metadata["total_files"],
                            "embedding_model": metadata["embedding_model"],
                            "path": str(kb_dir),
                            "loaded": metadata["name"] in self.loaded_kbs
                        }
                        kb_list.append(kb_info)
                    except Exception as e:
                        print(f"⚠️  Error reading KB {kb_dir.name}: {e}")
        
        return kb_list
    
    def load_knowledge_base(self, name: str) -> bool:
        """
        Load a knowledge base into memory for searching.
        
        Args:
            name: Name of the knowledge base to load
            
        Returns:
            True if successful, False otherwise
        """
        print(f"📚 Loading knowledge base: {name}")
        
        kb_dir = self.kb_base_dir / name
        if not kb_dir.exists():
            print(f"❌ Knowledge base '{name}' not found")
            return False
        
        try:
            # Initialize the framework
            kb = UniversalKnowledgeBase()
            
            # Load existing knowledge bases
            loaded_count = kb.load_existing_knowledge_bases()
            
            if name in kb.knowledge_bases:
                self.loaded_kbs[name] = kb
                print(f"✅ Knowledge base '{name}' loaded successfully!")
                print(f"   📄 Chunks: {len(kb.knowledge_bases[name]['chunks'])}")
                return True
            else:
                print(f"❌ Knowledge base '{name}' not found in loaded KBs")
                return False
                
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            return False
    
    def load_all_knowledge_bases(self) -> int:
        """
        Load all available knowledge bases.
        
        Returns:
            Number of knowledge bases loaded
        """
        print("📚 Loading all knowledge bases...")
        
        available_kbs = self.list_available_knowledge_bases()
        loaded_count = 0
        
        for kb_info in available_kbs:
            if self.load_knowledge_base(kb_info["name"]):
                loaded_count += 1
        
        print(f"✅ Loaded {loaded_count} knowledge bases")
        return loaded_count
    
    def search(self, 
               query: str, 
               kb_names: Optional[List[str]] = None,
               top_k: int = 5,
               similarity_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Search across knowledge bases.
        
        Args:
            query: Search query
            kb_names: List of knowledge base names to search (None = all loaded)
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            Search results with metadata
        """
        print(f"\n🔍 Searching: '{query}'")
        print("=" * 50)
        
        # Use all loaded KBs if none specified
        if kb_names is None:
            kb_names = list(self.loaded_kbs.keys())
        
        if not kb_names:
            return {
                "error": "No knowledge bases loaded. Use load_knowledge_base() first.",
                "results": [],
                "metadata": {}
            }
        
        print(f"📚 Searching in {len(kb_names)} knowledge bases:")
        for kb_name in kb_names:
            print(f"   • {kb_name}")
        
        # Search each knowledge base
        all_results = []
        search_start_time = time.time()
        
        for kb_name in kb_names:
            if kb_name not in self.loaded_kbs:
                print(f"⚠️  Knowledge base '{kb_name}' not loaded, skipping...")
                continue
            
            kb = self.loaded_kbs[kb_name]
            
            try:
                # Query the knowledge base
                kb_results = kb.query_knowledge_base(kb_name, query, top_k=top_k)
                
                if "error" not in kb_results:
                    # Add knowledge base name to each result
                    for result in kb_results["results"]:
                        result["knowledge_base"] = kb_name
                        all_results.append(result)
                    
                    print(f"   ✅ {kb_name}: Found {len(kb_results['results'])} results")
                else:
                    print(f"   ❌ {kb_name}: {kb_results['error']}")
                    
            except Exception as e:
                print(f"   ❌ {kb_name}: Error during search - {e}")
        
        # Sort all results by similarity score
        all_results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Apply similarity threshold
        filtered_results = [
            result for result in all_results 
            if result["similarity"] >= similarity_threshold
        ]
        
        # Limit to top_k results
        final_results = filtered_results[:top_k]
        
        search_time = time.time() - search_start_time
        
        # Prepare metadata
        metadata = {
            "query": query,
            "knowledge_bases_searched": kb_names,
            "total_results_found": len(all_results),
            "results_after_filtering": len(filtered_results),
            "results_returned": len(final_results),
            "similarity_threshold": similarity_threshold,
            "search_time_seconds": round(search_time, 3),
            "search_timestamp": datetime.now().isoformat()
        }
        
        print(f"\n📊 Search Summary:")
        print(f"   🔍 Query: '{query}'")
        print(f"   📚 KBs searched: {len(kb_names)}")
        print(f"   📄 Total results: {len(all_results)}")
        print(f"   ✅ Filtered results: {len(filtered_results)}")
        print(f"   🎯 Final results: {len(final_results)}")
        print(f"   ⏱️  Search time: {search_time:.3f}s")
        
        return {
            "results": final_results,
            "metadata": metadata
        }
    
    def search_single_kb(self, 
                        kb_name: str, 
                        query: str, 
                        top_k: int = 5,
                        similarity_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Search in a single knowledge base.
        
        Args:
            kb_name: Name of the knowledge base
            query: Search query
            top_k: Number of top results
            similarity_threshold: Minimum similarity score
            
        Returns:
            Search results
        """
        return self.search(query, [kb_name], top_k, similarity_threshold)
    
    def format_search_results(self, search_results: Dict[str, Any], 
                            include_metadata: bool = True) -> str:
        """
        Format search results as a readable string.
        
        Args:
            search_results: Results from search() method
            include_metadata: Whether to include metadata
            
        Returns:
            Formatted string
        """
        if "error" in search_results:
            return f"❌ Error: {search_results['error']}"
        
        results = search_results["results"]
        metadata = search_results.get("metadata", {})
        
        if not results:
            return "🔍 No results found matching your query."
        
        # Format results
        output = f"🔍 Search Results for: '{metadata.get('query', 'Unknown')}'\n"
        output += "=" * 60 + "\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"🏆 Result #{i} (Score: {result['similarity']:.3f})\n"
            output += f"📚 Knowledge Base: {result['knowledge_base']}\n"
            output += f"📄 File: {result['file_name']}\n"
            output += f"🔢 Chunk ID: {result['chunk_id']}\n"
            output += f"📝 Tokens: {result['tokens']}\n"
            output += f"📖 Content:\n{result['text'][:300]}...\n"
            output += "-" * 40 + "\n\n"
        
        # Add metadata if requested
        if include_metadata and metadata:
            output += "📊 Search Metadata:\n"
            output += "-" * 20 + "\n"
            output += f"🔍 Query: {metadata.get('query', 'Unknown')}\n"
            output += f"📚 KBs searched: {len(metadata.get('knowledge_bases_searched', []))}\n"
            output += f"📄 Total found: {metadata.get('total_results_found', 0)}\n"
            output += f"✅ After filtering: {metadata.get('results_after_filtering', 0)}\n"
            output += f"⏱️  Search time: {metadata.get('search_time_seconds', 0)}s\n"
            output += f"📅 Timestamp: {metadata.get('search_timestamp', 'Unknown')}\n"
        
        return output
    
    def export_search_results(self, 
                            search_results: Dict[str, Any], 
                            output_file: str,
                            format: str = "json") -> bool:
        """
        Export search results to a file.
        
        Args:
            search_results: Results from search() method
            output_file: Output file path
            format: Export format ("json" or "txt")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if format.lower() == "json":
                with open(output_file, "w") as f:
                    json.dump(search_results, f, indent=2)
            elif format.lower() == "txt":
                formatted_results = self.format_search_results(search_results, include_metadata=True)
                with open(output_file, "w") as f:
                    f.write(formatted_results)
            else:
                print(f"❌ Unsupported format: {format}")
                return False
            
            print(f"✅ Search results exported to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
            return False
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about loaded knowledge bases.
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "total_kbs_loaded": len(self.loaded_kbs),
            "loaded_kb_names": list(self.loaded_kbs.keys()),
            "total_chunks": 0,
            "total_files": 0
        }
        
        for kb_name, kb in self.loaded_kbs.items():
            if kb_name in kb.knowledge_bases:
                kb_data = kb.knowledge_bases[kb_name]
                stats["total_chunks"] += len(kb_data["chunks"])
                stats["total_files"] += kb_data["metadata"]["total_files"]
        
        return stats

def demo_query_interface():
    """
    Demo the Query Interface functionality.
    """
    print("🎯 Query Interface Demo")
    print("=" * 50)
    
    # Initialize the query interface
    query_interface = KnowledgeBaseQueryInterface()
    
    # List available knowledge bases
    print("\n📋 Available Knowledge Bases:")
    print("-" * 40)
    available_kbs = query_interface.list_available_knowledge_bases()
    
    if not available_kbs:
        print("❌ No knowledge bases found")
        return
    
    for kb in available_kbs:
        status = "✅ Loaded" if kb["loaded"] else "⏳ Not loaded"
        print(f"📚 {kb['name']} - {status}")
        print(f"   📄 Chunks: {kb['total_chunks']}")
        print(f"   📁 Files: {kb['total_files']}")
    
    # Load all knowledge bases
    print(f"\n📚 Loading all knowledge bases...")
    loaded_count = query_interface.load_all_knowledge_bases()
    
    if loaded_count == 0:
        print("❌ No knowledge bases loaded")
        return
    
    # Get statistics
    stats = query_interface.get_search_statistics()
    print(f"\n📊 Loaded Knowledge Bases Statistics:")
    print(f"   📚 Total KBs: {stats['total_kbs_loaded']}")
    print(f"   📄 Total chunks: {stats['total_chunks']}")
    print(f"   📁 Total files: {stats['total_files']}")
    
    # Perform searches
    test_queries = [
        "What is machine learning?",
        "How to make pasta?",
        "What is the vacation policy?",
        "artificial intelligence"
    ]
    
    print(f"\n🔍 Testing Searches:")
    print("-" * 30)
    
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        
        # Search across all knowledge bases
        results = query_interface.search(query, top_k=3, similarity_threshold=0.3)
        
        if "error" not in results and results["results"]:
            print(f"✅ Found {len(results['results'])} results")
            
            # Show top result
            top_result = results["results"][0]
            print(f"🏆 Top result: {top_result['knowledge_base']} (score: {top_result['similarity']:.3f})")
            print(f"   📄 {top_result['text'][:100]}...")
        else:
            print("❌ No results found")
    
    # Test single KB search
    print(f"\n🎯 Single KB Search Test:")
    print("-" * 30)
    
    if "ai_knowledge" in stats["loaded_kb_names"]:
        results = query_interface.search_single_kb(
            "ai_knowledge", 
            "What is artificial intelligence?",
            top_k=2
        )
        
        if "error" not in results and results["results"]:
            print(f"✅ Found {len(results['results'])} results in ai_knowledge")
            for result in results["results"]:
                print(f"   📄 {result['text'][:80]}...")
    
    # Export results
    print(f"\n💾 Export Test:")
    print("-" * 20)
    
    results = query_interface.search("machine learning", top_k=2)
    if "error" not in results:
        # Export to JSON
        query_interface.export_search_results(results, "search_results.json", "json")
        
        # Export to text
        query_interface.export_search_results(results, "search_results.txt", "txt")
    
    print(f"\n✅ Query Interface demo completed!")

if __name__ == "__main__":
    demo_query_interface()
