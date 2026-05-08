import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { searchProblems, getProblem, getProblemContent, getReadingTemplate, generateReadingTemplate } from '../api/client.ts'

export default function ProblemBank() {
  const [problems, setProblems] = useState<any[]>([])
  const [filters, setFilters] = useState<any>({})
  const [searchKw, setSearchKw] = useState('')
  const [compFilter, setCompFilter] = useState('')
  const [diffFilter, setDiffFilter] = useState('')
  const [yearFilter, setYearFilter] = useState(0)
  const [categoryFilter, setCategoryFilter] = useState('')
  const [selectedProblem, setSelectedProblem] = useState<any>(null)
  const [template, setTemplate] = useState('')
  const [templateLoading, setTemplateLoading] = useState(false)
  const [showCustomTemplate, setShowCustomTemplate] = useState(false)
  const [customTitle, setCustomTitle] = useState('')
  const [customDesc, setCustomDesc] = useState('')
  // 原题全文
  const [showContent, setShowContent] = useState(false)
  const [contentLoading, setContentLoading] = useState(false)
  const [problemContent, setProblemContent] = useState('')

  useEffect(() => {
    loadProblems()
  }, [searchKw, compFilter, diffFilter, yearFilter, categoryFilter])

  const loadProblems = async () => {
    const data = await searchProblems({
      keyword: searchKw, competition: compFilter,
      difficulty: diffFilter, year: yearFilter || undefined,
      category: categoryFilter,
    })
    setProblems(data.problems)
    setFilters(data.filters)
  }

  const handleSelect = async (id: string) => {
    const p = await getProblem(id)
    setSelectedProblem(p)
    setTemplate('')
    setShowContent(false)
  }

  const handleTemplate = async () => {
    if (!selectedProblem) return
    setTemplateLoading(true)
    const data = await getReadingTemplate(selectedProblem.id)
    setTemplate(data.template)
    setTemplateLoading(false)
  }

  const handleCustomTemplate = async () => {
    if (!customTitle.trim()) return
    setTemplateLoading(true)
    const data = await generateReadingTemplate({ title: customTitle, description: customDesc })
    setTemplate(data.template)
    setTemplateLoading(false)
    setShowCustomTemplate(false)
  }

  const handleViewContent = async () => {
    if (!selectedProblem) return
    setContentLoading(true)
    setShowContent(true)
    try {
      const data = await getProblemContent(selectedProblem.id)
      setProblemContent(data.content)
    } catch (e: any) {
      setProblemContent('⚠️ 该赛题暂未收录原题全文')
    }
    setContentLoading(false)
  }

  const handlePrevProblem = () => {
    const idx = problems.findIndex(p => p.id === selectedProblem?.id)
    if (idx > 0) handleSelect(problems[idx - 1].id)
  }
  const handleNextProblem = () => {
    const idx = problems.findIndex(p => p.id === selectedProblem?.id)
    if (idx < problems.length - 1) handleSelect(problems[idx + 1].id)
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>📚 历年赛题库</h2>
        <p>CUMCM / MCM / ICM 真题检索（2015-2025，共 81 题）</p>
      </div>

      <div className="two-col-layout">
        {/* 左栏：筛选 + 列表 */}
        <div className="col-left">
          <div className="card">
            <div className="filter-row">
              <input className="search-input" placeholder="🔍 搜索题目/模型/标签..." value={searchKw}
                onChange={e => setSearchKw(e.target.value)} />
            </div>
            <div className="filter-row">
              <select className="filter-select" value={compFilter} onChange={e => setCompFilter(e.target.value)}>
                <option value="">全部竞赛</option>
                {(filters.competitions || []).map((c: string) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <select className="filter-select" value={yearFilter} onChange={e => setYearFilter(Number(e.target.value))}>
                <option value={0}>全部年份</option>
                {(filters.years || []).map((y: number) => (
                  <option key={y} value={y}>{y}年</option>
                ))}
              </select>
              <select className="filter-select" value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}>
                <option value="">全部类别</option>
                {(filters.categories || []).map((c: string) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <select className="filter-select short" value={diffFilter} onChange={e => setDiffFilter(e.target.value)}>
                <option value="">难度</option>
                {(filters.difficulties || []).map((d: string) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
            <div className="result-count">共 {problems.length} 题</div>
          </div>

          <div className="problem-list">
            {problems.length === 0 && <p className="empty-hint">无匹配赛题</p>}
            {problems.map(p => (
              <div
                key={p.id}
                className={`problem-card ${selectedProblem?.id === p.id ? 'selected' : ''}`}
                onClick={() => handleSelect(p.id)}
              >
                <div className="problem-card-header">
                  <span className="prob-badge">{p.competition} {p.year}</span>
                  <span className={`diff-badge diff-${p.difficulty.toLowerCase()}`}>{p.difficulty}</span>
                  <span className="prob-category">{p.category}</span>
                </div>
                <div className="prob-title">{p.label} · {p.title}</div>
                <div className="prob-models">{p.models.slice(0, 3).join(' · ')}</div>
                <div className="prob-tags">
                  {p.tags.slice(0, 3).map((t: string) => (
                    <span key={t} className="tag">{t}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 右栏：详情 + 模板 */}
        <div className="col-right">
          {selectedProblem && (
            <div className="card">
              <h3>{selectedProblem.competition} {selectedProblem.year} {selectedProblem.label}</h3>
              <h4 className="prob-title-large">{selectedProblem.title}</h4>
              <div className="detail-grid">
                <div><strong>类别</strong><br/>{selectedProblem.category}</div>
                <div><strong>难度</strong><br/><span className={`diff-badge diff-${selectedProblem.difficulty.toLowerCase()}`}>{selectedProblem.difficulty}</span></div>
                <div><strong>数据</strong><br/>{selectedProblem.data_type}</div>
              </div>
              <p className="detail-desc">{selectedProblem.description}</p>
              <div className="detail-models">
                <strong>推荐模型:</strong> {selectedProblem.models.join(' · ')}
              </div>
              <div className="detail-tags">
                {selectedProblem.tags.map((t: string) => (
                  <span key={t} className="tag">{t}</span>
                ))}
              </div>
              <div className="btn-row">
                <button className="primary-btn" onClick={handleViewContent}>
                  📄 查看原题
                </button>
                <button className="secondary-btn" onClick={handleTemplate} disabled={templateLoading}>
                  {templateLoading ? '⏳ 生成中...' : '📖 生成速读模板'}
                </button>
              </div>
              {/* 上/下导航 */}
              <div className="nav-row">
                <button className="nav-btn" onClick={handlePrevProblem}
                  disabled={problems.findIndex(p => p.id === selectedProblem.id) <= 0}>
                  ◀ 上一题
                </button>
                <span className="nav-count">
                  {problems.findIndex(p => p.id === selectedProblem.id) + 1} / {problems.length}
                </span>
                <button className="nav-btn" onClick={handleNextProblem}
                  disabled={problems.findIndex(p => p.id === selectedProblem.id) >= problems.length - 1}>
                  下一题 ▶
                </button>
              </div>
            </div>
          )}

          {!selectedProblem && (
            <div className="card">
              <button className="secondary-btn" onClick={() => setShowCustomTemplate(!showCustomTemplate)}>
                ✏️ 自定义题目速读模板
              </button>
              {showCustomTemplate && (
                <div className="custom-template-form" style={{ marginTop: 12 }}>
                  <input className="search-input" placeholder="题目标题" value={customTitle}
                    onChange={e => setCustomTitle(e.target.value)} />
                  <textarea className="template-textarea" placeholder="题目描述（粘贴赛题内容）" rows={6}
                    value={customDesc} onChange={e => setCustomDesc(e.target.value)} />
                  <button className="primary-btn" onClick={handleCustomTemplate} disabled={templateLoading}>
                    生成模板
                  </button>
                </div>
              )}
            </div>
          )}

          {template && (
            <div className="card template-card">
              <h3>📖 速读模板</h3>
              <pre className="template-pre">{template}</pre>
              <button className="secondary-btn" onClick={() => {
                navigator.clipboard.writeText(template)
              }}>📋 复制模板</button>
            </div>
          )}
        </div>
      </div>

      {/* ─── 原题全文 Modal ─── */}
      {showContent && (
        <div className="modal-overlay" onClick={() => setShowContent(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📄 {selectedProblem?.title}</h3>
              <span className="modal-subtitle">{selectedProblem?.competition} {selectedProblem?.year} {selectedProblem?.label}</span>
              <button className="modal-close" onClick={() => setShowContent(false)}>✕</button>
            </div>
            <div className="modal-body">
              {contentLoading ? (
                <p className="loading-hint">⏳ 加载中...</p>
              ) : (
                <pre className="content-text">{problemContent}</pre>
              )}
            </div>
            <div className="modal-footer">
              <button className="secondary-btn" onClick={() => {
                navigator.clipboard.writeText(problemContent)
              }}>📋 复制全文</button>
              <button className="primary-btn" onClick={() => setShowContent(false)}>关闭</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
