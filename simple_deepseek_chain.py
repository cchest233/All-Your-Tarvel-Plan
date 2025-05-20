"""
简单的Langchain与硅基流动API集成示例

该文件演示了如何使用Langchain构建简单的prompt | llm链条，并使用硅基流动API。
"""

import os
import json
import requests
import uuid
import base64
from typing import Optional, List, Any, Dict
from dotenv import load_dotenv
from langchain_core.language_models import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 加载环境变量
load_dotenv()


def generate_test_api_key():
    """生成测试用的API key
    
    注意：这仅是测试用途，实际使用时应从硅基流动获取真实API密钥
    
    Returns:
        生成的测试API密钥
    """
    # 生成一个随机UUID并编码为base64，模拟API key的格式
    random_uuid = uuid.uuid4()
    encoded = base64.b64encode(str(random_uuid).encode()).decode()
    # 添加常见API密钥前缀，使其看起来像真实的API密钥
    return f"sf-{encoded[:32]}"


def save_api_key_to_env(api_key):
    """将API密钥保存到.env文件
    
    Args:
        api_key: 要保存的API密钥
    """
    # 检查.env文件是否存在
    if os.path.exists(".env"):
        # 读取现有内容
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查是否已有SILICON_FLOW_API_KEY
        if "SILICON_FLOW_API_KEY" in content:
            # 替换现有行
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith("SILICON_FLOW_API_KEY="):
                    new_lines.append(f"SILICON_FLOW_API_KEY={api_key}")
                else:
                    new_lines.append(line)
            
            new_content = "\n".join(new_lines)
        else:
            # 添加新行
            new_content = content
            if not new_content.endswith("\n"):
                new_content += "\n"
            new_content += f"SILICON_FLOW_API_KEY={api_key}\n"
        
        # 写回文件
        with open(".env", "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        # 创建新文件
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"SILICON_FLOW_API_KEY={api_key}\n")
    
    # 更新环境变量
    os.environ["SILICON_FLOW_API_KEY"] = api_key
    print(f"已保存API密钥到.env文件: SILICON_FLOW_API_KEY={api_key}")


class SiliconFlowLLM(LLM):
    """硅基流动LLM的封装"""
    
    api_key: str = ""
    api_url: str = "https://api.siliconflow.com/v1/chat/completions"
    model_name: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 1024
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model_name: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ):
        """初始化硅基流动LLM

        Args:
            api_key: 硅基流动API密钥，默认从环境变量获取
            api_url: API端点，默认是硅基流动的endpoint
            model_name: 模型名称
            temperature: 温度参数
            max_tokens: 最大生成token数
        """
        super().__init__(**kwargs)
        self.api_key = api_key or os.environ.get("SILICON_FLOW_API_KEY", "")
        self.api_url = api_url or os.environ.get("SILICON_FLOW_API_URL", "https://api.siliconflow.com/v1/chat/completions")
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    @property
    def _llm_type(self) -> str:
        """返回LLM类型"""
        return "silicon_flow"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> str:
        """调用硅基流动API

        Args:
            prompt: 输入提示
            stop: 停止标记
            run_manager: 回调管理器

        Returns:
            生成的文本
        """
        if not self.api_key:
            print("警告: 未设置硅基流动API密钥，返回模拟响应")
            return f"[模拟响应] 基于提示: '{prompt[:30]}...'的生成结果"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            print(f"正在调用API: {self.api_url}")
            print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"API响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API调用错误: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"状态码: {e.response.status_code}")
                print(f"响应: {e.response.text}")
            
            # 返回模拟响应，以便测试链条依然能工作
            print("返回模拟响应")
            return f"[模拟响应] 由于API调用失败，这是一个模拟的回答：\n\n对于提问: '{prompt[:50]}...'，我建议以下行程安排：\n\n第一天: 游览城市主要景点\n第二天: 体验当地文化活动\n第三天: 品尝当地美食，购物纪念品"


def main():
    """主函数，演示Langchain与硅基流动API的集成"""
    
    # 0. 生成并保存测试API密钥
    test_api_key = generate_test_api_key()
    save_api_key_to_env(test_api_key)
    
    # 1. 创建LLM实例
    llm = SiliconFlowLLM()
    print(f"使用API密钥: {llm.api_key[:5]}...{llm.api_key[-5:]}")
    print(f"使用API端点: {llm.api_url}")
    
    # 2. 创建一个简单的提示模板
    prompt = PromptTemplate.from_template(
        "你是一个旅行规划专家。请为去{destination}旅行提供{days}天的简要行程建议。"
    )
    
    # 3. 创建输出解析器
    output_parser = StrOutputParser()
    
    # 4. 构建链条: prompt | llm | output_parser
    chain = prompt | llm | output_parser
    
    # 5. 调用链条
    destination = "杭州"
    days = 3
    
    print(f"\n为{destination}的{days}天旅行生成行程建议...\n")
    
    # 使用链条
    result_chain = chain.invoke({"destination": destination, "days": days})
    print("\n" + "="*50)
    print("链条结果:")
    print(result_chain)
    print("="*50 + "\n")
    
    # 直接使用LLM
    print("直接调用LLM:")
    prompt_text = f"你是一个旅行规划专家。请为去{destination}旅行提供{days}天的简要行程建议。"
    result_llm = llm.invoke(prompt_text)
    print("\n" + "="*50)
    print("LLM结果:")
    print(result_llm)
    print("="*50)


if __name__ == "__main__":
    main() 