"""
高级DeepSeek V3对话链条
支持对话记忆、上下文管理、多轮对话等功能
"""

import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from langchain_core.language_models import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from openai import OpenAI
import json

# 加载环境变量
load_dotenv()


class DeepSeekV3LLM(LLM):
    """DeepSeek V3硅基流动LLM封装 - 高级版本"""
    
    model_name: str = "deepseek-ai/DeepSeek-V3"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    def __init__(self, **kwargs):
        """初始化DeepSeek V3 LLM"""
        super().__init__(**kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "deepseek_v3_advanced"
    
    def _get_api_config(self):
        """获取API配置"""
        api_key = os.environ.get("SILICON_FLOW_API_KEY", "")
        api_url = os.environ.get("SILICON_FLOW_API_URL", "https://api.siliconflow.cn/v1")
        
        if not api_key:
            raise ValueError("请设置SILICON_FLOW_API_KEY环境变量")
        
        return api_key, api_url
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ) -> str:
        """调用DeepSeek V3 API"""
        try:
            api_key, api_url = self._get_api_config()
            
            client = OpenAI(
                api_key=api_key,
                base_url=api_url
            )
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop=stop if stop else None
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def call_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """使用消息列表调用API（支持多轮对话）"""
        try:
            api_key, api_url = self._get_api_config()
            
            client = OpenAI(
                api_key=api_key,
                base_url=api_url
            )
            
            # 应用kwargs中的参数
            temperature = kwargs.get('temperature', self.temperature)
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")


