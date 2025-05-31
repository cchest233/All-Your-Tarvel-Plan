const axios = require('axios');
const logger = require('../utils/logger');

const LLM_SERVICE_URL = process.env.LLM_SERVICE_URL || 'http://localhost:5000';

class HealthController {
  /**
   * 基础健康检查
   */
  static async check(req, res) {
    res.json({
      status: 'healthy',
      service: 'Travel Chat Backend',
      timestamp: new Date().toISOString(),
      version: '1.0.0'
    });
  }

  /**
   * 详细健康检查
   */
  static async detailedCheck(req, res) {
    const healthData = {
      status: 'healthy',
      service: 'Travel Chat Backend',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      services: {
        llm: 'unknown'
      }
    };

    try {
      // 检查LLM服务状态
      const llmResponse = await axios.get(`${LLM_SERVICE_URL}/api/health`, {
        timeout: 5000
      });
      
      if (llmResponse.status === 200) {
        healthData.services.llm = 'healthy';
      } else {
        healthData.services.llm = 'unhealthy';
      }
    } catch (error) {
      logger.warn(`LLM服务健康检查失败: ${error.message}`);
      healthData.services.llm = 'unhealthy';
    }

    // 如果有关键服务不健康，则整体状态为不健康
    if (healthData.services.llm === 'unhealthy') {
      healthData.status = 'degraded';
    }

    const statusCode = healthData.status === 'healthy' ? 200 : 503;
    res.status(statusCode).json(healthData);
  }
}

module.exports = HealthController; 