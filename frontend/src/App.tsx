import { useState } from 'react'
import ChatPage from './pages/ChatPage.tsx'

export default function App() {
  const [mode, setMode] = useState('chat')

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="logo">🧮 数模智能体</h1>
          <p className="subtitle">数学建模竞赛全流程辅助</p>
        </div>

        <nav className="mode-nav">
          <button className={`mode-btn ${mode === 'chat' ? 'active' : ''}`} onClick={() => setMode('chat')}>
            <span className="mode-icon">💬</span>
            <span className="mode-label">对话解题</span>
          </button>
          <button className={`mode-btn ${mode === 'analysis' ? 'active' : ''}`} onClick={() => setMode('analysis')}>
            <span className="mode-icon">🔍</span>
            <span className="mode-label">选题分析</span>
          </button>
          <button className={`mode-btn ${mode === 'recommend' ? 'active' : ''}`} onClick={() => setMode('recommend')}>
            <span className="mode-icon">🎯</span>
            <span className="mode-label">模型推荐</span>
          </button>
          <button className={`mode-btn ${mode === 'code' ? 'active' : ''}`} onClick={() => setMode('code')}>
            <span className="mode-icon">💻</span>
            <span className="mode-label">代码生成</span>
          </button>
          <button className={`mode-btn ${mode === 'paper' ? 'active' : ''}`} onClick={() => setMode('paper')}>
            <span className="mode-icon">📄</span>
            <span className="mode-label">论文排版</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <p className="hint">选择功能开始使用</p>
        </div>
      </aside>

      <main className="main-content">
        <ChatPage mode={mode} setMode={setMode} />
      </main>
    </div>
  )
}
