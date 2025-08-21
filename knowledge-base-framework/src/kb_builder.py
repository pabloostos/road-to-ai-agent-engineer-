#!/usr/bin/env python3
"""
Step 2: KB Builder
==================
Simple interface for building knowledge bases from text files.

This module provides a user-friendly way to:
1. Select text files to process
2. Configure chunking and embedding settings
3. Create knowledge bases with progress feedback
4. Validate the created knowledge bases

🎯 Learning Objectives:
- Understand how to build a user-friendly interface
- Learn about configuration management
- See how to provide progress feedback
- Understand validation and error handling
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from kb_framework import UniversalKnowledgeBase

class KnowledgeBaseBuilder:
    """
    Simple Knowledge Base Builder
    
    This class provides a user-friendly interface for creating knowledge bases.
    It handles all the complexity of the UniversalKnowledgeBase framework
    and presents a simple, easy-to-use API.
    
    🎯 Key Features:
    - Simple file selection
    - Configurable settings
    - Progress feedback
    - Validation and error handling
    - Easy-to-understand interface
    """
    
    def __init__(self, base_dir: str = "knowledge_bases"):
        """
        Initialize the KB Builder.
        
        Args:
            base_dir: Directory where knowledge bases will be stored
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "embedding_model": "all-MiniLM-L6-v2",
            "chunk_size": 500,
            "overlap_size": 50,
            "similarity_threshold": 0.3
        }
        
        print("🔧 KB Builder initialized!")
        print(f"   📁 Storage directory: {self.base_dir}")
        print(f"   ⚙️  Default settings loaded")
    
    def list_available_files(self, data_dir: str) -> List[Dict[str, Any]]:
        """
        List all available text files in a directory.
        
        This method helps users see what files they can use to create
        knowledge bases. It provides file information like size and
        last modified date.
        
        Args:
            data_dir: Directory to scan for text files
            
        Returns:
            List of file information dictionaries
        """
        data_path = Path(data_dir)
        if not data_path.exists():
            print(f"❌ Directory not found: {data_dir}")
            return []
        
        # Find all .txt files
        txt_files = list(data_path.glob("*.txt"))
        
        file_info = []
        for file_path in txt_files:
            stat = file_path.stat()
            file_info.append({
                "name": file_path.name,
                "path": str(file_path),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "lines": len(file_path.read_text().splitlines())
            })
        
        return file_info
    
    def validate_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Validate that files exist and are readable.
        
        This method checks if the selected files are valid before
        processing them. It helps prevent errors during KB creation.
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Validation results with status and details
        """
        results = {
            "valid": True,
            "files": [],
            "errors": []
        }
        
        for file_path in file_paths:
            path = Path(file_path)
            file_info = {
                "path": str(path),
                "name": path.name,
                "exists": path.exists(),
                "readable": False,
                "size": 0,
                "error": None
            }
            
            if not path.exists():
                file_info["error"] = "File does not exist"
                results["errors"].append(f"File not found: {file_path}")
                results["valid"] = False
            else:
                try:
                    # Try to read the file
                    content = path.read_text(encoding="utf-8")
                    file_info["readable"] = True
                    file_info["size"] = len(content)
                    
                    if len(content.strip()) == 0:
                        file_info["error"] = "File is empty"
                        results["errors"].append(f"Empty file: {file_path}")
                        results["valid"] = False
                        
                except Exception as e:
                    file_info["error"] = str(e)
                    results["errors"].append(f"Cannot read file {file_path}: {e}")
                    results["valid"] = False
            
            results["files"].append(file_info)
        
        return results
    
    def create_knowledge_base(self, 
                            name: str, 
                            data_dir: str, 
                            config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a knowledge base with progress feedback.
        
        This is the main method that creates a knowledge base. It provides
        detailed progress feedback so users can see what's happening.
        
        Args:
            name: Name for the knowledge base
            data_dir: Directory containing text files
            config: Optional configuration overrides
            
        Returns:
            Creation results with status and details
        """
        print(f"\n🚀 Creating Knowledge Base: {name}")
        print("=" * 50)
        
        # Step 1: Validate inputs
        print("📋 Step 1: Validating inputs...")
        if not name or not name.strip():
            return {"success": False, "error": "Knowledge base name is required"}
        
        # Step 2: List available files
        print("📄 Step 2: Scanning for text files...")
        available_files = self.list_available_files(data_dir)
        if not available_files:
            return {"success": False, "error": f"No text files found in {data_dir}"}
        
        print(f"   ✅ Found {len(available_files)} text files:")
        for file_info in available_files:
            print(f"      • {file_info['name']} ({file_info['size_mb']} MB, {file_info['lines']} lines)")
        
        # Step 3: Validate files
        print("🔍 Step 3: Validating files...")
        file_paths = [file_info["path"] for file_info in available_files]
        validation = self.validate_files(file_paths)
        
        if not validation["valid"]:
            print("   ❌ Validation failed:")
            for error in validation["errors"]:
                print(f"      • {error}")
            return {"success": False, "error": "File validation failed", "details": validation}
        
        print("   ✅ All files are valid!")
        
        # Step 4: Merge configuration
        print("⚙️  Step 4: Applying configuration...")
        final_config = {**self.default_config}
        if config:
            final_config.update(config)
        
        print(f"   📊 Configuration:")
        print(f"      • Embedding model: {final_config['embedding_model']}")
        print(f"      • Chunk size: {final_config['chunk_size']} tokens")
        print(f"      • Overlap size: {final_config['overlap_size']} tokens")
        print(f"      • Similarity threshold: {final_config['similarity_threshold']}")
        
        # Step 5: Create knowledge base
        print("🔧 Step 5: Initializing framework...")
        try:
            kb = UniversalKnowledgeBase(
                embedding_model=final_config["embedding_model"],
                chunk_size=final_config["chunk_size"],
                overlap_size=final_config["overlap_size"],
                similarity_threshold=final_config["similarity_threshold"]
            )
        except Exception as e:
            return {"success": False, "error": f"Failed to initialize framework: {e}"}
        
        print("   ✅ Framework initialized successfully!")
        
        # Step 6: Process files
        print("📖 Step 6: Processing files...")
        try:
            success = kb.create_knowledge_base(name, data_dir)
            if not success:
                return {"success": False, "error": "Failed to create knowledge base"}
        except Exception as e:
            return {"success": False, "error": f"Error during processing: {e}"}
        
        # Step 7: Validate results
        print("✅ Step 7: Validating results...")
        try:
            stats = kb.get_kb_stats(name)
            if "error" in stats:
                return {"success": False, "error": f"Failed to get KB stats: {stats['error']}"}
        except Exception as e:
            return {"success": False, "error": f"Error getting stats: {e}"}
        
        # Step 8: Success!
        print("🎉 Step 8: Knowledge base created successfully!")
        print(f"   📊 Summary:")
        print(f"      • Name: {name}")
        print(f"      • Files processed: {stats['total_chunks']}")
        print(f"      • Total chunks: {stats['total_chunks']}")
        print(f"      • Total tokens: {stats['total_tokens']:,}")
        print(f"      • Average tokens per chunk: {stats['average_tokens_per_chunk']}")
        print(f"      • Storage location: {self.base_dir / name}")
        
        return {
            "success": True,
            "name": name,
            "stats": stats,
            "config": final_config,
            "files_processed": len(available_files)
        }
    
    def list_knowledge_bases(self) -> List[Dict[str, Any]]:
        """
        List all created knowledge bases.
        
        Returns:
            List of knowledge base information
        """
        kb_list = []
        
        if not self.base_dir.exists():
            return kb_list
        
        for kb_dir in self.base_dir.iterdir():
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
                            "path": str(kb_dir)
                        }
                        kb_list.append(kb_info)
                    except Exception as e:
                        print(f"⚠️  Error reading KB {kb_dir.name}: {e}")
        
        return kb_list
    
    def delete_knowledge_base(self, name: str) -> Dict[str, Any]:
        """
        Delete a knowledge base.
        
        Args:
            name: Name of the knowledge base to delete
            
        Returns:
            Deletion results
        """
        kb_dir = self.base_dir / name
        
        if not kb_dir.exists():
            return {"success": False, "error": f"Knowledge base '{name}' not found"}
        
        try:
            import shutil
            shutil.rmtree(kb_dir)
            return {"success": True, "message": f"Knowledge base '{name}' deleted successfully"}
        except Exception as e:
            return {"success": False, "error": f"Failed to delete knowledge base: {e}"}

