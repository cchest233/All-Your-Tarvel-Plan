const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const logger = require('./utils/logger');
const chatRoutes = require('./routes/chat');
const healthRoutes = require('./routes/health');
const errorHandler = require('./middleware/errorHandler');

const app = express();
const PORT = process.env.NODE_PORT || 3000;

// 中间件配置
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3001',
  credentials: true
}));

// 限流配置
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 每个IP最多100个请求
  message: {
    error: '请求过于频繁，请稍后再试'
  }
});
app.use(limiter);

// 日志中间件
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }));

// 解析JSON
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// 路由
app.use('/api/health', healthRoutes);
app.use('/api/chat', chatRoutes);

// 404处理
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    error: '接口不存在'
  });
});

// 错误处理中间件
app.use(errorHandler);

// 启动服务器
app.listen(PORT, () => {
  logger.info(`🚀 Node.js 后端服务启动成功`);
  logger.info(`📡 服务地址: http://localhost:${PORT}`);
  logger.info(`🔗 LLM服务地址: ${process.env.LLM_SERVICE_URL || 'http://localhost:5000'}`);
});

// 优雅关闭
process.on('SIGTERM', () => {
  logger.info('收到 SIGTERM 信号，准备关闭服务器...');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('收到 SIGINT 信号，准备关闭服务器...');
  process.exit(0);
});

module.exports = app; 