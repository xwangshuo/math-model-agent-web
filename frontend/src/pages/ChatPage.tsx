import { useState, useRef, useEffect, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import { chatStream, uploadFile, getSessions, saveSession, loadSession, deleteSession, getModels, analyzeData } from '../api/client.ts'

interface Message {
  role: 'user' | 'assistant'
  content: string
  figures?: string[]
}

interface StreamEvent {
  type: string
  content?: string
  name?: string
  figures?: string[]
  count?: number
}

export default function ChatPage({ mode, setMode }: { mode: string; setMode: (m: string) => void }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [model, setModel] = useState('deepseek/deepseek-chat-v3.1')
  const [models, setModels] = useState<any[]>([])
  const [sessions, setSessions] = useState<any[]>([])
  const [currentSessionId, setCurrentSessionId] = useState('')
  const [uploadedFilePath, setUploadedFilePath] = useState('')
  const [uploadedFileName, setUploadedFileName] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const abortRef = useRef<AbortController | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // 初始化
  useEffect(() => {
    getModels().then(setModels).catch(() => {})
    refreshSessions()
  }, [])

  // 自动滚动
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // 模式切换 → 欢迎消息
  useEffect(() => {
    const welcomeMessages: Record<string, string> = {
      chat: '你好！我是数模竞赛助手，可以帮你解答数学建模相关问题。想从哪个方面开始？',
      analysis: '📋 **选题分析**\n\n请粘贴或描述赛题内容，我会分析题目类型、难度和解题方向。',
      recommend: '🎯 **模型推荐**\n\n告诉我你的问题类型和已知条件，我会推荐最合适的数学模型。',
      code: '💻 **代码生成**\n\n告诉我你想使用的模型和问题描述，我会生成完整可运行的 Python 求解代码。',
      paper: '📄 **论文排版**\n\n输入论文标题、摘要和各章节内容，我会生成 LaTeX 格式的竞赛论文。',
    }
    if (!loading) {
      setMessages([{ role: 'assistant', content: welcomeMessages[mode] || welcomeMessages.chat }])
    }
  }, [mode])

  const refreshSessions = async () => {
    try {
      setSessions(await getSessions())
    } catch { /* ignore */ }
  }

  // 发送消息
  const handleSend = useCallback(async () => {
    if (!input.trim() || loading) return

    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    const history = messages.map(m => ({ role: m.role, content: m.content }))

    // 添加流式占位
    setMessages(prev => [...prev, { role: 'assistant', content: '', figures: [] }])

    const controller = new AbortController()
    abortRef.current = controller

    let currentText = ''
    let currentFigures: string[] = []

    try {
      await chatStream(
        input,
        history,
        model,
        uploadedFilePath,
        (event: StreamEvent) => {
          if (event.type === 'text') {
            currentText += event.content || ''
            setMessages(prev => {
              const next = [...prev]
              const last = next[next.length - 1]
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: currentText, figures: currentFigures }
              }
              return next
            })
          } else if (event.type === 'tool_start') {
            const toolMsg = `\n\n🔧 **正在执行: ${event.name}...**`
            currentText += toolMsg
            setMessages(prev => {
              const next = [...prev]
              const last = next[next.length - 1]
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: currentText, figures: currentFigures }
              }
              return next
            })
          } else if (event.type === 'tool_result') {
            const resultMsg = `\n\n📋 **工具执行结果:**\n\`\`\`\n${event.content}\n\`\`\``
            currentText += resultMsg
            setMessages(prev => {
              const next = [...prev]
              const last = next[next.length - 1]
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: currentText, figures: currentFigures }
              }
              return next
            })
          } else if (event.type === 'figures' && event.figures) {
            currentFigures = [...currentFigures, ...event.figures]
            setMessages(prev => {
              const next = [...prev]
              const last = next[next.length - 1]
              if (last && last.role === 'assistant') {
                next[next.length - 1] = { ...last, content: currentText, figures: currentFigures }
              }
              return next
            })
          } else if (event.type === 'error') {
            setMessages(prev => {
              const next = [...prev]
              if (next[next.length - 1]?.role === 'assistant' && next[next.length - 1].content === '') {
                next.pop()
              }
              next.push({ role: 'assistant', content: `❌ ${event.content}` })
              return next
            })
          }
        },
        controller.signal
      )
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        // 清除空占位
        setMessages(prev => {
          const next = [...prev]
          if (next[next.length - 1]?.role === 'assistant' && next[next.length - 1].content === '') {
            next.pop()
          }
          next.push({ role: 'assistant', content: '⚠️ 网络错误，请检查后端服务是否启动。' })
          return next
        })
      }
    }

    setLoading(false)
    abortRef.current = null
  }, [input, loading, messages, model, uploadedFilePath])

  // 停止生成
  const handleStop = () => {
    abortRef.current?.abort()
    setLoading(false)
  }

  // 文件上传
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    try {
      const result = await uploadFile(file)
      setUploadedFilePath(result.file_path)
      setUploadedFileName(result.filename)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `📎 已上传文件: **${result.filename}**\n\n\`\`\`\n${result.analysis.slice(0, 500)}...\n\`\`\``,
      }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ 文件上传失败' }])
    }
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  // 一键数据分析
  const handleAnalyze = async (type: string, method?: string) => {
    if (!uploadedFilePath || analyzing) return
    setAnalyzing(true)
    const typeLabels: Record<string, string> = {
      eda: '📊 一键 EDA',
      outlier: '⚠️ 异常值检测',
      missing: '🔍 缺失值分析',
    }
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: `🔄 **${typeLabels[type] || type}** 正在运行...`,
    }])
    try {
      const result = await analyzeData(uploadedFilePath, type, method)
      setMessages(prev => {
        const next = [...prev]
        next[next.length - 1] = {
          role: 'assistant',
          content: `## ${typeLabels[type] || type}\n\n\`\`\`\n${result.output}\n\`\`\``,
          figures: result.figures || [],
        }
        return next
      })
    } catch {
      setMessages(prev => {
        const next = [...prev]
        next[next.length - 1] = { role: 'assistant', content: '⚠️ 分析失败，请检查文件是否有效。' }
        return next
      })
    }
    setAnalyzing(false)
  }

  // 保存会话
  const handleSave = async () => {
    const history = messages.map(m => ({ role: m.role, content: m.content }))
    const result = await saveSession(history, model, '', currentSessionId)
    setCurrentSessionId(result.session_id)
    await refreshSessions()
  }

  // 加载会话
  const handleLoad = async (sessionId: string) => {
    const data = await loadSession(sessionId)
    if (!data) return
    setCurrentSessionId(data.id)
    setModel(data.model || model)
    const msgs: Message[] = (data.messages || []).map((m: any) => ({
      role: m.role,
      content: m.content,
      figures: m.figures || [],
    }))
    setMessages(msgs)
  }

  // 新对话
  const handleNew = () => {
    if (abortRef.current) abortRef.current.abort()
    setMessages([])
    setCurrentSessionId('')
    setUploadedFilePath('')
    setUploadedFileName('')
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
      {/* 顶栏 */}
      <div className="chat-toolbar">
        <div className="toolbar-left">
          <select
            className="model-select"
            value={model}
            onChange={e => setModel(e.target.value)}
            disabled={loading}
          >
            {models.map(m => (
              <option key={m.id} value={m.id}>{m.provider}/{m.name}</option>
            ))}
          </select>
          <button className="tb-btn" onClick={handleNew} title="新对话">🆕</button>
          <button className="tb-btn" onClick={handleSave} title="保存会话" disabled={messages.length === 0}>💾</button>
          <select
            className="session-select"
            value=""
            onChange={e => { if (e.target.value) handleLoad(e.target.value) }}
          >
            <option value="">📂 历史会话</option>
            {sessions.map(s => (
              <option key={s.id} value={s.id}>{s.title} ({s.message_count}条)</option>
            ))}
          </select>
        </div>
        <div className="toolbar-right">
          {uploadedFileName && (
            <div className="analysis-buttons">
              <span className="file-badge">📎 {uploadedFileName}</span>
              <button className="tb-btn analysis-btn" onClick={() => handleAnalyze('eda')} disabled={analyzing} title="一键 EDA">📊 EDA</button>
              <button className="tb-btn analysis-btn" onClick={() => handleAnalyze('missing')} disabled={analyzing} title="缺失值分析">🔍 缺失值</button>
              <button className="tb-btn analysis-btn" onClick={() => handleAnalyze('outlier', 'iqr')} disabled={analyzing} title="异常值检测">⚠️ 异常值</button>
            </div>
          )}
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            accept=".csv,.xls,.xlsx"
            onChange={handleFileUpload}
          />
          <button className="tb-btn" onClick={() => fileInputRef.current?.click()} title="上传数据文件">📤</button>
        </div>
      </div>

      {/* 消息区 */}
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role === 'user' ? 'user-msg' : 'assistant-msg'}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
            <div className="bubble">
              {msg.role === 'assistant' ? (
                <>
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
                    {msg.content || (loading && i === messages.length - 1 ? '思考中...' : '')}
                  </ReactMarkdown>
                  {msg.figures && msg.figures.length > 0 && (
                    <div className="figure-gallery">
                      {msg.figures.map((b64, fi) => (
                        <img
                          key={fi}
                          src={`data:image/png;base64,${b64}`}
                          alt={`图表 ${fi + 1}`}
                          className="figure-img"
                        />
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <p>{msg.content}</p>
              )}
            </div>
          </div>
        ))}
        {loading && messages[messages.length - 1]?.role === 'assistant' && !messages[messages.length - 1]?.content && (
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

      {/* 输入区 */}
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          placeholder="描述你的数学建模问题..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
          disabled={loading}
        />
        {loading ? (
          <button className="stop-btn" onClick={handleStop}>⏹ 停止</button>
        ) : (
          <button className="send-btn" onClick={handleSend} disabled={!input.trim()}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{marginRight: 4}}>
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            发送
          </button>
        )}
      </div>
    </div>
  )
}
