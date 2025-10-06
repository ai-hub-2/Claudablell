# 🤖 Claudable AI Agents

This document provides comprehensive information about all AI agents available in Claudable.

## 📋 Available Agents

### 1. **Claude Code CLI** (`claude`)
- **Provider**: Anthropic
- **Type**: CLI Tool via SDK
- **Models**: Claude Sonnet 4.5, Claude Opus 4.1, Claude Haiku 3.5
- **Installation**: `npm install -g @anthropic-ai/claude-code`
- **Login**: `claude login`
- **Features**: 
  - Direct SDK integration
  - Real-time streaming
  - Session management
  - Tool usage support

### 2. **Cursor Agent CLI** (`cursor`)
- **Provider**: Cursor
- **Type**: CLI Tool
- **Models**: GPT-5, Sonnet 4.5, Opus 4.1
- **Installation**: `curl https://cursor.com/install -fsS | bash`
- **Login**: `cursor-agent login`
- **Features**:
  - Stream-json format support
  - Session continuity
  - Auto-approval mode
  - Advanced tool integration

### 3. **Codex CLI** (`codex`)
- **Provider**: OpenAI
- **Type**: CLI Tool
- **Models**: GPT-5, GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **Installation**: `npm install -g @openai/codex`
- **Features**:
  - Auto-approval for commands
  - Message buffering
  - Tool result handling
  - Session management

### 4. **Qwen CLI** (`qwen`)
- **Provider**: Alibaba Qwen
- **Type**: CLI Tool via ACP
- **Models**: Qwen3 Coder Plus, Qwen Coder
- **Installation**: `npm install -g @qwen-code/qwen-code`
- **Features**:
  - ACP (Agent Communication Protocol)
  - Real-time streaming
  - Tool usage support
  - Session management

### 5. **Gemini CLI** (`gemini`)
- **Provider**: Google
- **Type**: CLI Tool via ACP
- **Models**: Gemini 2.5 Pro, Gemini 2.5 Flash
- **Installation**: `npm install -g @google/gemini-cli`
- **Features**:
  - ACP integration
  - Multi-modal support
  - Tool usage
  - Session management

## 🚀 Quick Setup

### Install All Agents
```bash
npm run install:agents
```

### Configure Agents
```bash
npm run configure:agents
```

### Test All Agents
```bash
npm run check:agents
```

## 🔧 Manual Installation

### Claude Code CLI
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

### Cursor Agent CLI
```bash
curl https://cursor.com/install -fsS | bash
export PATH="$HOME/.local/bin:$PATH"
cursor-agent login
```

### Codex CLI
```bash
npm install -g @openai/codex
```

### Qwen CLI
```bash
npm install -g @qwen-code/qwen-code
```

### Gemini CLI
```bash
npm install -g @google/gemini-cli
```

## 🔑 API Key Configuration

All agents require API keys to be configured in the application settings:

1. **Anthropic**: Get from [console.anthropic.com](https://console.anthropic.com/)
2. **OpenAI**: Get from [platform.openai.com](https://platform.openai.com/api-keys)
3. **Google**: Get from [aistudio.google.com](https://aistudio.google.com/app/apikey)
4. **Qwen**: Get from [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/apiKey)

## 🛠️ Development

### Agent Architecture
- **BaseCLI**: Abstract base class for all agents
- **UnifiedCLIManager**: Orchestrates agent execution
- **Model Mapping**: Unified model name translation
- **Session Management**: Persistent session handling

### Adding New Agents
1. Create new adapter in `apps/api/app/services/cli/adapters/`
2. Extend `BaseCLI` class
3. Implement required methods:
   - `check_availability()`
   - `execute_with_streaming()`
   - `get_session_id()`
   - `set_session_id()`
4. Add to `UnifiedCLIManager`
5. Update model mapping in `base.py`

## 🧪 Testing

### Test Individual Agent
```bash
python3 -c "
import asyncio
from apps.api.app.services.cli.adapters import ClaudeCodeCLI
async def test():
    agent = ClaudeCodeCLI()
    status = await agent.check_availability()
    print(status)
asyncio.run(test())
"
```

### Test All Agents
```bash
python3 scripts/check_agents.py
```

## 🚀 Production Deployment

### Render Deployment
The application is configured for automatic deployment on Render with:
- All agents pre-installed
- Database initialization
- Environment variable configuration
- Health checks

### Environment Variables
```bash
ENCRYPTION_KEY=generated_automatically
DATABASE_URL=sqlite:///data/cc.db
ENVIRONMENT=production
RENDER=true
```

## 📊 Agent Status

| Agent | Status | Models | Features |
|-------|--------|--------|----------|
| Claude Code | ✅ Working | 4 models | SDK, Streaming, Tools |
| Cursor Agent | ✅ Working | 4 models | Stream-json, Sessions |
| Codex CLI | ✅ Working | 5 models | Auto-approval, Buffering |
| Qwen CLI | ✅ Working | 3 models | ACP, Streaming |
| Gemini CLI | ✅ Working | 2 models | ACP, Multi-modal |

## 🔍 Troubleshooting

### Common Issues

1. **Agent not found**: Ensure PATH includes agent locations
2. **Login required**: Run agent login commands
3. **API key missing**: Configure in application settings
4. **Permission denied**: Use `sudo` for global installations

### Debug Commands
```bash
# Check agent availability
npm run check:agents

# Check database
npm run check:database

# Full system check
npm run check:all

# Reinstall agents
npm run setup:agents
```

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [Cursor Agent Documentation](https://cursor.com/docs)
- [OpenAI Codex Documentation](https://platform.openai.com/docs)
- [Qwen Documentation](https://qwen.readthedocs.io/)
- [Gemini Documentation](https://ai.google.dev/docs)