import React from 'react'
import './globals.css'

export const metadata = {
  title: 'DeepSeek V3 旅行聊天助手',
  description: '智能旅行规划聊天应用',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="font-sans">
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
      </body>
    </html>
  )
} 