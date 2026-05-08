import { useState } from 'react'

interface ExplainResult {
  explanation_by_section: { code_snippet: string; math_meaning: string }[]
  parameter_tuning: string
  common_errors: { error: string; cause: string; fix: string }[]
  dependencies: string
}

export default function CodeExplainer() {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [problemContext, setProblemContext] = useState('')
  const [result, setResult] = useState<ExplainResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState<'sections' | 'tuning' | 'errors'>('sections')

  const handleAnalyze = async () => {
    if (!code.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('/api/code/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language, problem_context: problemContext }),
      })
      if (!res.ok) throw new Error('API 请求失败')
      const data = await res.json()
      setResult(data)
    } catch (e: any) {
      setError(e.message || '分析失败，请检查后端服务')
    }
    setLoading(false)
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>💻 代码解释与调试助手</h2>
        <p>分析代码的数学含义、参数调优建议、常见错误处理</p>
      </div>

      <div className="two-col-layout">
        {/* 左栏：代码输入 */}
        <div className="col-left">
          <div className="card">
            <h3>📝 代码输入</h3>
            <label>编程语言</label>
            <select
              className="filter-select"
              value={language}
              onChange={e => setLanguage(e.target.value)}
              style={{ width: '100%', marginBottom: 12 }}
            >
              <option value="python">Python</option>
              <option value="matlab">MATLAB</option>
              <option value="r">R</option>
            </select>

            <label>粘贴代码</label>
            <textarea
              className="template-textarea"
              placeholder="在此粘贴你的数学建模代码..."
              rows={14}
              value={code}
              onChange={e => setCode(e.target.value)}
              style={{ fontFamily: 'var(--font-mono)', fontSize: 12 }}
            />

            <label>问题上下文（可选）</label>
            <input
              className="search-input"
              placeholder="描述问题背景、目标或遇到的困难..."
              value={problemContext}
              onChange={e => setProblemContext(e.target.value)}
            />

            <button
              className="primary-btn"
              onClick={handleAnalyze}
              disabled={loading || !code.trim()}
            >
              {loading ? '⏳ 分析中...' : '🔍 分析代码'}
            </button>
          </div>
        </div>

        {/* 右栏：结果 */}
        <div className="col-right">
          {loading && (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              <p style={{ fontSize: 48, marginBottom: 16 }}>⏳</p>
              <p>正在分析代码...</p>
            </div>
          )}

          {error && (
            <div className="card" style={{ borderColor: '#fca5a5', background: '#fef2f2' }}>
              <p style={{ color: 'var(--danger)', fontSize: 14 }}>❌ {error}</p>
            </div>
          )}

          {result && !loading && (
            <>
              {/* Tab bar */}
              <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                <div style={{ display: 'flex', borderBottom: '1px solid var(--card-border)' }}>
                  <button
                    style={{
                      flex: 1, padding: '12px 16px', border: 'none', background: activeTab === 'sections' ? 'var(--primary-bg)' : 'transparent',
                      color: activeTab === 'sections' ? 'var(--primary-dark)' : 'var(--text-secondary)',
                      fontWeight: activeTab === 'sections' ? 600 : 400, cursor: 'pointer', fontSize: 13,
                      borderBottom: activeTab === 'sections' ? '2px solid var(--primary)' : '2px solid transparent',
                      transition: 'all 0.2s',
                    }}
                    onClick={() => setActiveTab('sections')}
                  >
                    📖 逐段解释
                  </button>
                  <button
                    style={{
                      flex: 1, padding: '12px 16px', border: 'none', background: activeTab === 'tuning' ? 'var(--primary-bg)' : 'transparent',
                      color: activeTab === 'tuning' ? 'var(--primary-dark)' : 'var(--text-secondary)',
                      fontWeight: activeTab === 'tuning' ? 600 : 400, cursor: 'pointer', fontSize: 13,
                      borderBottom: activeTab === 'tuning' ? '2px solid var(--primary)' : '2px solid transparent',
                      transition: 'all 0.2s',
                    }}
                    onClick={() => setActiveTab('tuning')}
                  >
                    🔧 参数调优
                  </button>
                  <button
                    style={{
                      flex: 1, padding: '12px 16px', border: 'none', background: activeTab === 'errors' ? 'var(--primary-bg)' : 'transparent',
                      color: activeTab === 'errors' ? 'var(--primary-dark)' : 'var(--text-secondary)',
                      fontWeight: activeTab === 'errors' ? 600 : 400, cursor: 'pointer', fontSize: 13,
                      borderBottom: activeTab === 'errors' ? '2px solid var(--primary)' : '2px solid transparent',
                      transition: 'all 0.2s',
                    }}
                    onClick={() => setActiveTab('errors')}
                  >
                    ⚠️ 常见错误
                  </button>
                </div>
              </div>

              {/* Tab content */}
              <div className="card" style={{ marginTop: 0 }}>
                {activeTab === 'sections' && (
                  <div>
                    {result.explanation_by_section.length === 0 && (
                      <p className="empty-hint">暂无逐段解释结果</p>
                    )}
                    {result.explanation_by_section.map((item, i) => (
                      <div key={i} style={{ marginBottom: 18, paddingBottom: 18, borderBottom: i < result.explanation_by_section.length - 1 ? '1px solid var(--card-border)' : 'none' }}>
                        <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 8, fontWeight: 600 }}>
                          代码段 {i + 1}
                        </div>
                        <pre className="code-block" style={{ fontSize: 12, margin: '0 0 10px' }}>
                          <code>{item.code_snippet}</code>
                        </pre>
                        <div className="principle-content">
                          <p><strong>📐 数学含义：</strong></p>
                          <p>{item.math_meaning}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'tuning' && (
                  <div>
                    {result.parameter_tuning ? (
                      <div className="principle-content">
                        <p>{result.parameter_tuning}</p>
                      </div>
                    ) : (
                      <p className="empty-hint">暂无参数调优建议</p>
                    )}
                  </div>
                )}

                {activeTab === 'errors' && (
                  <div>
                    {result.common_errors.length === 0 && (
                      <p className="empty-hint">暂无常见错误记录</p>
                    )}
                    {result.common_errors.map((item, i) => (
                      <div key={i} style={{
                        marginBottom: 12, padding: 14, borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--card-border)', background: '#f8fafc',
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                          <span style={{ color: 'var(--danger)', fontWeight: 700 }}>⚠️</span>
                          <span style={{ fontWeight: 600, fontSize: 13 }}>{item.error}</span>
                        </div>
                        <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 6, paddingLeft: 24 }}>
                          <strong>原因：</strong> {item.cause}
                        </div>
                        <div style={{ fontSize: 12, color: '#15803d', paddingLeft: 24 }}>
                          <strong>💡 修复：</strong> {item.fix}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Dependencies */}
              {result.dependencies && (
                <div className="card">
                  <h3>📦 依赖包</h3>
                  <div className="principle-content">
                    <p style={{ fontFamily: 'var(--font-mono)', fontSize: 12, whiteSpace: 'pre-wrap' }}>{result.dependencies}</p>
                  </div>
                </div>
              )}
            </>
          )}

          {!result && !loading && !error && (
            <div className="card hint-card" style={{ padding: '60px 20px' }}>
              <p style={{ textAlign: 'center', color: 'var(--text-muted)', lineHeight: 2 }}>
                👈 在左侧输入代码<br />
                选择语言后点击"分析代码"<br />
                <span style={{ fontSize: 12 }}>支持 Python / MATLAB / R 代码的数学含义分析</span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
