"""
DeepSeek V3 聊天API服务
提供RESTful接口，支持前端交互
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from advanced_deepseek_chain import AdvancedDeepSeekChain
import logging
from datetime import datetime
import traceback

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局对话链条实例
chat_chain = AdvancedDeepSeekChain(max_history=20)

# 存储活跃会话
active_sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'DeepSeek V3 Chat API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/chat/session', methods=['POST'])
def create_session():
    """创建新的聊天会话"""
    try:
        data = request.get_json() or {}
        prompt_type = data.get('prompt_type', 'default')
        
        session_id = chat_chain.create_session(prompt_type)
        active_sessions[session_id] = {
            'created_at': datetime.now().isoformat(),
            'prompt_type': prompt_type
        }
        
        logger.info(f"创建新会话: {session_id}, 类型: {prompt_type}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'prompt_type': prompt_type,
            'message': '会话创建成功'
        })
        
    except Exception as e:
        logger.error(f"创建会话失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/message', methods=['POST'])
def send_message():
    """发送消息并获取回复"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请求数据为空'
            }), 400
        
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': '消息内容不能为空'
            }), 400
        
        # 如果没有会话ID，创建新会话
        if not session_id or session_id not in active_sessions:
            session_id = chat_chain.create_session()
            active_sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'prompt_type': 'default'
            }
        
        # 获取可选参数
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2048)
        
        logger.info(f"会话 {session_id} 收到消息: {message[:50]}...")
        
        # 调用对话链条
        result = chat_chain.chat(
            session_id, 
            message, 
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if result['success']:
            logger.info(f"会话 {session_id} 响应成功，用时: {result['response_time']:.2f}秒")
            return jsonify({
                'success': True,
                'session_id': session_id,
                'response': result['response'],
                'message_count': result['message_count'],
                'response_time': result['response_time']
            })
        else:
            logger.error(f"会话 {session_id} 响应失败: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error'],
                'session_id': session_id
            }), 500
            
    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_conversation_history(session_id):
    """获取对话历史"""
    try:
        summary = chat_chain.get_conversation_summary(session_id)
        
        if 'error' in summary:
            return jsonify({
                'success': False,
                'error': summary['error']
            }), 404
        
        # 获取完整历史
        history = chat_chain.conversation_manager.conversations.get(session_id, [])
        
        # 过滤掉系统消息，只返回用户和AI的对话
        filtered_history = [
            {
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': msg['timestamp']
            }
            for msg in history
            if msg['role'] in ['user', 'assistant']
        ]
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'summary': summary,
            'history': filtered_history
        })
        
    except Exception as e:
        logger.error(f"获取对话历史失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/clear/<session_id>', methods=['POST'])
def clear_conversation(session_id):
    """清空对话"""
    try:
        result = chat_chain.clear_conversation(session_id)
        
        if result['success']:
            logger.info(f"清空会话: {session_id}")
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"清空对话失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/sessions', methods=['GET'])
def list_sessions():
    """列出所有活跃会话"""
    try:
        sessions = []
        for session_id, info in active_sessions.items():
            summary = chat_chain.get_conversation_summary(session_id)
            if 'error' not in summary:
                sessions.append({
                    'session_id': session_id,
                    'created_at': info['created_at'],
                    'prompt_type': info['prompt_type'],
                    'message_count': summary.get('total_messages', 0),
                    'last_activity': summary.get('last_activity')
                })
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'total_sessions': len(sessions)
        })
        
    except Exception as e:
        logger.error(f"列出会话失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat/export/<session_id>', methods=['GET'])
def export_conversation(session_id):
    """导出对话记录"""
    try:
        result = chat_chain.export_conversation(session_id)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"导出对话失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置信息"""
    return jsonify({
        'success': True,
        'config': {
            'max_history': chat_chain.conversation_manager.max_history,
            'available_prompts': list(chat_chain.system_prompts.keys()),
            'model': 'deepseek-ai/DeepSeek-V3',
            'api_url': os.environ.get('SILICON_FLOW_API_URL', 'https://api.siliconflow.cn/v1')
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'API端点不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 检查环境变量
    api_key = os.environ.get("SILICON_FLOW_API_KEY")
    if not api_key:
        logger.warning("未设置SILICON_FLOW_API_KEY环境变量")
        print("⚠️  警告: 请设置SILICON_FLOW_API_KEY环境变量")
        print("   PowerShell: $env:SILICON_FLOW_API_KEY='your_key'")
    else:
        logger.info(f"API密钥已配置: {api_key[:10]}...{api_key[-5:]}")
    
    print("🚀 DeepSeek V3 聊天API服务启动")
    print("📡 API文档:")
    print("   GET  /api/health              - 健康检查")
    print("   POST /api/chat/session        - 创建会话")
    print("   POST /api/chat/message        - 发送消息")
    print("   GET  /api/chat/history/<id>   - 获取历史")
    print("   POST /api/chat/clear/<id>     - 清空对话")
    print("   GET  /api/chat/sessions       - 列出会话")
    print("   GET  /api/config              - 获取配置")
    print()
    print("🌐 服务地址: http://localhost:5000")
    print("📖 Swagger文档: http://localhost:5000/api/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    ) 