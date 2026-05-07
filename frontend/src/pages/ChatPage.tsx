import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { chatSend } from '../api/client.ts'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const MODE_NAMES: Record<string, string> = {
  chat: '💬 对话解题',
  analysis: '🔍 选题分析',
  recommend: '🎯 模型推荐',
  code: '💻 代码生成',
  paper: '📄 论文排版',
}

const MODE_PLACEHOLDERS: Record<string, string> = {
  chat: '输入你的数学建模问题...',
  analysis: '粘贴或描述赛题内容...',
  recommend: '描述你的问题类型和已知条件...',
  code: '描述你想生成的模型代码...',
  paper: '输入论文标题和主要内容...',
}

export default function ChatPage({ mode }: { mode: string; setMode: (m: string) => void }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Show welcome message per mode
  useEffect(() => {
    const welcomeMessages: Record<string, string> = {
      chat: '你好！我是数模竞赛助手，可以帮你解答数学建模相关问题。想从哪个方面开始？',
      analysis: '📋 **选题分析**\n\n请粘贴或描述赛题内容，我会分析题目类型、难度和解题方向，给出选题建议。',
      recommend: '🎯 **模型推荐**\n\n告诉我你的问题类型和已知条件，我会推荐最合适的数学模型，并解释原理和适用场景。',
      code: '💻 **代码生成**\n\n告诉我你想使用的模型和问题描述，我会生成完整可运行的 Python 求解代码。',
      paper: '📄 **论文排版**\n\n输入论文标题、摘要和各章节内容，我会生成 LaTeX 格式的竞赛论文。',
    }
    setMessages([{ role: 'assistant', content: welcomeMessages[mode] || welcomeMessages.chat }])
  }, [mode])

  const handleSend = async () => {
    if (!input.trim() || loading) return
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      const data = await chatSend(input, history, mode)
      const reply: Message = { role: 'assistant', content: data.reply || '抱歉，我暂时无法回答这个问题。' }
      setMessages(prev => [...prev, reply])
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ 网络错误，请检查后端服务是否启动。' }])
    }
    setLoading(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <h2>{MODE_NAMES[mode] || '💬 对话解题'}</h2>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role === 'user' ? 'user-msg' : 'assistant-msg'}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
            <div className="bubble">
              {msg.role === 'assistant' ? (
                <ReactMarkdown
                  components={{
                    code({ className, children, ...props }: any) {
                      const isInline = !className
                      if (isInline) return <code className="inline-code">{children}</code>
                      return (
                        <pre className="code-block">
                          <code className={className}>{children}</code>
                        </pre>
                      )
                    },
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant-msg">
            <div className="avatar">🤖</div>
            <div className="bubble thinking">
              <span className="dot-pulse"></span>
              思考中...
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          placeholder={MODE_PLACEHOLDERS[mode]}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
          disabled={loading}
        />
        <button className="send-btn" onClick={handleSend} disabled={loading || !input.trim()}>
          {loading ? '⏳' : '发送'}
        </button>
      </div>
    </div>
  )
}
