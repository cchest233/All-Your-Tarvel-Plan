const logger = require('../utils/logger');

function errorHandler(err, req, res, next) {
  logger.error(`错误: ${err.message}`, {
    stack: err.stack,
    url: req.url,
    method: req.method,
    body: req.body
  });

  // 默认错误响应
  let error = {
    success: false,
    error: '服务器内部错误'
  };

  // 根据错误类型自定义响应
  if (err.name === 'ValidationError') {
    error.error = '请求参数验证失败';
    return res.status(400).json(error);
  }

  if (err.name === 'UnauthorizedError') {
    error.error = '未授权访问';
    return res.status(401).json(error);
  }

  if (err.code === 'ECONNREFUSED') {
    error.error = 'LLM服务暂时不可用';
    return res.status(503).json(error);
  }

  // 生产环境下不暴露具体错误信息
  if (process.env.NODE_ENV === 'production') {
    error.error = '服务器内部错误';
  } else {
    error.error = err.message;
    error.stack = err.stack;
  }

  res.status(500).json(error);
}

module.exports = errorHandler; 