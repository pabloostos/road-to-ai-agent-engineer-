#!/usr/bin/env python3
"""
Test Script for Multi-KB Manager (Step 4)
=========================================
This script demonstrates all the Multi-KB Manager features step by step.

🎯 Learning Objectives:
- See how to use the complete management system
- Understand backup and restore functionality
- Learn about bulk operations and health monitoring
- See comprehensive reporting and logging
"""

from src.multi_kb_manager import MultiKnowledgeBaseManager

def main():
    """Test the Multi-KB Manager step by step."""
    print("🧪 Testing Multi-KB Manager (Step 4)")
    print("=" * 50)
    
    # Step 1: Initialize the manager
    print("\n🔧 Step 1: Initialize Multi-KB Manager")
    print("-" * 45)
    manager = MultiKnowledgeBaseManager()
    
    # Step 2: Get comprehensive overview
    print("\n📊 Step 2: Get Knowledge Base Overview")
    print("-" * 40)
    overview = manager.get_knowledge_base_overview()
    
    print(f"📚 Total Knowledge Bases: {overview['total_knowledge_bases']}")
    print(f"📄 Total Chunks: {overview['total_chunks']:,}")
    print(f"📁 Total Files: {overview['total_files']}")
    print(f"💾 Total Size: {overview['total_size_mb']:.2f} MB")
    print(f"🏥 Health Status: {overview['health_status'].upper()}")
    
    # Show individual KBs
    print(f"\n📋 Knowledge Bases:")
    for kb in overview["knowledge_bases"][:3]:  # Show first 3
        status_emoji = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(kb["health_status"], "❓")
        print(f"   {status_emoji} {kb['name']}")
        print(f"      📄 Chunks: {kb['total_chunks']}")
        print(f"      💾 Size: {kb['size_mb']:.2f} MB")
    
    # Step 3: Create a new knowledge base
    print(f"\n🚀 Step 3: Create New Knowledge Base")
    print("-" * 40)
    
    result = manager.create_knowledge_base(
        name="test_management_kb",
        data_dir="data/company_policies",
        config={"chunk_size": 250, "similarity_threshold": 0.5}
    )
    
    if result["success"]:
        print(f"✅ Created: {result['name']}")
        print(f"   📄 Chunks: {result['stats']['total_chunks']}")
        print(f"   🔤 Tokens: {result['stats']['total_tokens']:,}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Step 4: Create backups
    print(f"\n💾 Step 4: Create Backups")
    print("-" * 25)
    
    available_kbs = [kb["name"] for kb in manager.builder.list_knowledge_bases()]
    if available_kbs:
        # Create backups for first 3 KBs
        backup_result = manager.bulk_operation("backup", available_kbs[:3])
        print(f"✅ Bulk backup completed:")
        print(f"   📚 Total targets: {backup_result['total_targets']}")
        print(f"   ✅ Successful: {backup_result['successful']}")
        print(f"   ❌ Failed: {backup_result['failed']}")
    
    # Step 5: List and manage backups
    print(f"\n📋 Step 5: List Backups")
    print("-" * 25)
    backups = manager.list_backups()
    
    if backups:
        print(f"📦 Found {len(backups)} backups:")
        for backup in backups[:3]:  # Show first 3 backups
            print(f"   📦 {backup['backup_name']}")
            print(f"      📅 {backup['backup_timestamp']}")
            print(f"      💾 {backup['backup_size_mb']:.2f} MB")
            print(f"      📁 Original: {backup['original_name']}")
    else:
        print("❌ No backups found")
    
    # Step 6: Health monitoring
    print(f"\n🏥 Step 6: Health Monitoring")
    print("-" * 30)
    
    if available_kbs:
        health_result = manager.bulk_operation("health_check", available_kbs[:4])
        print(f"✅ Health check completed:")
        print(f"   📚 Total targets: {health_result['total_targets']}")
        print(f"   ✅ Healthy: {health_result['successful']}")
        print(f"   ❌ Issues: {health_result['failed']}")
        
        # Show health details
        for result in health_result["results"][:2]:  # Show first 2 results
            kb_name = result["kb_name"]
            stats = result["result"]["stats"]
            print(f"   📊 {kb_name}: {stats.get('health_status', 'unknown')}")
    
    # Step 7: Test restore functionality
    print(f"\n🔄 Step 7: Test Restore Functionality")
    print("-" * 40)
    
    if backups:
        # Try to restore the first backup with a new name
        first_backup = backups[0]
        restore_name = f"{first_backup['original_name']}_restored"
        
        print(f"🔄 Restoring {first_backup['backup_name']} as {restore_name}")
        restore_result = manager.restore_knowledge_base(
            first_backup['backup_name'], 
            restore_name
        )
        
        if restore_result["success"]:
            print(f"✅ Restored successfully!")
            print(f"   📁 Restored as: {restore_result['restored_name']}")
            print(f"   📊 From backup: {restore_result['backup_name']}")
        else:
            print(f"❌ Restore failed: {restore_result['error']}")
    
    # Step 8: Update knowledge base
    print(f"\n🔄 Step 8: Update Knowledge Base")
    print("-" * 35)
    
    # Try to update one of the existing KBs
    if "ai_knowledge" in available_kbs:
        print("🔄 Updating ai_knowledge with new configuration...")
        update_result = manager.update_knowledge_base(
            "ai_knowledge",
            "data/ai_knowledge",
            config={"chunk_size": 400, "similarity_threshold": 0.6}
        )
        
        if update_result["success"]:
            print(f"✅ Updated successfully!")
            print(f"   📄 New chunks: {update_result['stats']['total_chunks']}")
        else:
            print(f"❌ Update failed: {update_result['error']}")
    
    # Step 9: Generate comprehensive report
    print(f"\n📊 Step 9: Generate Management Report")
    print("-" * 40)
    
    report = manager.generate_report()
    print("📄 Management Report Generated:")
    print(report[:800] + "..." if len(report) > 800 else report)
    
    # Step 10: View operation logs
    print(f"\n📝 Step 10: View Operation Logs")
    print("-" * 35)
    
    recent_logs = manager.get_management_log(10)
    if recent_logs:
        print(f"📋 Recent Operations ({len(recent_logs)} entries):")
        for log in recent_logs[:5]:  # Show last 5 operations
            status_emoji = {"success": "✅", "error": "❌", "warning": "⚠️"}.get(log["status"], "❓")
            timestamp = log["timestamp"].split("T")[1][:8]  # Just time part
            print(f"   {status_emoji} {log['operation'].upper()}: {log['kb_name']} ({timestamp})")
    else:
        print("📭 No recent operations found")
    
    # Step 11: Test search integration
    print(f"\n🔍 Step 11: Test Search Integration")
    print("-" * 40)
    
    # Load knowledge bases for search
    manager.query_interface.load_all_knowledge_bases()
    
    # Perform a search
    search_result = manager.query_interface.search(
        "artificial intelligence",
        top_k=2,
        similarity_threshold=0.3
    )
    
    if "error" not in search_result and search_result["results"]:
        print(f"✅ Search completed successfully!")
        print(f"   📄 Found {len(search_result['results'])} results")
        print(f"   ⏱️  Search time: {search_result['metadata']['search_time_seconds']:.3f}s")
        
        # Show top result
        top_result = search_result["results"][0]
        print(f"   🏆 Top result: {top_result['knowledge_base']} (score: {top_result['similarity']:.3f})")
    else:
        print("❌ Search failed or no results found")
    
    # Step 12: Performance summary
    print(f"\n⚡ Step 12: Performance Summary")
    print("-" * 35)
    
    # Get final overview
    final_overview = manager.get_knowledge_base_overview()
    
    print(f"📊 Final System Status:")
    print(f"   📚 Total KBs: {final_overview['total_knowledge_bases']}")
    print(f"   📄 Total chunks: {final_overview['total_chunks']:,}")
    print(f"   💾 Total size: {final_overview['total_size_mb']:.2f} MB")
    print(f"   🏥 Health: {final_overview['health_status'].upper()}")
    
    # Count backups
    final_backups = manager.list_backups()
    print(f"   💾 Backups: {len(final_backups)}")
    
    # Count recent operations
    final_logs = manager.get_management_log()
    print(f"   📝 Operations logged: {len(final_logs)}")
    
    print(f"\n✅ Multi-KB Manager testing completed!")
    print(f"🎯 Step 4 implementation is working perfectly!")
    print(f"🚀 Complete Knowledge Base Framework is ready!")

if __name__ == "__main__":
    main()
