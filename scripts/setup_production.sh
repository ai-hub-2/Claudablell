#!/bin/bash

# Production Setup Script for Claudable
# This script sets up the complete production environment

set -e

echo "🚀 Setting up Claudable for Production..."

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "apps" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# 1. Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# 2. Install Python dependencies
echo "📦 Installing Python dependencies..."
cd apps/api
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
cd ../..

# 3. Install AI Agent CLI tools
echo "🤖 Installing AI Agent CLI tools..."
export PATH="$HOME/.local/bin:$PATH"
npm run install:agents

# 4. Set up environment variables
echo "🔧 Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please edit .env file with your actual API keys"
fi

# 5. Initialize database
echo "🗄️  Initializing database..."
cd apps/api
source .venv/bin/activate
python -c "
from app.db.session import engine
from app.db.base import Base
Base.metadata.create_all(bind=engine)
print('✅ Database initialized')
"
cd ../..

# 6. Test all components
echo "🧪 Testing all components..."
export PATH="$HOME/.local/bin:$PATH"

echo "Testing database..."
python3 scripts/check_database.py

echo "Testing agents..."
python3 scripts/check_agents.py

echo "Testing build..."
npm run build

echo ""
echo "🎉 Production setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Login to agents: claude login, cursor-agent login"
echo "3. Start the application: npm run dev"
echo "4. Or deploy to Render: git push origin main"
echo ""
echo "🔧 Available commands:"
echo "  npm run dev          - Start development server"
echo "  npm run build        - Build for production"
echo "  npm run check:all    - Test all components"
echo "  npm run setup:agents - Reinstall agents"