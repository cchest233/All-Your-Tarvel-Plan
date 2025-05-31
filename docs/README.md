# 🚀 全栈旅行聊天应用

基于 **DeepSeek V3** 的现代化全栈聊天应用，采用微服务架构，支持多角色AI助手。

## ✨ 功能特性

🤖 **智能对话** - DeepSeek V3 驱动的高质量AI对话  
🎭 **多角色切换** - 旅行规划师、写作助手、编程专家等  
💬 **实时聊天** - 现代化聊天界面，支持Markdown渲染  
⚙️ **参数调节** - 可调节AI创造性和回复长度  
📱 **响应式设计** - 完美适配桌面和移动设备  
🔄 **会话管理** - 支持会话历史、清空对话等功能  

## 🏗️ 技术架构

```
🐍 Python (5000端口) ←→ ⚡ Node.js (3000端口) ←→ 🌐 Next.js (3001端口)
   DeepSeek V3核心         Express中间层          React前端界面
```

- **后端**: Python Flask + DeepSeek V3 API
- **中间层**: Node.js Express + TypeScript 
- **前端**: Next.js + React + TailwindCSS
- **状态管理**: React Context + TypeScript
- **样式**: TailwindCSS + 响应式设计

## 🚀 快速开始

### 前置要求
- Node.js >= 18.0.0
- Python >= 3.8
- DeepSeek API密钥

### 1. 克隆项目
```bash
git clone <repository-url>
cd All-Your-Tarvel-Plan
```

### 2. 配置环境变量
创建 `.env` 文件：
```env
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 3. 启动应用
```bash
# 方式1: 一键启动（推荐）
python start_new_stack.py

# 方式2: 手动启动（开发模式）
# 终端1: Python服务
python chat_api.py

# 终端2: Node.js后端  
cd backend && npm run dev

# 终端3: Next.js前端
cd frontend-next && npm run dev
```

### 4. 访问应用
打开浏览器访问: **http://localhost:3001**

## 📁 项目结构

```
项目根目录/
├── 🐍 Python LLM服务
│   ├── chat_api.py                 # Flask API服务器
│   ├── advanced_deepseek_chain.py  # DeepSeek V3聊天链
│   └── requirements.txt            # Python依赖
│
├── ⚡ Node.js后端 (backend/)
│   ├── src/
│   │   ├── server.js               # Express服务器
│   │   ├── controllers/            # API控制器
│   │   ├── routes/                 # 路由定义
│   │   └── middleware/             # 中间件
│   └── package.json                # Node.js依赖
│
├── 🌐 Next.js前端 (frontend-next/)
│   ├── app/                        # App Router页面
│   ├── components/                 # React组件
│   │   ├── ChatContainer.tsx       # 主聊天容器
│   │   ├── MessageList.tsx         # 消息列表
│   │   ├── ChatInput.tsx           # 输入框
│   │   └── SettingsPanel.tsx       # 设置面板
│   ├── contexts/
│   │   └── ChatContext.tsx         # 全局状态管理
│   └── package.json                # React依赖
│
└── 🔧 配置文件
    ├── start_new_stack.py          # 全栈启动脚本
    ├── docker-compose.yml          # Docker配置
    └── QUICK_START.md              # 详细启动指南
```

## 🎯 使用指南

### 基本对话
1. 打开 http://localhost:3001
2. 在输入框中输入您的问题
3. 按回车或点击发送按钮
4. AI将为您提供智能回复

### 切换AI角色
1. 点击右上角设置按钮
2. 在"AI角色"下拉菜单中选择：
   - **通用助手** - 全能AI助手
   - **旅行规划师** - 专业旅行规划
   - **写作助手** - 文案写作支持
   - **编程专家** - 技术问题解答

### 调节AI参数
- **创造性控制** - 滑动条调节AI回复的随机性
- **回复长度** - 设置AI回复的最大长度

## 🌐 API文档

### Python LLM API (端口5000)
```
GET  /api/health              # 健康检查
POST /api/chat/session        # 创建会话
POST /api/chat/message        # 发送消息
GET  /api/chat/history/<id>   # 获取历史
POST /api/chat/clear/<id>     # 清空对话
```

### Node.js中间层 (端口3000)
```
GET  /api/health              # 健康检查
POST /api/chat/*              # 代理到Python服务
```

## 🔧 开发指南

### 添加新功能
1. **前端组件**: 在 `frontend-next/components/` 中创建
2. **API路由**: 在 `backend/src/routes/` 中定义
3. **Python服务**: 在 `chat_api.py` 中扩展

### 调试技巧
- 查看浏览器开发者工具的网络面板
- 检查各服务的控制台输出
- 使用健康检查端点验证服务状态

## 🐳 Docker部署

```bash
# 构建和启动
docker-compose up --build

# 后台运行
docker-compose up -d
```

## 🛠️ 故障排除

### 常见问题
1. **Node.js命令不识别** - 重启终端或设置环境变量
2. **端口被占用** - 检查并关闭相关进程
3. **API密钥错误** - 确认 `.env` 文件配置正确
4. **依赖安装失败** - 尝试清除缓存重新安装

### 监控端点
- Python服务: http://localhost:5000/api/health
- Node.js服务: http://localhost:3000/api/health  
- 前端应用: http://localhost:3001

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

---

**⭐ 如果这个项目对您有帮助，请考虑给个星标！** 