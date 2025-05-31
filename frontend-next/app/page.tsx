'use client'

import { useState, useEffect, useRef } from 'react'
import ChatContainer from '../components/ChatContainer'
import { ChatProvider } from '../contexts/ChatContext'

export default function Home() {
  return (
    <ChatProvider>
      <main className="h-screen flex flex-col">
        <ChatContainer />
      </main>
    </ChatProvider>
  )
} 