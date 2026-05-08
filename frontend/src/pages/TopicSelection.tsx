import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { searchProblems, analyzeSelection } from '../api/client.ts'

export default function TopicSelection() {
  const [problems, setProblems] = useState<any[]>([])
  const [filters, setFilters] = useState<any>({})
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [strengths, setStrengths] = useState('数据分析, 编程, 数学推导')
  const [prefCategory, setPrefCategory] = useState('')
  const [hours, setHours] = useState(72)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [searchKw, setSearchKw] = useState('')
  const [compFilter, setCompFilter] = useState('')

  useEffect(() => {
    loadProblems()
  }, [searchKw, compFilter])

  const loadProblems = async () => {
    const data = await searchProblems({ keyword: searchKw, competition: compFilter })
    setProblems(data.problems)
    setFilters(data.filters)
  }

  const toggleSelect = (id: string) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

  const handleAnalyze = async () => {
    if (selectedIds.length === 0) return
    setLoading(true)
    try {
      const data = await analyzeSelection({
        problem_ids: selectedIds,
        team_strengths: strengths.split(',').map(s => s.trim()).filter(Boolean),
        preferred_category: prefCategory,
        hours_available: hours,
      })
      setResult(data)
    } catch (e) {
      setResult({ conclusions: '❌ 分析失败，请检查后端服务。' })
    }
    setLoading(false)
  }

  const strengthPresets = [
    { label: '数据分析型', val: '数据分析, 编程, 统计检验, 机器学习' },
    { label: '理论推导型', val: '数学推导, 物理直觉, 数值计算, 公式推导' },
    { label: '编程实现型', val: '算法设计, 编程, 优化求解, 数据处理' },
    { label: '综合型', val: '数据分析, 编程, 数学推导, 算法设计' },
  ]

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>🎯 选题决策</h2>
        <p>从历年赛题中筛选候选题目，根据团队优势智能推荐最佳选题</p>
      </div>

      <div className="two-col-layout">
        {/* 左栏：筛选 + 列表 */}
        <div className="col-left">
          <div className="card">
            <div className="filter-row">
              <input
                className="search-input"
                placeholder="🔍 搜索题目..."
                value={searchKw}
                onChange={e => setSearchKw(e.target.value)}
              />
              <select className="filter-select" value={compFilter} onChange={e => setCompFilter(e.target.value)}>
                <option value="">全部竞赛</option>
                {(filters.competitions || []).map((c: string) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="problem-list">
            {problems.length === 0 && <p className="empty-hint">无匹配赛题</p>}
            {problems.map(p => (
              <div
                key={p.id}
                className={`problem-card ${selectedIds.includes(p.id) ? 'selected' : ''}`}
                onClick={() => toggleSelect(p.id)}
              >
                <div className="problem-card-header">
                  <span className="prob-badge">{p.competition} {p.year}</span>
                  <span className={`diff-badge diff-${p.difficulty.toLowerCase()}`}>{p.difficulty}</span>
                  <span className="prob-category">{p.category}</span>
                </div>
                <div className="prob-title">{p.label} · {p.title}</div>
                <div className="prob-desc">{p.description}</div>
                <div className="prob-models">{p.models.join(' · ')}</div>
                {selectedIds.includes(p.id) && <div className="check-mark">✓ 已选</div>}
              </div>
            ))}
          </div>
        </div>

        {/* 右栏：配置 + 结果 */}
        <div className="col-right">
          <div className="card">
            <h3>⚙️ 团队配置</h3>
            <label>团队优势（逗号分隔）</label>
            <input className="search-input" value={strengths} onChange={e => setStrengths(e.target.value)} />
            <div className="preset-row">
              {strengthPresets.map(sp => (
                <button key={sp.label} className="preset-btn" onClick={() => setStrengths(sp.val)}>
                  {sp.label}
                </button>
              ))}
            </div>

            <label>偏好题目类别</label>
            <select className="filter-select" value={prefCategory} onChange={e => setPrefCategory(e.target.value)}>
              <option value="">不限</option>
              {(filters.categories || []).map((c: string) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            <label>可用时间（小时）</label>
            <input type="range" min={24} max={120} step={12} value={hours}
              onChange={e => setHours(Number(e.target.value))} />
            <span className="range-label">{hours} 小时</span>

            <button
              className="primary-btn"
              onClick={handleAnalyze}
              disabled={loading || selectedIds.length === 0}
            >
              {loading ? '⏳ 分析中...' : `📊 分析 ${selectedIds.length} 道题`}
            </button>
          </div>

          {result && (
            <div className="card result-card">
              <ReactMarkdown>{result.conclusions || ''}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
