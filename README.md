# All-Your-Travel-Plan

一个AI驱动的旅行规划应用，根据用户偏好生成个性化旅行行程。利用检索增强生成（RAG）技术，系统结合来自小红书和Google地图的数据，创建详细的旅行计划。

## 主要功能

- **个性化行程**: 根据旅行时长、偏好和兴趣创建自定义旅行计划
- **AI驱动推荐**: 利用DeepSeek API和RAG生成上下文感知的建议
- **多源数据**: 结合小红书和Google地图的信息提供全面的推荐
- **日程规划**: 获取优化的日程安排，包括景点、餐厅和活动

使用Python (Flask/Django)作为后端，向量数据库进行高效数据检索，并提供响应式Web界面。未来开发计划包括支持Google Chrome扩展以提供增强的可访问性。

## 项目结构

```
travel-plan-app/
├── app/                    # 应用包
│   ├── __init__.py          # 应用初始化
│   ├── api/                 # API模块
│   │   ├── __init__.py        # API模块初始化
│   │   └── routes.py          # API路由定义
│   ├── chains/              # Langchain处理链
│   │   ├── __init__.py        # Chains模块初始化
│   │   └── travel_planner.py  # 旅行规划Chain
│   ├── llm/                 # LLM集成
│   │   ├── __init__.py        # LLM模块初始化
│   │   └── deepseek.py        # DeepSeek LLM集成
│   └── mcp/                 # 小红书MCP协议集成
│       ├── __init__.py        # MCP模块初始化
│       └── client.py          # MCP客户端实现
├── config.example.py        # 配置示例
├── requirements.txt         # 依赖列表
└── run.py                   # 应用启动脚本
```

## 安装与设置

1. 克隆仓库:
   ```bash
   git clone https://github.com/your-username/All-Your-Travel-Plan.git
   cd All-Your-Travel-Plan
   ```

2. 创建虚拟环境:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境:
   - 复制 `config.example.py` 为 `config.py`
   - 设置 DeepSeek API 密钥等必要配置

5. 运行应用:
   ```bash
   python run.py
   ```

## API使用

### 创建旅行计划

**POST** `/api/v1/travel-plan`

请求体:
```json
{
  "location": "杭州",
  "duration": 3,
  "preferences": "喜欢文化景点，对美食感兴趣，较少购物"
}
```

### 获取景点信息

**GET** `/api/v1/attractions?location=杭州&categories=文化,自然&limit=5`

### 获取餐厅信息

**GET** `/api/v1/restaurants?location=杭州&cuisine_types=浙菜,川菜&limit=5`

## 技术栈

- **后端**: Flask, Langchain
- **LLM**: DeepSeek API
- **数据源**: 小红书MCP协议 (准备集成)

