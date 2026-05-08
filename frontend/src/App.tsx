import { useState } from 'react'
import ChatPage from './pages/ChatPage.tsx'
import TopicSelection from './pages/TopicSelection.tsx'
import ProblemBank from './pages/ProblemBank.tsx'

export default function App() {
  const [mode, setMode] = useState('chat')

  const renderPage = () => {
    switch (mode) {
      case 'selection': return <TopicSelection />
      case 'problems': return <ProblemBank />
      default: return <ChatPage mode={mode} setMode={setMode} />
    }
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="logo">🧮 数模智能体</h1>
          <p className="subtitle">数学建模竞赛全流程辅助</p>
        </div>

        <div className="mode-section-label">核心工具</div>
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

        <div className="mode-section-label" style={{ marginTop: 20 }}>赛题专项</div>
        <nav className="mode-nav">
          <button className={`mode-btn ${mode === 'selection' ? 'active' : ''}`} onClick={() => setMode('selection')}>
            <span className="mode-icon">🎯</span>
            <span className="mode-label">选题决策</span>
          </button>
          <button className={`mode-btn ${mode === 'problems' ? 'active' : ''}`} onClick={() => setMode('problems')}>
            <span className="mode-icon">📚</span>
            <span className="mode-label">历年赛题库</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <p className="hint">华东师范大学 · 数学建模</p>
        </div>
      </aside>

      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  )
}
