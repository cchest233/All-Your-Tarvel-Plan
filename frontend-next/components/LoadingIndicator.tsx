'use client'

import React from 'react'

export default function LoadingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="flex max-w-2xl space-x-3">
        {/* AI头像 */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
          <svg className="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
            <path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V9a1 1 0 00-1-1h-1v-1z" />
          </svg>
        </div>
        
        {/* 加载动画 */}
        <div className="bg-white border border-gray-200 rounded-lg px-4 py-3">
          <div className="flex items-center space-x-1">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.4s' }}></div>
            </div>
            <span className="text-sm text-gray-500 ml-2">AI正在思考中...</span>
          </div>
        </div>
      </div>
    </div>
  )
} 