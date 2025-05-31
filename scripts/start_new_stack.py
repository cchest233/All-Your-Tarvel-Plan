#!/usr/bin/env python3
"""
新架构全栈启动脚本
启动 Python LLM服务 + Node.js后端 + Next.js前端
"""

import os
import sys
import subprocess
import signal
import time
import psutil
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("🚀 全栈旅行聊天应用")
    print("=" * 50)
    print("🐍 Python LLM服务: http://localhost:5000")
    print("⚡ Node.js后端: http://localhost:3000")
    print("🌐 Next.js前端: http://localhost:3001")
    print("=" * 50)

def check_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except:
        print("❌ Python未安装")
        return False
    
    # 检查Node.js
    try:
        result = subprocess.run(["node", "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except:
        print("❌ Node.js未安装")
        return False
    
    # 检查npm
    try:
        result = subprocess.run(["npm", "--version"], 
                              capture_output=True, text=True)
        print(f"✅ npm: {result.stdout.strip()}")
    except:
        print("❌ npm未安装")
        return False
    
    return True

def install_dependencies():
    """安装依赖"""
    print("\n📦 安装依赖...")
    
    # 安装Python依赖
    print("安装Python依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "python-llm/requirements.txt"])
    
    # 安装Node.js依赖
    print("安装Node.js依赖...")
    subprocess.run(["npm", "run", "install:all"])

def start_services():
    """启动所有服务"""
    print("\n🚀 启动服务...")
    
    processes = []
    
    try:
        # 启动Python LLM服务
        print("启动Python LLM服务...")
        llm_process = subprocess.Popen([
            sys.executable, "python-llm/chat_api.py"
        ], cwd="..")
        processes.append(("LLM服务", llm_process))
        time.sleep(2)
        
        # 启动Node.js后端
        print("启动Node.js后端...")
        backend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd="../backend")
        processes.append(("Node.js后端", backend_process))
        time.sleep(2)
        
        # 启动Next.js前端
        print("启动Next.js前端...")
        frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd="../frontend-next")
        processes.append(("Next.js前端", frontend_process))
        
        print("\n✅ 所有服务启动成功!")
        print("按 Ctrl+C 停止所有服务...")
        
        # 等待中断信号
        try:
            while True:
                time.sleep(1)
                # 检查进程是否还在运行
                for name, process in processes:
                    if process.poll() is not None:
                        print(f"⚠️ {name} 意外停止")
        except KeyboardInterrupt:
            print("\n🛑 收到停止信号...")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
    finally:
        # 停止所有进程
        print("停止所有服务...")
        for name, process in processes:
            try:
                if process.poll() is None:
                    print(f"停止 {name}...")
                    process.terminate()
                    process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"强制停止 {name}...")
                process.kill()
            except Exception as e:
                print(f"停止 {name} 时出错: {e}")

def main():
    """主函数"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ 系统要求检查失败，请安装必要的软件")
        sys.exit(1)
    
    # 检查是否需要安装依赖
    install_deps = input("\n是否需要安装/更新依赖? (y/n): ").lower() == 'y'
    if install_deps:
        install_dependencies()
    
    start_services()

if __name__ == "__main__":
    main() 