#!/usr/bin/env python3
"""
Agent Configuration Script for Claudable
This script helps configure and test all AI agents
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the API directory to the path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

from app.services.cli.adapters import ClaudeCodeCLI, CursorAgentCLI, QwenCLI, GeminiCLI, CodexCLI

async def configure_agent(agent_class, name):
    """Configure and test an agent"""
    try:
        print(f"\n🔧 Configuring {name}...")
        agent = agent_class()
        
        # Check availability
        status = await agent.check_availability()
        
        if status.get("available", False):
            print(f"✅ {name}: Available and configured")
            
            # Show supported models
            models = status.get("models", [])
            if models:
                print(f"   📋 Supported models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
            
            return True
        else:
            print(f"❌ {name}: {status.get('error', 'Not available')}")
            return False
            
    except Exception as e:
        print(f"❌ {name}: Configuration error - {e}")
        return False

async def main():
    """Main configuration function"""
    print("🚀 Configuring AI Agents for Claudable...")
    print("=" * 60)
    
    agents = [
        (ClaudeCodeCLI, "Claude Code CLI"),
        (CursorAgentCLI, "Cursor Agent CLI"),
        (CodexCLI, "Codex CLI"),
        (QwenCLI, "Qwen CLI"),
        (GeminiCLI, "Gemini CLI"),
    ]
    
    configured_count = 0
    total_count = len(agents)
    
    for agent_class, name in agents:
        if await configure_agent(agent_class, name):
            configured_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Configuration Summary: {configured_count}/{total_count} agents configured")
    
    if configured_count == 0:
        print("⚠️  No agents configured! Please install CLI tools first:")
        print("   Run: bash scripts/install_agents.sh")
        return False
    elif configured_count < total_count:
        print("⚠️  Some agents not configured. Check installation and login status.")
        return True
    else:
        print("🎉 All agents configured successfully!")
        return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)