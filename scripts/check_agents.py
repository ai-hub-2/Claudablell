#!/usr/bin/env python3
"""
Script to check if all AI agents are working correctly
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the API directory to the path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

from app.services.cli.adapters import ClaudeCodeCLI, CursorAgentCLI, QwenCLI, GeminiCLI, CodexCLI

async def check_agent(agent_class, name):
    """Check if an agent is available"""
    try:
        agent = agent_class()
        result = await agent.check_availability()
        if result.get("available", False):
            print(f"✅ {name}: Available")
            return True
        else:
            print(f"❌ {name}: {result.get('error', 'Not available')}")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

async def main():
    """Check all agents"""
    print("🔍 Checking AI Agents...")
    print("=" * 50)
    
    agents = [
        (ClaudeCodeCLI, "Claude Code CLI"),
        (CursorAgentCLI, "Cursor Agent CLI"),
        (QwenCLI, "Qwen CLI"),
        (GeminiCLI, "Gemini CLI"),
        (CodexCLI, "Codex CLI"),
    ]
    
    available_count = 0
    total_count = len(agents)
    
    for agent_class, name in agents:
        if await check_agent(agent_class, name):
            available_count += 1
    
    print("=" * 50)
    print(f"📊 Summary: {available_count}/{total_count} agents available")
    
    if available_count == 0:
        print("⚠️  No agents available! Check installation.")
        return False
    elif available_count < total_count:
        print("⚠️  Some agents not available. Check installation.")
        return True
    else:
        print("🎉 All agents available!")
        return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)