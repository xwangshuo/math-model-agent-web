import { useState, useEffect } from 'react'

interface Paper {
  id: string
  year: number
  competition: string
  problem: string
  award: string
  team: string
  abstract: string
  highlights: string[]
  chart_quality: string
  code_quality: string
  source?: { source_label: string; source_url: string; paper_note: string }
}

interface PaperFull extends Paper {
  structure: { organization: string; writing_style: string; model_connection: string; key_figures: string[] }
  innovation: string[]
  scoring_analysis: Record<string, string>
  key_lessons: string[]
}

export default function ExcellentPapers() {
  const [papers, setPapers] = useState<Paper[]>([])
  const [filters, setFilters] = useState<any>({})
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [detail, setDetail] = useState<PaperFull | null>(null)
  const [loading, setLoading] = useState(false)
  const [compFilter, setCompFilter] = useState('')
  const [yearFilter, setYearFilter] = useState(0)
  const [searchKw, setSearchKw] = useState('')

  useEffect(() => {
    loadPapers()
  }, [compFilter, yearFilter])

  const loadPapers = async () => {
    const q = new URLSearchParams()
    if (searchKw) q.set('keyword', searchKw)
    if (compFilter) q.set('competition', compFilter)
    if (yearFilter) q.set('year', String(yearFilter))
    const res = await fetch(`/api/papers?${q}`)
    const data = await res.json()
    setPapers(data.papers)
    setFilters(data.filters)
  }

  const handleSelect = async (id: string) => {
    setSelectedId(id)
    setLoading(true)
    const res = await fetch(`/api/papers/${id}`)
    const data = await res.json()
    setDetail(data)
    setLoading(false)
  }

  const awardColor = (award: string) => {
    if (award.includes('O奖') || award.includes('特等奖')) return { bg: '#fef3c7', color: '#b45309' }
    if (award.includes('一等')) return { bg: '#dcfce7', color: '#15803d' }
    return { bg: '#f1f3f5', color: '#555' }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>🏆 优秀论文库</h2>
        <p>历年国赛一等奖 / 美赛 O 奖论文结构分析与学习指南</p>
      </div>

      <div className="knowledge-layout">
        {/* 左栏 */}
        <div className="col-left">
          <div className="card filters-bar">
            <div className="filter-row">
              <input className="search-input" placeholder="🔍 搜索题目/学校..." value={searchKw}
                onChange={e => { setSearchKw(e.target.value); setTimeout(loadPapers, 300) }} />
              <select className="filter-select" value={compFilter} onChange={e => setCompFilter(e.target.value)}>
                <option value="">全部竞赛</option>
                {(filters.competitions || []).map((c: string) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <select className="filter-select short" value={yearFilter} onChange={e => setYearFilter(Number(e.target.value))}>
                <option value={0}>全部年份</option>
                {(filters.years || []).map((y: number) => (
                  <option key={y} value={y}>{y}年</option>
                ))}
              </select>
            </div>
            <div className="result-count">共 {papers.length} 篇</div>
          </div>

          <div className="problem-list" style={{ gap: 12 }}>
            {papers.map(p => {
              const ac = awardColor(p.award)
              return (
                <div key={p.id}
                  className={`problem-card ${selectedId === p.id ? 'selected' : ''}`}
                  onClick={() => handleSelect(p.id)}
                  style={{ padding: 18 }}>
                  <div className="problem-card-header">
                    <span className="prob-badge">{p.competition} {p.year}</span>
                    <span style={{
                      fontSize: 11, padding: '2px 8px', borderRadius: 4,
                      background: ac.bg, color: ac.color, fontWeight: 700
                    }}>{p.award}</span>
                    <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{p.team}</span>
                  </div>
                  <div className="prob-title">{p.problem}</div>
                  <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5, marginTop: 4,
                    display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {p.abstract}
                  </p>
                  <div className="prob-tags" style={{ marginTop: 8 }}>
                    {p.highlights.slice(0, 2).map((h, i) => (
                      <span key={i} className="tag">✦ {h.slice(0, 20)}..</span>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* 右栏 */}
        <div className="col-right">
          {!detail && !loading && (
            <div className="card hint-card" style={{ padding: '60px 20px' }}>
              <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                👈 选择一篇获奖论文查看分析
              </p>
            </div>
          )}

          {loading && <div className="card"><p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: 20 }}>⏳ 加载中...</p></div>}

          {detail && !loading && (
            <div className="model-detail-card">
              <div className="detail-header">
                <h3>{detail.problem}</h3>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 6 }}>
                  <span className="prob-badge">{detail.competition} {detail.year}</span>
                  <span style={{
                    fontSize: 11, padding: '2px 8px', borderRadius: 4,
                    background: awardColor(detail.award).bg, color: awardColor(detail.award).color, fontWeight: 700
                  }}>{detail.award}</span>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>🏫 {detail.team}</span>
                </div>
              </div>

              {detail.source && (
                <div className="source-link-bar">
                  <a href={detail.source.source_url} target="_blank" rel="noopener noreferrer">
                    🔗 {detail.source.source_label}
                  </a>
                  <span className="source-note">{detail.source.paper_note}</span>
                  <button className="view-problem-btn" onClick={() => {
                    // Map paper problem to problem bank ID
                    const idMap: Record<string, string> = {
                      'cumcm-2023-a-01': 'cumcm-2023-a',
                      'cumcm-2023-c-01': 'cumcm-2023-c',
                      'cumcm-2022-c-01': 'cumcm-2022-c',
                      'cumcm-2022-a-01': 'cumcm-2022-a',
                      'cumcm-2021-a-01': 'cumcm-2021-a',
                      'mcm-2024-b-01': 'mcm-2024-b',
                      'mcm-2023-c-01': 'mcm-2023-c',
                    }
                    const probId = idMap[detail.id]
                    if (probId) window.open(`/api/problem-bank/${probId}/content`, '_blank')
                  }}>📄 查看原题全文</button>
                </div>
              )}

              {/* 评分 */}
              <div className="detail-section">
                <h4>📊 评委视角评分</h4>
                <div className="score-grid">
                  {Object.entries(detail.scoring_analysis).map(([k, v]) => {
                    const num = parseInt(v.split('/')[0]) || 7
                    return (
                      <div key={k} className="score-item">
                        <span className="score-label">{k}</span>
                        <div className="score-bar-bg">
                          <div className="score-bar-fill" style={{ width: `${num * 10}%` }} />
                        </div>
                        <span className="score-val">{v}</span>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* 摘要 */}
              <div className="detail-section">
                <h4>📝 论文摘要</h4>
                <div className="principle-content">
                  <p style={{ lineHeight: 1.8, fontSize: 13 }}>{detail.abstract}</p>
                </div>
              </div>

              {/* 亮点 */}
              <div className="detail-section">
                <h4>💡 建模亮点</h4>
                <ul style={{ paddingLeft: 20 }}>
                  {detail.highlights.map((h, i) => (
                    <li key={i} style={{ fontSize: 13, lineHeight: 1.7, marginBottom: 6, color: 'var(--text-secondary)' }}>{h}</li>
                  ))}
                </ul>
              </div>

              {/* 论文结构 */}
              <div className="detail-section">
                <h4>📋 论文结构拆解</h4>
                <div className="structure-card">
                  <div className="struct-item">
                    <span className="struct-label">组织方式</span>
                    <p>{detail.structure.organization}</p>
                  </div>
                  <div className="struct-item">
                    <span className="struct-label">写作风格</span>
                    <p>{detail.structure.writing_style}</p>
                  </div>
                  <div className="struct-item">
                    <span className="struct-label">模型衔接</span>
                    <p>{detail.structure.model_connection}</p>
                  </div>
                  <div className="struct-item">
                    <span className="struct-label">关键图表</span>
                    <ul style={{ paddingLeft: 18, margin: '6px 0' }}>
                      {detail.structure.key_figures.map((f, i) => (
                        <li key={i} style={{ fontSize: 12, lineHeight: 1.6, color: 'var(--text-secondary)' }}>{f}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* 创新点 */}
              <div className="pros-cons" style={{ marginBottom: 16 }}>
                <div className="pros-section">
                  <h4>🚀 创新点</h4>
                  <ul>
                    {detail.innovation.map((inn, i) => (
                      <li key={i}>{inn}</li>
                    ))}
                  </ul>
                </div>
                <div style={{ padding: 14 }}>
                  <h4 style={{ fontSize: 13, marginBottom: 8 }}>🖼️ 图表质量</h4>
                  <div style={{ fontSize: 20, marginBottom: 8 }}>{detail.chart_quality}</div>
                  <h4 style={{ fontSize: 13, marginBottom: 8 }}>💻 代码质量</h4>
                  <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{detail.code_quality}</p>
                </div>
              </div>

              {/* 经验教训 */}
              <div className="detail-section">
                <h4>🎓 这篇论文教你的</h4>
                <div className="lessons-list">
                  {detail.key_lessons.map((l, i) => (
                    <div key={i} className="lesson-item">
                      <span className="lesson-num">{i + 1}</span>
                      <p>{l}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
