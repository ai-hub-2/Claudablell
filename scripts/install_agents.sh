#!/bin/bash

# Agent Installation Script for Claudable
# This script installs all required CLI tools for the AI agents

set -e

echo "🚀 Installing AI Agent CLI Tools..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Install Claude Code CLI
echo "📦 Installing Claude Code CLI..."
if npm install -g @anthropic-ai/claude-code; then
    echo "✅ Claude Code CLI installed successfully"
else
    echo "⚠️  Failed to install Claude Code CLI. You may need to run with sudo."
    echo "   Try: sudo npm install -g @anthropic-ai/claude-code"
fi

# Install OpenAI Codex CLI
echo "📦 Installing OpenAI Codex CLI..."
if npm install -g @openai/codex; then
    echo "✅ OpenAI Codex CLI installed successfully"
else
    echo "⚠️  Failed to install OpenAI Codex CLI. You may need to run with sudo."
    echo "   Try: sudo npm install -g @openai/codex"
fi

# Install Cursor Agent CLI
echo "📦 Installing Cursor Agent CLI..."
if curl -fsSL https://cursor.com/install | bash; then
    echo "✅ Cursor Agent CLI installed successfully"
else
    echo "⚠️  Failed to install Cursor Agent CLI."
    echo "   Please visit: https://cursor.com/install"
fi

# Install Qwen CLI (if available)
echo "📦 Installing Qwen CLI..."
if npm install -g @qwen-code/qwen-code 2>/dev/null; then
    echo "✅ Qwen CLI installed successfully"
else
    echo "⚠️  Qwen CLI not available via npm. Please install manually."
    echo "   Visit: https://github.com/QwenLM/Qwen"
fi

# Install Gemini CLI (if available)
echo "📦 Installing Gemini CLI..."
if npm install -g @google/gemini-cli 2>/dev/null; then
    echo "✅ Gemini CLI installed successfully"
else
    echo "⚠️  Gemini CLI not available via npm. Please install manually."
    echo "   Visit: https://aistudio.google.com/"
fi

echo ""
echo "🎉 Agent installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Login to Claude: claude login"
echo "2. Login to Cursor: cursor-agent login"
echo "3. Set up API keys in the application settings"
echo "4. Test agents: npm run check:agents"
echo ""
echo "🔧 If you encounter permission issues, try running with sudo:"
echo "   sudo bash scripts/install_agents.sh"