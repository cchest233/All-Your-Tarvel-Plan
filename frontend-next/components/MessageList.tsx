'use client'

import React from 'react'
import { Message } from '../contexts/ChatContext'
import MessageItem from './MessageItem'

interface MessageListProps {
  messages: Message[]
}

export default function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.959 8.959 0 01-4.906-1.435l-3.815 1.275a.75.75 0 01-.921-.921l1.275-3.815A8.959 8.959 0 013 12c0-4.418 3.582-8 8-8s8 3.582 8 8z" />
          </svg>
        </div>
        <p className="text-gray-500 text-lg">开始对话</p>
        <p className="text-gray-400 text-sm mt-2">发送消息开始与AI助手聊天</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {messages.map((message) => (
        <MessageItem 
          key={message.id} 
          message={message} 
        />
      ))}
    </div>
  )
} 