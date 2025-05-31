const express = require('express');
const router = express.Router();
const ChatController = require('../controllers/ChatController');

// 创建聊天会话
router.post('/session', ChatController.createSession);

// 发送消息
router.post('/message', ChatController.sendMessage);

// 获取对话历史
router.get('/history/:sessionId', ChatController.getHistory);

// 清空对话
router.post('/clear/:sessionId', ChatController.clearConversation);

// 获取活跃会话列表
router.get('/sessions', ChatController.getSessions);

// 导出对话
router.get('/export/:sessionId', ChatController.exportConversation);

// 获取配置
router.get('/config', ChatController.getConfig);

module.exports = router; 