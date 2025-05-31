const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const logger = require('../utils/logger');

const LLM_SERVICE_URL = process.env.LLM_SERVICE_URL || 'http://localhost:5000';

// 内存存储活跃会话（生产环境应使用Redis）
const activeSessions = new Map();

class ChatController {
  /**
   * 创建新的聊天会话
   */
  static async createSession(req, res) {
    try {
      const { prompt_type = 'default' } = req.body;
      
      // 调用Python LLM服务创建会话
      const response = await axios.post(`${LLM_SERVICE_URL}/api/chat/session`, {
        prompt_type
      });

      if (response.data.success) {
        const sessionData = {
          id: response.data.session_id,
          prompt_type,
          created_at: new Date().toISOString(),
          last_activity: new Date().toISOString()
        };
        
        activeSessions.set(response.data.session_id, sessionData);
        
        logger.info(`创建新会话: ${response.data.session_id}, 类型: ${prompt_type}`);
        
        res.json({
          success: true,
          session_id: response.data.session_id,
          prompt_type,
          message: '会话创建成功'
        });
      } else {
        throw new Error(response.data.error || '创建会话失败');
      }
    } catch (error) {
      logger.error(`创建会话失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '创建会话失败'
      });
    }
  }

  /**
   * 发送消息
   */
  static async sendMessage(req, res) {
    try {
      const { session_id, message, temperature = 0.7, max_tokens = 2048 } = req.body;

      if (!message || !message.trim()) {
        return res.status(400).json({
          success: false,
          error: '消息内容不能为空'
        });
      }

      // 更新会话活动时间
      if (activeSessions.has(session_id)) {
        const sessionData = activeSessions.get(session_id);
        sessionData.last_activity = new Date().toISOString();
        activeSessions.set(session_id, sessionData);
      }

      logger.info(`会话 ${session_id} 收到消息: ${message.substring(0, 50)}...`);

      // 转发到Python LLM服务
      const response = await axios.post(`${LLM_SERVICE_URL}/api/chat/message`, {
        session_id,
        message,
        temperature,
        max_tokens
      });

      if (response.data.success) {
        logger.info(`会话 ${session_id} 响应成功，用时: ${response.data.response_time}秒`);
        res.json(response.data);
      } else {
        throw new Error(response.data.error || '发送消息失败');
      }
    } catch (error) {
      logger.error(`发送消息失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '发送消息失败'
      });
    }
  }

  /**
   * 获取对话历史
   */
  static async getHistory(req, res) {
    try {
      const { sessionId } = req.params;
      
      const response = await axios.get(`${LLM_SERVICE_URL}/api/chat/history/${sessionId}`);
      
      res.json(response.data);
    } catch (error) {
      logger.error(`获取对话历史失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '获取对话历史失败'
      });
    }
  }

  /**
   * 清空对话
   */
  static async clearConversation(req, res) {
    try {
      const { sessionId } = req.params;
      
      const response = await axios.post(`${LLM_SERVICE_URL}/api/chat/clear/${sessionId}`);
      
      logger.info(`清空会话: ${sessionId}`);
      res.json(response.data);
    } catch (error) {
      logger.error(`清空对话失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '清空对话失败'
      });
    }
  }

  /**
   * 获取活跃会话列表
   */
  static async getSessions(req, res) {
    try {
      const sessions = Array.from(activeSessions.values()).map(session => ({
        id: session.id,
        prompt_type: session.prompt_type,
        created_at: session.created_at,
        last_activity: session.last_activity
      }));

      res.json({
        success: true,
        sessions,
        total: sessions.length
      });
    } catch (error) {
      logger.error(`获取会话列表失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '获取会话列表失败'
      });
    }
  }

  /**
   * 导出对话
   */
  static async exportConversation(req, res) {
    try {
      const { sessionId } = req.params;
      
      const response = await axios.get(`${LLM_SERVICE_URL}/api/chat/export/${sessionId}`);
      
      res.json(response.data);
    } catch (error) {
      logger.error(`导出对话失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '导出对话失败'
      });
    }
  }

  /**
   * 获取配置
   */
  static async getConfig(req, res) {
    try {
      const response = await axios.get(`${LLM_SERVICE_URL}/api/config`);
      
      res.json(response.data);
    } catch (error) {
      logger.error(`获取配置失败: ${error.message}`);
      res.status(500).json({
        success: false,
        error: error.message || '获取配置失败'
      });
    }
  }
}

module.exports = ChatController; 