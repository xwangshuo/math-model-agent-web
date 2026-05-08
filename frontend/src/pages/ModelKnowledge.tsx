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

const CATEGORY_COLORS: Record<string, string> = {
  '优化类': '#6366f1',
  '评价类': '#f59e0b',
  '统计类': '#06b6d4',
  '机器学习': '#8b5cf6',
  '机理建模': '#ef4444',
  '模拟类': '#22c55e',
  '预测类': '#ec4899',
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
        <h2>🧠 模型知识库</h2>
        <p>20 个常用数模模型 · 数学原理 · 代码模板 · 常见错误</p>
      </div>

      {/* 分类筛选 chips */}
      <div className="mk-cats">
        <button className={`mk-chip ${selectedCat === '' ? 'active' : ''}`} onClick={() => setSelectedCat('')}>
          📋 全部 <span className="mk-chip-count">{models.length}</span>
        </button>
        {categories.map(c => (
          <button key={c} className={`mk-chip ${selectedCat === c ? 'active' : ''}`} onClick={() => setSelectedCat(c)}
            style={selectedCat === c ? { borderColor: CATEGORY_COLORS[c], background: CATEGORY_COLORS[c] + '18' } : {}}>
            {c}
          </button>
        ))}
      </div>

      <div className="mk-layout">
        {/* 左栏：卡片网格 */}
        <div className="mk-grid-col">
          <div className="mk-grid">
            {models.map(m => (
              <div key={m.id} className={`mk-card ${selectedModel?.id === m.id ? 'selected' : ''}`}
                onClick={() => loadDetail(m.id)}
                style={selectedModel?.id === m.id ? {
                  borderColor: CATEGORY_COLORS[m.category] || '#6366f1',
                  boxShadow: `0 4px 20px ${(CATEGORY_COLORS[m.category] || '#6366f1')}22`
                } : {}}>
                <div className="mk-card-top">
                  <span className="mk-icon">{m.icon}</span>
                  <span className="mk-badge" style={{
                    background: (CATEGORY_COLORS[m.category] || '#6366f1') + '18',
                    color: CATEGORY_COLORS[m.category] || '#6366f1',
                  }}>{m.category}</span>
                </div>
                <div className="mk-card-name">{m.name}</div>
                <div className="mk-card-desc">{m.summary.slice(0, 45)}..</div>
                <div className="mk-card-tags">
                  {m.tags.slice(0, 3).map(t => <span key={t} className="mk-tag">{t}</span>)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 右栏：详情面板 */}
        <div className="mk-detail-col">
          {loading && (
            <div className="mk-empty">
              <div className="mk-loading-spinner" />
              <p>加载中...</p>
            </div>
          )}

          {selectedModel && !loading && (
            <div className="mk-detail">
              {/* 头部 */}
              <div className="mk-detail-head">
                <div className="mk-detail-head-left">
                  <span className="mk-detail-icon">{selectedModel.icon}</span>
                  <div>
                    <h3>{selectedModel.name}</h3>
                    <span className="mk-badge" style={{
                      background: (CATEGORY_COLORS[selectedModel.category] || '#6366f1') + '18',
                      color: CATEGORY_COLORS[selectedModel.category] || '#6366f1',
                      fontSize: 11,
                    }}>{selectedModel.category}</span>
                  </div>
                </div>
              </div>

              <div className="mk-detail-summary">{selectedModel.summary}</div>

              {/* 场景 */}
              <div className="mk-scenes">
                <div className="mk-section-label">🎯 适用场景</div>
                <div className="mk-scene-grid">
                  {selectedModel.applicable_scenarios.map((s, i) => (
                    <div key={i} className="mk-scene-item">
                      <span className="mk-scene-dot" style={{ background: CATEGORY_COLORS[selectedModel.category] || '#6366f1' }} />
                      {s}
                    </div>
                  ))}
                </div>
              </div>

              {/* Tabs */}
              <div className="mk-tabs">
                <button className={`mk-tab ${activeTab === 'principles' ? 'active' : ''}`}
                  onClick={() => setActiveTab('principles')}
                  style={activeTab === 'principles' ? { color: CATEGORY_COLORS[selectedModel.category], borderBottomColor: CATEGORY_COLORS[selectedModel.category] } : {}}>
                  📐 数学原理
                </button>
                <button className={`mk-tab ${activeTab === 'code' ? 'active' : ''}`}
                  onClick={() => setActiveTab('code')}
                  style={activeTab === 'code' ? { color: CATEGORY_COLORS[selectedModel.category], borderBottomColor: CATEGORY_COLORS[selectedModel.category] } : {}}>
                  💻 代码模板
                </button>
                <button className={`mk-tab ${activeTab === 'errors' ? 'active' : ''}`}
                  onClick={() => setActiveTab('errors')}
                  style={activeTab === 'errors' ? { color: CATEGORY_COLORS[selectedModel.category], borderBottomColor: CATEGORY_COLORS[selectedModel.category] } : {}}>
                  ⚠️ 常见错误
                </button>
              </div>

              {/* Tab 内容 */}
              <div className="mk-tab-content">
                {activeTab === 'principles' && (
                  <>
                    <div className="mk-math-content">
                      <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                        {selectedModel.math_principles}
                      </ReactMarkdown>
                    </div>
                    <div className="mk-gutter">
                      <div className="mk-pros">
                        <div className="mk-gutter-title" style={{ color: '#22c55e' }}>✅ 优点</div>
                        <ul>{selectedModel.pros.map((p, i) => <li key={i}>{p}</li>)}</ul>
                      </div>
                      <div className="mk-cons">
                        <div className="mk-gutter-title" style={{ color: '#ef4444' }}>❌ 缺点</div>
                        <ul>{selectedModel.cons.map((c, i) => <li key={i}>{c}</li>)}</ul>
                      </div>
                    </div>
                    <div className="mk-pkgs">
                      📦 <strong>依赖包: </strong>
                      {selectedModel.python_packages.map((pkg, i) => (
                        <code key={i} className="mk-pkg">{pkg}</code>
                      ))}
                    </div>
                  </>
                )}

                {activeTab === 'code' && (
                  <div className="mk-code-section">
                    <pre className="mk-code-block"><code>{selectedModel.code_template}</code></pre>
                    <button className="mk-copy-btn" onClick={() => navigator.clipboard.writeText(selectedModel.code_template)}>
                      📋 复制代码
                    </button>
                  </div>
                )}

                {activeTab === 'errors' && (
                  <div className="mk-errors">
                    {selectedModel.common_errors.map(([err, fix], i) => (
                      <div key={i} className="mk-error-item">
                        <div className="mk-error-problem">⚠️ {err}</div>
                        <div className="mk-error-fix">💡 {fix}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {!selectedModel && !loading && (
            <div className="mk-empty">
              <span className="mk-empty-icon">👆</span>
              <p>点击左侧模型卡片查看完整知识详情</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
