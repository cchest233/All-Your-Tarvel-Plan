const express = require('express');
const router = express.Router();
const HealthController = require('../controllers/HealthController');

// 健康检查
router.get('/', HealthController.check);

// 详细健康检查
router.get('/detailed', HealthController.detailedCheck);

module.exports = router; 