'use client'

import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'
import axios from 'axios'

// 消息类型
export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

// 聊天状态
export interface ChatState {
  sessionId: string | null
  messages: Message[]
  isLoading: boolean
  error: string | null
  promptType: string
  config: {
    temperature: number
    maxTokens: number
  }
}

// Action类型
export type ChatAction =
  | { type: 'SET_SESSION_ID'; payload: string }
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_MESSAGES' }
  | { type: 'SET_PROMPT_TYPE'; payload: string }
  | { type: 'SET_CONFIG'; payload: Partial<ChatState['config']> }

// 初始状态
const initialState: ChatState = {
  sessionId: null,
  messages: [],
  isLoading: false,
  error: null,
  promptType: 'default',
  config: {
    temperature: 0.7,
    maxTokens: 2048
  }
}

// Reducer
function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case 'SET_SESSION_ID':
      return { ...state, sessionId: action.payload }
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] }
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    case 'SET_ERROR':
      return { ...state, error: action.payload }
    case 'CLEAR_MESSAGES':
      return { ...state, messages: [] }
    case 'SET_PROMPT_TYPE':
      return { ...state, promptType: action.payload }
    case 'SET_CONFIG':
      return { ...state, config: { ...state.config, ...action.payload } }
    default:
      return state
  }
}

// Context类型
interface ChatContextType {
  state: ChatState
  dispatch: React.Dispatch<ChatAction>
  sendMessage: (message: string) => Promise<void>
  createSession: (promptType?: string) => Promise<void>
  clearConversation: () => Promise<void>
}

// 创建Context
const ChatContext = createContext<ChatContextType | undefined>(undefined)

// API配置
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3000'

// Provider组件
export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(chatReducer, initialState)

  // 创建会话
  const createSession = async (promptType: string = 'default') => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true })
      dispatch({ type: 'SET_ERROR', payload: null })

      const response = await axios.post(`${API_BASE_URL}/api/chat/session`, {
        prompt_type: promptType
      })

      if (response.data.success) {
        dispatch({ type: 'SET_SESSION_ID', payload: response.data.session_id })
        dispatch({ type: 'SET_PROMPT_TYPE', payload: promptType })
        
        // 添加欢迎消息
        const welcomeMessage: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: getWelcomeMessage(promptType),
          timestamp: new Date().toISOString()
        }
        dispatch({ type: 'ADD_MESSAGE', payload: welcomeMessage })
      } else {
        throw new Error(response.data.error || '创建会话失败')
      }
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || '创建会话失败' })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  // 发送消息
  const sendMessage = async (message: string) => {
    if (!message.trim() || !state.sessionId) return

    try {
      // 添加用户消息
      const userMessage: Message = {
        id: uuidv4(),
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      }
      dispatch({ type: 'ADD_MESSAGE', payload: userMessage })
      dispatch({ type: 'SET_LOADING', payload: true })
      dispatch({ type: 'SET_ERROR', payload: null })

      // 发送到后端
      const response = await axios.post(`${API_BASE_URL}/api/chat/message`, {
        session_id: state.sessionId,
        message,
        temperature: state.config.temperature,
        max_tokens: state.config.maxTokens
      })

      if (response.data.success) {
        // 添加AI回复
        const aiMessage: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString()
        }
        dispatch({ type: 'ADD_MESSAGE', payload: aiMessage })
      } else {
        throw new Error(response.data.error || '发送消息失败')
      }
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || '发送消息失败' })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  // 清空对话
  const clearConversation = async () => {
    if (!state.sessionId) return

    try {
      await axios.post(`${API_BASE_URL}/api/chat/clear/${state.sessionId}`)
      dispatch({ type: 'CLEAR_MESSAGES' })
      
      // 重新添加欢迎消息
      const welcomeMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: getWelcomeMessage(state.promptType),
        timestamp: new Date().toISOString()
      }
      dispatch({ type: 'ADD_MESSAGE', payload: welcomeMessage })
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || '清空对话失败' })
    }
  }

  // 初始化时创建会话
  useEffect(() => {
    createSession()
  }, [])

  const value: ChatContextType = {
    state,
    dispatch,
    sendMessage,
    createSession,
    clearConversation
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}

// Hook使用Context
export function useChat() {
  const context = useContext(ChatContext)
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider')
  }
  return context
}

// 获取欢迎消息
function getWelcomeMessage(promptType: string): string {
  const welcomeMessages = {
    default: '你好！我是DeepSeek V3智能助手。我可以帮助您解答问题、提供旅行建议、协助写作等。有什么我可以帮助您的吗？',
    travel: '你好！我是您的专属旅行规划师。我可以帮您规划行程、推荐景点、安排住宿和交通。请告诉我您想去哪里旅行？',
    writing: '你好！我是您的写作助手。我可以帮您写文章、修改文案、提供创意灵感。请告诉我您需要什么样的写作帮助？',
    code: '你好！我是您的编程专家。我可以帮您解决代码问题、提供技术建议、解释编程概念。请告诉我您遇到了什么编程问题？'
  }
  
  return welcomeMessages[promptType as keyof typeof welcomeMessages] || welcomeMessages.default
} 