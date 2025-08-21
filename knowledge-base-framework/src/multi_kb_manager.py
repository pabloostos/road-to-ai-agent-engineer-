#!/usr/bin/env python3
"""
Step 4: Multi-KB Manager
========================
Comprehensive interface for managing multiple knowledge bases.

This module provides a complete management system for:
1. Creating, updating, and deleting knowledge bases
2. Monitoring KB health and performance
3. Managing KB metadata and configurations
4. Bulk operations across multiple KBs
5. Backup and restore functionality

🎯 Learning Objectives:
- Understand how to build a comprehensive management system
- Learn about bulk operations and batch processing
- See how to monitor and maintain KB health
- Understand backup and restore strategies
"""

import json
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from kb_framework import UniversalKnowledgeBase
from kb_builder import KnowledgeBaseBuilder
from kb_query_interface import KnowledgeBaseQueryInterface

class MultiKnowledgeBaseManager:
    """
    Comprehensive Multi-Knowledge Base Manager
    
    This class provides a complete management system for multiple knowledge bases.
    It combines the functionality of the KB Builder, Query Interface, and adds
    advanced management features like monitoring, backup, and bulk operations.
    
    🎯 Key Features:
    - Complete KB lifecycle management
    - Health monitoring and diagnostics
    - Backup and restore functionality
    - Bulk operations across multiple KBs
    - Performance analytics and reporting
    - Configuration management
    """
    
    def __init__(self, kb_base_dir: str = "knowledge_bases"):
        """
        Initialize the Multi-KB Manager.
        
        Args:
            kb_base_dir: Directory containing knowledge bases
        """
        self.kb_base_dir = Path(kb_base_dir)
        self.kb_base_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.builder = KnowledgeBaseBuilder(str(self.kb_base_dir))
        self.query_interface = KnowledgeBaseQueryInterface(str(self.kb_base_dir))
        
        # Management state
        self.management_log = []
        self.health_checks = {}
        
        print("🏢 Multi-KB Manager initialized!")
        print(f"   📁 Knowledge bases directory: {self.kb_base_dir}")
        print(f"   🔧 Builder component: Ready")
        print(f"   🔍 Query interface: Ready")
    
    def get_knowledge_base_overview(self) -> Dict[str, Any]:
        """
        Get comprehensive overview of all knowledge bases.
        
        Returns:
            Overview dictionary with statistics and status
        """
        print("📊 Generating Knowledge Base Overview...")
        
        available_kbs = self.builder.list_knowledge_bases()
        
        overview = {
            "total_knowledge_bases": len(available_kbs),
            "total_chunks": 0,
            "total_files": 0,
            "total_size_mb": 0,
            "knowledge_bases": [],
            "health_status": "unknown",
            "last_updated": datetime.now().isoformat()
        }
        
        for kb_info in available_kbs:
            kb_name = kb_info["name"]
            kb_stats = self._get_detailed_kb_stats(kb_name)
            
            overview["total_chunks"] += kb_stats.get("total_chunks", 0)
            overview["total_files"] += kb_stats.get("total_files", 0)
            overview["total_size_mb"] += kb_stats.get("size_mb", 0)
            
            kb_overview = {
                "name": kb_name,
                "created_at": kb_info["created_at"],
                "total_chunks": kb_stats.get("total_chunks", 0),
                "total_files": kb_stats.get("total_files", 0),
                "size_mb": kb_stats.get("size_mb", 0),
                "embedding_model": kb_info["embedding_model"],
                "health_status": kb_stats.get("health_status", "unknown"),
                "last_accessed": kb_stats.get("last_accessed", "never")
            }
            
            overview["knowledge_bases"].append(kb_overview)
        
        # Determine overall health status
        health_statuses = [kb["health_status"] for kb in overview["knowledge_bases"]]
        if all(status == "healthy" for status in health_statuses):
            overview["health_status"] = "healthy"
        elif any(status == "error" for status in health_statuses):
            overview["health_status"] = "error"
        else:
            overview["health_status"] = "warning"
        
        return overview
    
    def _get_detailed_kb_stats(self, kb_name: str) -> Dict[str, Any]:
        """
        Get detailed statistics for a specific knowledge base.
        
        Args:
            kb_name: Name of the knowledge base
            
        Returns:
            Detailed statistics dictionary
        """
        kb_dir = self.kb_base_dir / kb_name
        
        if not kb_dir.exists():
            return {"error": f"Knowledge base '{kb_name}' not found"}
        
        try:
            # Get basic stats
            metadata_file = kb_dir / "metadata.json"
            embeddings_file = kb_dir / "embeddings.jsonl"
            
            if not metadata_file.exists() or not embeddings_file.exists():
                return {"health_status": "error", "error": "Missing required files"}
            
            # Read metadata
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Calculate size
            size_mb = sum(f.stat().st_size for f in kb_dir.rglob("*") if f.is_file()) / (1024 * 1024)
            
            # Count chunks
            chunk_count = 0
            with open(embeddings_file, "r") as f:
                for line in f:
                    chunk_count += 1
            
            # Check health
            health_status = "healthy"
            if chunk_count != metadata.get("total_chunks", 0):
                health_status = "warning"
            
            return {
                "total_chunks": chunk_count,
                "total_files": metadata.get("total_files", 0),
                "size_mb": round(size_mb, 2),
                "health_status": health_status,
                "last_accessed": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"health_status": "error", "error": str(e)}
    
    def create_knowledge_base(self, name: str, data_dir: str, 
                            config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new knowledge base with management features.
        
        Args:
            name: Name for the knowledge base
            data_dir: Directory containing text files
            config: Optional configuration overrides
            
        Returns:
            Creation results with management metadata
        """
        print(f"🚀 Creating Knowledge Base: {name}")
        print("=" * 50)
        
        # Check if KB already exists
        if (self.kb_base_dir / name).exists():
            return {
                "success": False,
                "error": f"Knowledge base '{name}' already exists"
            }
        
        # Create the knowledge base
        result = self.builder.create_knowledge_base(name, data_dir, config)
        
        if result["success"]:
            # Add management metadata
            management_info = {
                "created_by": "Multi-KB Manager",
                "creation_timestamp": datetime.now().isoformat(),
                "config_used": result.get("config", {}),
                "management_version": "1.0"
            }
            
            # Save management metadata
            kb_dir = self.kb_base_dir / name
            with open(kb_dir / "management.json", "w") as f:
                json.dump(management_info, f, indent=2)
            
            # Log the creation
            self._log_operation("create", name, "success", result)
            
            print(f"✅ Knowledge base '{name}' created successfully!")
            print(f"   📊 Management metadata saved")
            print(f"   📝 Operation logged")
        
        return result
    
    def update_knowledge_base(self, name: str, data_dir: str, 
                            config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update an existing knowledge base with new data.
        
        Args:
            name: Name of the knowledge base to update
            data_dir: Directory containing new text files
            config: Optional configuration overrides
            
        Returns:
            Update results
        """
        print(f"🔄 Updating Knowledge Base: {name}")
        print("=" * 50)
        
        # Check if KB exists
        if not (self.kb_base_dir / name).exists():
            return {
                "success": False,
                "error": f"Knowledge base '{name}' not found"
            }
        
        # Create backup before update
        backup_result = self.backup_knowledge_base(name)
        if not backup_result["success"]:
            return {
                "success": False,
                "error": f"Failed to create backup: {backup_result['error']}"
            }
        
        # Delete existing KB
        delete_result = self.delete_knowledge_base(name)
        if not delete_result["success"]:
            return {
                "success": False,
                "error": f"Failed to delete existing KB: {delete_result['error']}"
            }
        
        # Create new KB with same name
        result = self.create_knowledge_base(name, data_dir, config)
        
        if result["success"]:
            # Log the update
            self._log_operation("update", name, "success", result)
            
            print(f"✅ Knowledge base '{name}' updated successfully!")
            print(f"   💾 Backup created before update")
            print(f"   📝 Operation logged")
        
        return result
    
    def delete_knowledge_base(self, name: str) -> Dict[str, Any]:
        """
        Delete a knowledge base with confirmation.
        
        Args:
            name: Name of the knowledge base to delete
            
        Returns:
            Deletion results
        """
        print(f"🗑️  Deleting Knowledge Base: {name}")
        print("=" * 50)
        
        kb_dir = self.kb_base_dir / name
        
        if not kb_dir.exists():
            return {
                "success": False,
                "error": f"Knowledge base '{name}' not found"
            }
        
        try:
            # Get KB info before deletion
            kb_info = self._get_detailed_kb_stats(name)
            
            # Delete the directory
            shutil.rmtree(kb_dir)
            
            # Log the deletion
            self._log_operation("delete", name, "success", kb_info)
            
            print(f"✅ Knowledge base '{name}' deleted successfully!")
            print(f"   📊 Deleted {kb_info.get('total_chunks', 0)} chunks")
            print(f"   📁 Deleted {kb_info.get('total_files', 0)} files")
            print(f"   📝 Operation logged")
            
            return {
                "success": True,
                "message": f"Knowledge base '{name}' deleted successfully",
                "deleted_info": kb_info
            }
            
        except Exception as e:
            error_msg = f"Failed to delete knowledge base: {e}"
            self._log_operation("delete", name, "error", {"error": error_msg})
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def backup_knowledge_base(self, name: str, backup_dir: str = "backups") -> Dict[str, Any]:
        """
        Create a backup of a knowledge base.
        
        Args:
            name: Name of the knowledge base to backup
            backup_dir: Directory to store backups
            
        Returns:
            Backup results
        """
        print(f"💾 Creating Backup: {name}")
        print("=" * 50)
        
        kb_dir = self.kb_base_dir / name
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        if not kb_dir.exists():
            return {
                "success": False,
                "error": f"Knowledge base '{name}' not found"
            }
        
        try:
            # Create timestamped backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{name}_backup_{timestamp}"
            backup_location = backup_path / backup_name
            
            # Copy the knowledge base
            shutil.copytree(kb_dir, backup_location)
            
            # Create backup metadata
            backup_metadata = {
                "original_name": name,
                "backup_name": backup_name,
                "backup_timestamp": datetime.now().isoformat(),
                "backup_size_mb": sum(f.stat().st_size for f in backup_location.rglob("*") if f.is_file()) / (1024 * 1024),
                "backup_location": str(backup_location)
            }
            
            with open(backup_location / "backup_metadata.json", "w") as f:
                json.dump(backup_metadata, f, indent=2)
            
            # Log the backup
            self._log_operation("backup", name, "success", backup_metadata)
            
            print(f"✅ Backup created successfully!")
            print(f"   📁 Location: {backup_location}")
            print(f"   📊 Size: {backup_metadata['backup_size_mb']:.2f} MB")
            print(f"   📝 Operation logged")
            
            return {
                "success": True,
                "backup_name": backup_name,
                "backup_location": str(backup_location),
                "metadata": backup_metadata
            }
            
        except Exception as e:
            error_msg = f"Failed to create backup: {e}"
            self._log_operation("backup", name, "error", {"error": error_msg})
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def restore_knowledge_base(self, backup_name: str, restore_name: str = None) -> Dict[str, Any]:
        """
        Restore a knowledge base from backup.
        
        Args:
            backup_name: Name of the backup to restore
            restore_name: Name for the restored KB (defaults to original name)
            
        Returns:
            Restore results
        """
        print(f"🔄 Restoring from Backup: {backup_name}")
        print("=" * 50)
        
        backup_path = Path("backups") / backup_name
        
        if not backup_path.exists():
            return {
                "success": False,
                "error": f"Backup '{backup_name}' not found"
            }
        
        try:
            # Read backup metadata
            metadata_file = backup_path / "backup_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    backup_metadata = json.load(f)
                original_name = backup_metadata["original_name"]
            else:
                original_name = backup_name.split("_backup_")[0]
            
            # Use original name if no restore name specified
            if restore_name is None:
                restore_name = original_name
            
            # Check if restore target already exists
            if (self.kb_base_dir / restore_name).exists():
                return {
                    "success": False,
                    "error": f"Knowledge base '{restore_name}' already exists"
                }
            
            # Restore the knowledge base
            restore_location = self.kb_base_dir / restore_name
            shutil.copytree(backup_path, restore_location)
            
            # Update metadata
            if metadata_file.exists():
                restore_metadata = backup_metadata.copy()
                restore_metadata["restored_name"] = restore_name
                restore_metadata["restore_timestamp"] = datetime.now().isoformat()
                
                with open(restore_location / "restore_metadata.json", "w") as f:
                    json.dump(restore_metadata, f, indent=2)
            
            # Log the restore
            self._log_operation("restore", restore_name, "success", {
                "backup_name": backup_name,
                "original_name": original_name,
                "restore_location": str(restore_location)
            })
            
            print(f"✅ Knowledge base restored successfully!")
            print(f"   📁 Restored as: {restore_name}")
            print(f"   📊 From backup: {backup_name}")
            print(f"   📝 Operation logged")
            
            return {
                "success": True,
                "restored_name": restore_name,
                "original_name": original_name,
                "backup_name": backup_name
            }
            
        except Exception as e:
            error_msg = f"Failed to restore knowledge base: {e}"
            self._log_operation("restore", restore_name or backup_name, "error", {"error": error_msg})
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all available backups.
        
        Returns:
            List of backup information
        """
        backup_path = Path("backups")
        
        if not backup_path.exists():
            return []
        
        backups = []
        
        for backup_dir in backup_path.iterdir():
            if backup_dir.is_dir():
                metadata_file = backup_dir / "backup_metadata.json"
                
                if metadata_file.exists():
                    try:
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                        
                        backup_info = {
                            "backup_name": backup_dir.name,
                            "original_name": metadata.get("original_name", "unknown"),
                            "backup_timestamp": metadata.get("backup_timestamp", "unknown"),
                            "backup_size_mb": metadata.get("backup_size_mb", 0),
                            "backup_location": str(backup_dir)
                        }
                        backups.append(backup_info)
                    except Exception as e:
                        print(f"⚠️  Error reading backup {backup_dir.name}: {e}")
        
        return sorted(backups, key=lambda x: x["backup_timestamp"], reverse=True)
    
    def bulk_operation(self, operation: str, kb_names: List[str], 
                      **kwargs) -> Dict[str, Any]:
        """
        Perform bulk operations on multiple knowledge bases.
        
        Args:
            operation: Operation to perform ("backup", "delete", "health_check")
            kb_names: List of knowledge base names
            **kwargs: Additional operation-specific parameters
            
        Returns:
            Bulk operation results
        """
        print(f"🔄 Bulk Operation: {operation}")
        print("=" * 50)
        print(f"📚 Target Knowledge Bases: {', '.join(kb_names)}")
        
        results = {
            "operation": operation,
            "total_targets": len(kb_names),
            "successful": 0,
            "failed": 0,
            "results": []
        }
        
        for kb_name in kb_names:
            print(f"\n📋 Processing: {kb_name}")
            
            try:
                if operation == "backup":
                    result = self.backup_knowledge_base(kb_name, **kwargs)
                elif operation == "delete":
                    result = self.delete_knowledge_base(kb_name)
                elif operation == "health_check":
                    result = {"success": True, "stats": self._get_detailed_kb_stats(kb_name)}
                else:
                    result = {"success": False, "error": f"Unknown operation: {operation}"}
                
                if result["success"]:
                    results["successful"] += 1
                    print(f"   ✅ Success")
                else:
                    results["failed"] += 1
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                
                results["results"].append({
                    "kb_name": kb_name,
                    "success": result["success"],
                    "result": result
                })
                
            except Exception as e:
                results["failed"] += 1
                error_result = {"success": False, "error": str(e)}
                results["results"].append({
                    "kb_name": kb_name,
                    "success": False,
                    "result": error_result
                })
                print(f"   ❌ Exception: {e}")
        
        print(f"\n📊 Bulk Operation Summary:")
        print(f"   📚 Total targets: {results['total_targets']}")
        print(f"   ✅ Successful: {results['successful']}")
        print(f"   ❌ Failed: {results['failed']}")
        
        return results
    
    def _log_operation(self, operation: str, kb_name: str, status: str, details: Dict[str, Any]):
        """
        Log an operation for audit purposes.
        
        Args:
            operation: Type of operation
            kb_name: Name of the knowledge base
            status: Operation status
            details: Operation details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "kb_name": kb_name,
            "status": status,
            "details": details
        }
        
        self.management_log.append(log_entry)
        
        # Save to file
        log_file = self.kb_base_dir / "management_log.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_management_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent management operations log.
        
        Args:
            limit: Maximum number of log entries to return
            
        Returns:
            List of recent log entries
        """
        return self.management_log[-limit:] if self.management_log else []
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive management report.
        
        Returns:
            Formatted report string
        """
        print("📊 Generating Management Report...")
        
        overview = self.get_knowledge_base_overview()
        backups = self.list_backups()
        recent_logs = self.get_management_log(10)
        
        report = f"""
🏢 KNOWLEDGE BASE MANAGEMENT REPORT
{'='*60}

📊 OVERVIEW
   📚 Total Knowledge Bases: {overview['total_knowledge_bases']}
   📄 Total Chunks: {overview['total_chunks']:,}
   📁 Total Files: {overview['total_files']}
   💾 Total Size: {overview['total_size_mb']:.2f} MB
   🏥 Health Status: {overview['health_status'].upper()}
   📅 Last Updated: {overview['last_updated']}

📋 KNOWLEDGE BASES
"""
        
        for kb in overview["knowledge_bases"]:
            status_emoji = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(kb["health_status"], "❓")
            report += f"   {status_emoji} {kb['name']}\n"
            report += f"      📄 Chunks: {kb['total_chunks']}\n"
            report += f"      📁 Files: {kb['total_files']}\n"
            report += f"      💾 Size: {kb['size_mb']:.2f} MB\n"
            report += f"      🤖 Model: {kb['embedding_model']}\n"
            report += f"      📅 Created: {kb['created_at']}\n\n"
        
        report += f"💾 BACKUPS\n"
        if backups:
            report += f"   📁 Total Backups: {len(backups)}\n"
            for backup in backups[:5]:  # Show last 5 backups
                report += f"   📦 {backup['backup_name']}\n"
                report += f"      📅 {backup['backup_timestamp']}\n"
                report += f"      💾 {backup['backup_size_mb']:.2f} MB\n"
        else:
            report += f"   ❌ No backups found\n"
        
        report += f"\n📝 RECENT OPERATIONS\n"
        if recent_logs:
            for log in recent_logs:
                status_emoji = {"success": "✅", "error": "❌", "warning": "⚠️"}.get(log["status"], "❓")
                report += f"   {status_emoji} {log['operation'].upper()}: {log['kb_name']} ({log['timestamp']})\n"
        else:
            report += f"   📭 No recent operations\n"
        
        return report