class ConversationManager:
    """对话管理器，处理对话历史和上下文"""
    
    def __init__(self, max_history: int = 10):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.max_history = max_history
        self.session_info: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, session_id: str = None) -> str:
        """创建新的对话会话"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        self.conversations[session_id] = []
        self.session_info[session_id] = {
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'message_count': 0
        }
        
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """添加消息到对话历史"""
        if session_id not in self.conversations:
            self.create_session(session_id)
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.conversations[session_id].append(message)
        
        # 保持历史记录在最大长度内
        if len(self.conversations[session_id]) > self.max_history * 2:  # *2 因为每轮对话有用户和AI两条消息
            self.conversations[session_id] = self.conversations[session_id][-self.max_history * 2:]
        
        # 更新会话信息
        self.session_info[session_id]['last_activity'] = datetime.now().isoformat()
        self.session_info[session_id]['message_count'] += 1
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """获取对话历史（OpenAI API格式）"""
        if session_id not in self.conversations:
            return []
        
        return [
            {'role': msg['role'], 'content': msg['content']}
            for msg in self.conversations[session_id]
        ]
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """获取会话信息"""
        return self.session_info.get(session_id, {})
    
    def clear_session(self, session_id: str):
        """清空会话"""
        if session_id in self.conversations:
            self.conversations[session_id] = []
            self.session_info[session_id]['message_count'] = 0
    
    def delete_session(self, session_id: str):
        """删除会话"""
        if session_id in self.conversations:
            del self.conversations[session_id]
        if session_id in self.session_info:
            del self.session_info[session_id]


class AdvancedDeepSeekChain:
    """高级DeepSeek对话链条"""
    
    def __init__(self, max_history: int = 10):
        self.llm = DeepSeekV3LLM()
        self.conversation_manager = ConversationManager(max_history)
        self.system_prompts = {
            'default': "你是DeepSeek V3智能助手，一个友好、专业且乐于助人的AI。请用中文回答问题。",
            'travel': "你是一个专业的旅行规划师，擅长制定详细的旅行计划、推荐景点和提供旅行建议。",
            'writing': "你是一个专业的写作助手，擅长协助用户进行各种类型的写作，包括文章、报告、创意写作等。",
            'code': "你是一个编程专家，擅长多种编程语言，能够帮助用户解决编程问题、编写代码、解释算法等。"
        }
    
    def create_session(self, system_prompt_type: str = 'default') -> str:
        """创建新的对话会话"""
        session_id = self.conversation_manager.create_session()
        
        # 添加系统提示
        system_prompt = self.system_prompts.get(system_prompt_type, self.system_prompts['default'])
        self.conversation_manager.add_message(
            session_id, 
            'system', 
            system_prompt,
            {'prompt_type': system_prompt_type}
        )
        
        return session_id
    
    def chat(self, session_id: str, user_message: str, **kwargs) -> Dict[str, Any]:
        """进行对话"""
        try:
            # 检查会话是否存在
            if session_id not in self.conversation_manager.conversations:
                session_id = self.create_session()
            
            # 添加用户消息
            self.conversation_manager.add_message(session_id, 'user', user_message)
            
            # 获取对话历史
            messages = self.conversation_manager.get_conversation_history(session_id)
            
            # 调用LLM
            start_time = datetime.now()
            ai_response = self.llm.call_with_messages(messages, **kwargs)
            end_time = datetime.now()
            
            # 添加AI响应
            self.conversation_manager.add_message(
                session_id, 
                'assistant', 
                ai_response,
                {
                    'response_time': (end_time - start_time).total_seconds(),
                    'model_params': kwargs
                }
            )
            
            return {
                'success': True,
                'session_id': session_id,
                'response': ai_response,
                'message_count': len(messages) + 1,
                'response_time': (end_time - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """获取对话摘要"""
        if session_id not in self.conversation_manager.conversations:
            return {'error': '会话不存在'}
        
        history = self.conversation_manager.conversations[session_id]
        session_info = self.conversation_manager.get_session_info(session_id)
        
        user_messages = [msg for msg in history if msg['role'] == 'user']
        ai_messages = [msg for msg in history if msg['role'] == 'assistant']
        
        return {
            'session_id': session_id,
            'created_at': session_info.get('created_at'),
            'last_activity': session_info.get('last_activity'),
            'total_messages': len(history),
            'user_messages': len(user_messages),
            'ai_messages': len(ai_messages),
            'conversation_preview': history[-2:] if len(history) >= 2 else history
        }
    
    def clear_conversation(self, session_id: str) -> Dict[str, Any]:
        """清空对话"""
        try:
            self.conversation_manager.clear_session(session_id)
            return {'success': True, 'message': '对话已清空'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def export_conversation(self, session_id: str) -> Dict[str, Any]:
        """导出对话记录"""
        if session_id not in self.conversation_manager.conversations:
            return {'error': '会话不存在'}
        
        history = self.conversation_manager.conversations[session_id]
        session_info = self.conversation_manager.get_session_info(session_id)
        
        return {
            'session_info': session_info,
            'conversation': history,
            'export_time': datetime.now().isoformat()
        }


def main():
    """测试高级对话链条"""
    print("🚀 高级DeepSeek V3对话链条测试")
    print("=" * 50)
    
    # 创建链条实例
    chain = AdvancedDeepSeekChain(max_history=5)
    
    # 创建会话
    session_id = chain.create_session('travel')
    print(f"✅ 创建会话: {session_id}")
    
    # 测试对话
    test_messages = [
        "你好，我想规划一个北京3天游",
        "我比较喜欢历史文化景点",
        "预算大概3000元，有什么建议吗？"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- 第{i}轮对话 ---")
        print(f"用户: {message}")
        
        result = chain.chat(session_id, message, temperature=0.7)
        
        if result['success']:
            print(f"AI: {result['response'][:200]}...")
            print(f"响应时间: {result['response_time']:.2f}秒")
        else:
            print(f"错误: {result['error']}")
    
    # 获取对话摘要
    print(f"\n--- 对话摘要 ---")
    summary = chain.get_conversation_summary(session_id)
    print(f"总消息数: {summary['total_messages']}")
    print(f"用户消息: {summary['user_messages']}")
    print(f"AI消息: {summary['ai_messages']}")
    
    print("\n✅ 测试完成！")


if __name__ == "__main__":
    main() 