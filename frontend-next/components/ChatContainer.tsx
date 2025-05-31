'use client'

import React, { useState, useRef, useEffect } from 'react'
import { useChat } from '../contexts/ChatContext'
import ChatHeader from './ChatHeader'
import MessageList from './MessageList'
import ChatInput from './ChatInput'
import SettingsPanel from './SettingsPanel'
import LoadingIndicator from './LoadingIndicator'

export default function ChatContainer() {
  const { state } = useChat()
  const [showSettings, setShowSettings] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [state.messages])

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* 聊天头部 */}
      <ChatHeader onSettingsClick={() => setShowSettings(true)} />
      
      {/* 消息区域 */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-4xl mx-auto space-y-6">
            <MessageList messages={state.messages} />
            
            {/* 加载指示器 */}
            {state.isLoading && <LoadingIndicator />}
            
            {/* 错误提示 */}
            {state.error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      发生错误
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      {state.error}
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>
        
        {/* 输入区域 */}
        <div className="border-t border-gray-200 bg-white">
          <div className="max-w-4xl mx-auto">
            <ChatInput disabled={state.isLoading} />
          </div>
        </div>
      </div>
      
      {/* 设置面板 */}
      <SettingsPanel 
        isOpen={showSettings} 
        onClose={() => setShowSettings(false)} 
      />
    </div>
  )
} 