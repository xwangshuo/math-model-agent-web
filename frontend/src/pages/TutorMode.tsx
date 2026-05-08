import { useState, useEffect, useRef } from 'react'

interface TutorMode {
  id: string
  name: string
  icon: string
  description: string
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  mode?: string
}

export default function TutorMode() {
  const [modes, setModes] = useState<TutorMode[]>([])
  const [selectedMode, setSelectedMode] = useState<TutorMode | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadModes()
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadModes = async () => {
    try {
      const res = await fetch('/api/tutor/modes')
      const data = await res.json()
      setModes(data.modes || data)
    } catch { /* ignore */ }
  }

  const handleSelectMode = (mode: TutorMode) => {
    setSelectedMode(mode)
    setMessages([{
      role: 'assistant',
      content: `你好！我是 **${mode.name}** 导师。${mode.description}\n\n请问有什么数学建模问题需要我帮助？`,
      mode: mode.name,
    }])
    setInput('')
    setError('')
  }

  const handleSend = async () => {
    if (!input.trim() || loading || !selectedMode) return

    const userMsg: Message = { role: 'user', content: input, mode: selectedMode.name }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    setError('')

    const history = messages.map(m => ({ role: m.role, content: m.content }))

    try {
      const res = await fetch('/api/tutor/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          history,
          mode: selectedMode.id,
          context: '',
        }),
      })
      if (!res.ok) throw new Error('请求失败')
      const data = await res.json()
      const reply: Message = { role: 'assistant', content: data.reply, mode: selectedMode.name }
      setMessages(prev => [...prev, reply])
    } catch (e: any) {
      setError(e.message || '对话失败，请检查后端服务')
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ 对话失败，请稍后重试。',
        mode: selectedMode.name,
      }])
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
    <div className="page-container">
      <div className="page-header">
        <h2>🧑‍🏫 角色化导师模式</h2>
        <p>选择导师角色，获得个性化指导</p>
      </div>

      {/* Role selector cards */}
      <div style={{ padding: '16px 20px', display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        {modes.map(mode => (
          <div
            key={mode.id}
            onClick={() => handleSelectMode(mode)}
            style={{
              flex: '1 1 180px', maxWidth: 260, cursor: 'pointer',
              padding: 16, borderRadius: 'var(--radius-md)',
              border: selectedMode?.id === mode.id
                ? '2px solid var(--primary)'
                : '1px solid var(--card-border)',
              background: selectedMode?.id === mode.id
                ? 'linear-gradient(135deg, #f5f3ff, #ede9fe)'
                : 'var(--card-bg)',
              boxShadow: selectedMode?.id === mode.id ? '0 4px 16px rgba(99,102,241,0.15)' : 'var(--shadow-sm)',
              transition: 'all 0.25s',
            }}
          >
            <div style={{ fontSize: 32, marginBottom: 8, textAlign: 'center' }}>{mode.icon}</div>
            <div style={{
              fontSize: 14, fontWeight: 600, color: selectedMode?.id === mode.id ? 'var(--primary-dark)' : 'var(--text)',
              textAlign: 'center', marginBottom: 4,
            }}>
              {mode.name}
            </div>
            <div style={{
              fontSize: 12, color: 'var(--text-muted)', textAlign: 'center',
              lineHeight: 1.5,
            }}>
              {mode.description}
            </div>
            {selectedMode?.id === mode.id && (
              <div style={{
                textAlign: 'center', marginTop: 8, fontSize: 11, fontWeight: 600,
                color: 'var(--primary)',
              }}>
                ✓ 当前导师
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Chat area */}
      {selectedMode ? (
        <div style={{
          flex: 1, margin: '0 20px 16px', display: 'flex', flexDirection: 'column',
          border: '1px solid var(--card-border)', borderRadius: 'var(--radius-md)',
          overflow: 'hidden', background: 'var(--card-bg)',
        }}>
          {/* Chat header */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '12px 20px', borderBottom: '1px solid var(--card-border)',
            background: 'var(--primary-bg)',
          }}>
            <span style={{ fontSize: 24 }}>{selectedMode.icon}</span>
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--primary-dark)' }}>
                {selectedMode.name}
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                当前对话 · 发送消息开始提问
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-messages" style={{ flex: 1, padding: 20, maxHeight: 'none' }}>
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role === 'user' ? 'user-msg' : 'assistant-msg'}`}>
                <div className="avatar">
                  {msg.role === 'user' ? '👤' : selectedMode.icon || '🤖'}
                </div>
                <div className="bubble">
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 6 }}>
                    {msg.role === 'assistant' ? (msg.mode || selectedMode.name) : '你'}
                  </div>
                  <div style={{ fontSize: 14, lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="message assistant-msg">
                <div className="avatar">{selectedMode.icon || '🤖'}</div>
                <div className="bubble thinking">
                  <span className="dot-pulse"></span>
                  {selectedMode.name}正在思考...
                </div>
              </div>
            )}

            {error && (
              <div className="message assistant-msg">
                <div className="avatar">⚠️</div>
                <div className="bubble" style={{ borderColor: '#fca5a5', background: '#fef2f2' }}>
                  <p style={{ color: 'var(--danger)', fontSize: 13 }}>{error}</p>
                </div>
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* Input area */}
          <div className="chat-input-area">
            <textarea
              className="chat-input"
              placeholder={`向 ${selectedMode.name} 提问...`}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={2}
              disabled={loading}
            />
            {loading ? (
              <button className="stop-btn" onClick={() => setLoading(false)}>⏹ 停止</button>
            ) : (
              <button className="send-btn" onClick={handleSend} disabled={!input.trim()}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 4 }}>
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
                发送
              </button>
            )}
          </div>
        </div>
      ) : (
        /* Empty state */
        <div style={{ flex: 1, margin: '0 20px 16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="card hint-card" style={{ padding: '80px 40px', textAlign: 'center', maxWidth: 500 }}>
            <p style={{ fontSize: 64, marginBottom: 16 }}>🧑‍🏫</p>
            <p style={{ color: 'var(--text-muted)', fontSize: 14, lineHeight: 1.8 }}>
              请选择上方一位导师开始对话<br />
              <span style={{ fontSize: 12 }}>不同导师有不同专业领域和指导风格</span>
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
