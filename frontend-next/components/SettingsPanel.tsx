'use client'

import React, { useState } from 'react'
import { useChat } from '../contexts/ChatContext'

interface SettingsPanelProps {
  isOpen: boolean
  onClose: () => void
}

export default function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  const { state, dispatch, createSession } = useChat()
  const [tempConfig, setTempConfig] = useState(state.config)
  const [tempPromptType, setTempPromptType] = useState(state.promptType)

  const handleSave = async () => {
    // 更新配置
    dispatch({ type: 'SET_CONFIG', payload: tempConfig })
    
    // 如果prompt类型改变了，创建新会话
    if (tempPromptType !== state.promptType) {
      await createSession(tempPromptType)
    }
    
    onClose()
  }

  const handleClose = () => {
    // 重置临时配置
    setTempConfig(state.config)
    setTempPromptType(state.promptType)
    onClose()
  }

  if (!isOpen) return null

  return (
    <>
      {/* 背景遮罩 */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={handleClose}
      />
      
      {/* 设置面板 */}
      <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 transform transition-transform">
        <div className="flex flex-col h-full">
          {/* 头部 */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">设置</h3>
            <button
              onClick={handleClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          {/* 内容 */}
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
            {/* AI角色设置 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                AI角色
              </label>
              <select
                value={tempPromptType}
                onChange={(e) => setTempPromptType(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="default">通用助手</option>
                <option value="travel">旅行规划师</option>
                <option value="writing">写作助手</option>
                <option value="code">编程专家</option>
              </select>
              <p className="mt-2 text-sm text-gray-500">
                更改角色将创建新的对话会话
              </p>
            </div>
            
            {/* 温度设置 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                创造性 ({tempConfig.temperature})
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={tempConfig.temperature}
                onChange={(e) => setTempConfig({
                  ...tempConfig,
                  temperature: parseFloat(e.target.value)
                })}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>保守</span>
                <span>平衡</span>
                <span>创造</span>
              </div>
              <p className="mt-2 text-sm text-gray-500">
                较高的值会使输出更随机，较低的值会使其更集中和确定
              </p>
            </div>
            
            {/* 最大Token数设置 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                最大回复长度
              </label>
              <input
                type="number"
                min="100"
                max="4096"
                step="100"
                value={tempConfig.maxTokens}
                onChange={(e) => setTempConfig({
                  ...tempConfig,
                  maxTokens: parseInt(e.target.value)
                })}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <p className="mt-2 text-sm text-gray-500">
                控制AI回复的最大长度（100-4096 tokens）
              </p>
            </div>
          </div>
          
          {/* 底部按钮 */}
          <div className="border-t border-gray-200 px-6 py-4">
            <div className="flex space-x-3">
              <button
                onClick={handleClose}
                className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleSave}
                className="flex-1 px-4 py-2 text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
              >
                保存
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
} 