def demo_multi_kb_manager():
    """
    Demo the Multi-KB Manager functionality.
    """
    print("🎯 Multi-KB Manager Demo")
    print("=" * 50)
    
    # Initialize the manager
    manager = MultiKnowledgeBaseManager()
    
    # Get overview
    print("\n📊 Knowledge Base Overview:")
    print("-" * 30)
    overview = manager.get_knowledge_base_overview()
    print(f"📚 Total KBs: {overview['total_knowledge_bases']}")
    print(f"📄 Total chunks: {overview['total_chunks']}")
    print(f"🏥 Health status: {overview['health_status']}")
    
    # Create a new knowledge base
    print(f"\n🚀 Creating New Knowledge Base:")
    print("-" * 35)
    
    result = manager.create_knowledge_base(
        name="demo_management_kb",
        data_dir="data/ai_knowledge",
        config={"chunk_size": 300, "similarity_threshold": 0.4}
    )
    
    if result["success"]:
        print(f"✅ Created: {result['name']}")
        print(f"   📄 Chunks: {result['stats']['total_chunks']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Create backups
    print(f"\n💾 Creating Backups:")
    print("-" * 25)
    
    available_kbs = [kb["name"] for kb in manager.builder.list_knowledge_bases()]
    if available_kbs:
        backup_result = manager.bulk_operation("backup", available_kbs[:2])  # Backup first 2 KBs
        print(f"✅ Backups created: {backup_result['successful']}/{backup_result['total_targets']}")
    
    # List backups
    print(f"\n📋 Available Backups:")
    print("-" * 25)
    backups = manager.list_backups()
    if backups:
        for backup in backups[:3]:  # Show first 3 backups
            print(f"📦 {backup['backup_name']}")
            print(f"   📅 {backup['backup_timestamp']}")
            print(f"   💾 {backup['backup_size_mb']:.2f} MB")
    else:
        print("❌ No backups found")
    
    # Health check
    print(f"\n🏥 Health Check:")
    print("-" * 20)
    if available_kbs:
        health_result = manager.bulk_operation("health_check", available_kbs[:3])
        print(f"✅ Health checks completed: {health_result['successful']}/{health_result['total_targets']}")
    
    # Generate report
    print(f"\n📊 Management Report:")
    print("-" * 25)
    report = manager.generate_report()
    print(report[:1000] + "..." if len(report) > 1000 else report)
    
    # Show recent operations
    print(f"\n📝 Recent Operations:")
    print("-" * 25)
    recent_logs = manager.get_management_log(5)
    if recent_logs:
        for log in recent_logs:
            status_emoji = {"success": "✅", "error": "❌"}.get(log["status"], "❓")
            print(f"{status_emoji} {log['operation'].upper()}: {log['kb_name']}")
    else:
        print("📭 No recent operations")
    
    print(f"\n✅ Multi-KB Manager demo completed!")

if __name__ == "__main__":
    demo_multi_kb_manager()
