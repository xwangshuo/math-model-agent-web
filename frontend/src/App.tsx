import { useState } from 'react'
import ChatPage from './pages/ChatPage.tsx'
import TopicSelection from './pages/TopicSelection.tsx'
import ProblemBank from './pages/ProblemBank.tsx'
import ModelKnowledge from './pages/ModelKnowledge.tsx'
import ExcellentPapers from './pages/ExcellentPapers.tsx'
import CodeExplainer from './pages/CodeExplainer.tsx'
import Simulation from './pages/Simulation.tsx'
import TutorMode from './pages/TutorMode.tsx'
import TeamAdvisor from './pages/TeamAdvisor.tsx'

export default function App() {
  const [mode, setMode] = useState('chat')

  const renderPage = () => {
    switch (mode) {
      case 'selection': return <TopicSelection />
      case 'problems': return <ProblemBank />
      case 'models': return <ModelKnowledge />
      case 'papers': return <ExcellentPapers />
      case 'explain': return <CodeExplainer />
      case 'simulate': return <Simulation />
      case 'tutor': return <TutorMode />
      case 'team': return <TeamAdvisor />
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

        <div className="sidebar-section-label">核心工具</div>
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

        <div className="sidebar-section-label" style={{ marginTop: 20 }}>学习资源</div>
        <nav className="mode-nav">
          <button className={`mode-btn ${mode === 'models' ? 'active' : ''}`} onClick={() => setMode('models')}>
            <span className="mode-icon">🧠</span>
            <span className="mode-label">模型知识库</span>
          </button>
          <button className={`mode-btn ${mode === 'problems' ? 'active' : ''}`} onClick={() => setMode('problems')}>
            <span className="mode-icon">📚</span>
            <span className="mode-label">历年赛题库</span>
          </button>
          <button className={`mode-btn ${mode === 'papers' ? 'active' : ''}`} onClick={() => setMode('papers')}>
            <span className="mode-icon">🏆</span>
            <span className="mode-label">优秀论文库</span>
          </button>
          <button className={`mode-btn ${mode === 'explain' ? 'active' : ''}`} onClick={() => setMode('explain')}>
            <span className="mode-icon">🔧</span>
            <span className="mode-label">代码调试助手</span>
          </button>
        </nav>

        <div className="sidebar-section-label" style={{ marginTop: 20 }}>赛题专项</div>
        <nav className="mode-nav">
          <button className={`mode-btn ${mode === 'selection' ? 'active' : ''}`} onClick={() => setMode('selection')}>
            <span className="mode-icon">🎯</span>
            <span className="mode-label">选题决策</span>
          </button>
          <button className={`mode-btn ${mode === 'simulate' ? 'active' : ''}`} onClick={() => setMode('simulate')}>
            <span className="mode-icon">🏋️</span>
            <span className="mode-label">实战训练</span>
          </button>
        </nav>

        <div className="sidebar-section-label" style={{ marginTop: 20 }}>团队协作</div>
        <nav className="mode-nav">
          <button className={`mode-btn ${mode === 'tutor' ? 'active' : ''}`} onClick={() => setMode('tutor')}>
            <span className="mode-icon">🧑‍🏫</span>
            <span className="mode-label">导师模式</span>
          </button>
          <button className={`mode-btn ${mode === 'team' ? 'active' : ''}`} onClick={() => setMode('team')}>
            <span className="mode-icon">👥</span>
            <span className="mode-label">团队分工</span>
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