def demo_kb_builder():
    """
    Demo the KB Builder functionality.
    
    This function shows how to use the KB Builder step by step.
    """
    print("🎯 KB Builder Demo")
    print("=" * 50)
    
    # Initialize the builder
    builder = KnowledgeBaseBuilder()
    
    # List available files
    print("\n📄 Available Files:")
    print("-" * 30)
    available_files = builder.list_available_files("data/ai_knowledge")
    
    if not available_files:
        print("❌ No text files found in data/ai_knowledge directory")
        return
    
    for file_info in available_files:
        print(f"📄 {file_info['name']}")
        print(f"   📊 Size: {file_info['size_mb']} MB")
        print(f"   📝 Lines: {file_info['lines']}")
        print(f"   📅 Modified: {file_info['modified']}")
    
    # Create a knowledge base with custom config
    print(f"\n🚀 Creating Knowledge Base with Custom Config:")
    print("-" * 50)
    
    custom_config = {
        "chunk_size": 300,  # Smaller chunks for more granular search
        "overlap_size": 30,  # Less overlap
        "similarity_threshold": 0.4  # Higher threshold for better quality
    }
    
    result = builder.create_knowledge_base(
        name="demo_kb",
        data_dir="data/ai_knowledge",
        config=custom_config
    )
    
    if result["success"]:
        print(f"\n✅ Success! Knowledge base created:")
        print(f"   📊 Stats: {result['stats']}")
    else:
        print(f"\n❌ Failed: {result['error']}")
    
    # List all knowledge bases
    print(f"\n📋 All Knowledge Bases:")
    print("-" * 30)
    kbs = builder.list_knowledge_bases()
    
    if kbs:
        for kb in kbs:
            print(f"📚 {kb['name']}")
            print(f"   📅 Created: {kb['created_at']}")
            print(f"   📄 Chunks: {kb['total_chunks']}")
            print(f"   📁 Files: {kb['total_files']}")
    else:
        print("No knowledge bases found")

if __name__ == "__main__":
    demo_kb_builder()
