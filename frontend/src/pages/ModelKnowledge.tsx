import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'

const API_BASE = '/api'

interface ModelCard {
  id: string; name: string; category: string; icon: string
  tags: string[]; summary: string; applicable_scenarios: string[]
  pros: string[]; cons: string[]; python_packages: string[]
}

interface ModelDetail extends ModelCard {
  math_principles: string; code_template: string; common_errors: [string, string][]
}

export default function ModelKnowledge() {
  const [models, setModels] = useState<ModelCard[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCat, setSelectedCat] = useState('')
  const [selectedModel, setSelectedModel] = useState<ModelDetail | null>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'principles' | 'code' | 'errors'>('principles')

  useEffect(() => { loadModels() }, [selectedCat])

  const loadModels = async () => {
    const url = selectedCat ? `${API_BASE}/model-knowledge?category=${selectedCat}` : `${API_BASE}/model-knowledge`
    const res = await fetch(url)
    const data = await res.json()
    setModels(data.models)
    setCategories(data.categories)
  }

  const loadDetail = async (id: string) => {
    setLoading(true)
    const res = await fetch(`${API_BASE}/model-knowledge/${id}`)
    const data = await res.json()
    setSelectedModel(data)
    setLoading(false)
    setActiveTab('principles')
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>📚 模型知识库</h2>
        <p>10个常用数模模型知识卡片 — 适用场景、数学原理、代码模板、常见错误</p>
      </div>

      <div className="filter-row" style={{ marginBottom: 20 }}>
        <button className={`filter-chip ${selectedCat === '' ? 'active' : ''}`} onClick={() => setSelectedCat('')}>全部</button>
        {categories.map(c => (
          <button key={c} className={`filter-chip ${selectedCat === c ? 'active' : ''}`} onClick={() => setSelectedCat(c)}>{c}</button>
        ))}
      </div>

      <div className="two-col-layout">
        <div className="col-left">
          <div className="model-grid">
            {models.map(m => (
              <div key={m.id} className="knowledge-card" onClick={() => loadDetail(m.id)}>
                <div className="kc-icon">{m.icon}</div>
                <div className="kc-header">
                  <span className="kc-name">{m.name}</span>
                  <span className="kc-badge">{m.category}</span>
                </div>
                <div className="kc-summary">{m.summary}</div>
                <div className="kc-tags">
                  {m.tags.map(t => <span key={t} className="tag">{t}</span>)}
                </div>
                <div className="kc-footer">
                  <span className="kc-hint">📋 查看详情 →</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="col-right">
          {loading && <div className="card" style={{ padding: 40, textAlign: 'center' }}>⏳ 加载中...</div>}

          {selectedModel && !loading && (
            <div className="card model-detail-card">
              <div className="md-header">
                <span className="md-icon">{selectedModel.icon}</span>
                <div>
                  <h3>{selectedModel.name}</h3>
                  <span className="kc-badge">{selectedModel.category}</span>
                </div>
              </div>
              <p className="md-summary">{selectedModel.summary}</p>

              <div className="md-scenarios">
                <strong>适用场景:</strong>
                <ul>{selectedModel.applicable_scenarios.map((s, i) => <li key={i}>{s}</li>)}</ul>
              </div>

              <div className="md-tab-bar">
                <button className={`md-tab ${activeTab === 'principles' ? 'active' : ''}`} onClick={() => setActiveTab('principles')}>📐 数学原理</button>
                <button className={`md-tab ${activeTab === 'code' ? 'active' : ''}`} onClick={() => setActiveTab('code')}>💻 代码模板</button>
                <button className={`md-tab ${activeTab === 'errors' ? 'active' : ''}`} onClick={() => setActiveTab('errors')}>⚠️ 常见错误</button>
              </div>

              <div className="md-content">
                {activeTab === 'principles' && (
                  <div className="md-math">
                    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>{selectedModel.math_principles}</ReactMarkdown>
                    <div className="md-pros-cons">
                      <div className="md-pros">
                        <strong>✅ 优点</strong>
                        <ul>{selectedModel.pros.map((p, i) => <li key={i}>{p}</li>)}</ul>
                      </div>
                      <div className="md-cons">
                        <strong>❌ 缺点</strong>
                        <ul>{selectedModel.cons.map((c, i) => <li key={i}>{c}</li>)}</ul>
                      </div>
                    </div>
                    <div className="md-packages">
                      <strong>📦 Python 包: </strong>
                      {selectedModel.python_packages.join(' · ')}
                    </div>
                  </div>
                )}

                {activeTab === 'code' && (
                  <div>
                    <pre className="code-block"><code>{selectedModel.code_template}</code></pre>
                    <button className="secondary-btn" onClick={() => navigator.clipboard.writeText(selectedModel.code_template)}>
                      📋 复制代码
                    </button>
                  </div>
                )}

                {activeTab === 'errors' && (
                  <div className="md-errors">
                    {selectedModel.common_errors.map(([err, fix], i) => (
                      <div key={i} className="error-item">
                        <div className="error-problem">⚠️ {err}</div>
                        <div className="error-fix">💡 {fix}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {!selectedModel && !loading && (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              <p style={{ fontSize: 48, marginBottom: 16 }}>👆</p>
              <p>点击左侧卡片查看完整知识详情</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
