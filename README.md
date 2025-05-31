# 🚀 全栈旅行聊天应用

基于 **DeepSeek V3** 的现代化全栈聊天应用，采用微服务架构。

## 🎯 快速开始

```bash
# 1. 配置API密钥
echo "DEEPSEEK_API_KEY=your_api_key" > .env

# 2. 启动应用
python scripts/start_new_stack.py

# 3. 访问应用
# http://localhost:3001
```

## 🏗️ 技术架构

```
🐍 Python (5000端口) ←→ ⚡ Node.js (3000端口) ←→ 🌐 Next.js (3001端口)
   DeepSeek V3核心         Express中间层          React前端界面
```

## 📁 项目结构

```
项目根目录/
├── 🐍 python-llm/             # Python LLM服务
├── ⚡ backend/                # Node.js Express后端
├── 🌐 frontend-next/          # Next.js React前端
├── 📚 docs/                  # 详细文档
├── 🔧 scripts/               # 启动脚本
├── 🐳 docker-compose.yml     # Docker部署
└── 📄 package.json           # 根工作空间
```

## 📚 文档

- **[详细说明](docs/README.md)** - 完整项目文档
- **[快速启动](docs/QUICK_START.md)** - 详细启动指南
- **[架构设计](.cursor/rules/architecture.mdc)** - 技术架构文档

## 🛠️ 开发环境

- Node.js >= 18.0.0  
- Python >= 3.8
- DeepSeek API密钥

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**⭐ 给个星标支持项目发展！** 