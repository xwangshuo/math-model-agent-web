import { useState, useEffect } from 'react'

interface TeamRole {
  name: string
  icon: string
  description: string
  responsibilities: string[]
  required_skills: string[]
}

interface Member {
  name: string
  strengths: string[]
  preference: string
}

interface RoleAllocation {
  member: string
  role: string
  reason: string
  tasks: string[]
}

interface AnalyzeResult {
  roles: RoleAllocation[]
  collaboration_tips: string[]
  risk_warnings: string[]
}

export default function TeamAdvisor() {
  const [roles, setRoles] = useState<TeamRole[]>([])
  const [members, setMembers] = useState<Member[]>([])
  const [memberName, setMemberName] = useState('')
  const [strengthInput, setStrengthInput] = useState('')
  const [preference, setPreference] = useState('')
  const [result, setResult] = useState<AnalyzeResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [editingIdx, setEditingIdx] = useState<number | null>(null)

  useEffect(() => {
    loadRoles()
  }, [])

  const loadRoles = async () => {
    try {
      const res = await fetch('/api/team/roles')
      const data = await res.json()
      setRoles(data.roles || data)
    } catch { /* ignore */ }
  }

  const addMember = () => {
    if (!memberName.trim()) return
    const strengths = strengthInput
      .split(/[,，、]/)
      .map(s => s.trim())
      .filter(Boolean)

    if (editingIdx !== null) {
      setMembers(prev => prev.map((m, i) => i === editingIdx ? {
        name: memberName.trim(),
        strengths,
        preference: preference || '',
      } : m))
      setEditingIdx(null)
    } else {
      setMembers(prev => [...prev, {
        name: memberName.trim(),
        strengths,
        preference: preference || '',
      }])
    }
    setMemberName('')
    setStrengthInput('')
    setPreference('')
  }

  const editMember = (idx: number) => {
    const m = members[idx]
    setMemberName(m.name)
    setStrengthInput(m.strengths.join(', '))
    setPreference(m.preference)
    setEditingIdx(idx)
  }

  const removeMember = (idx: number) => {
    setMembers(prev => prev.filter((_, i) => i !== idx))
    if (editingIdx === idx) {
      setEditingIdx(null)
      setMemberName('')
      setStrengthInput('')
      setPreference('')
    }
  }

  const handleAnalyze = async () => {
    if (members.length === 0) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('/api/team/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ members }),
      })
      if (!res.ok) throw new Error('分析请求失败')
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
        <h2>👥 团队分工建议</h2>
        <p>根据队员背景自动推荐角色分配</p>
      </div>

      <div className="two-col-layout">
        {/* Left Panel: Roles info + Member input */}
        <div className="col-left">
          {/* Predefined roles */}
          <div className="card">
            <h3>📋 预设角色</h3>
            {roles.length === 0 ? (
              <p className="loading-hint">⏳ 加载角色信息...</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {roles.map((role, i) => (
                  <div key={i} style={{
                    padding: 14, borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--card-border)',
                    background: '#f8fafc',
                    display: 'flex', gap: 12, alignItems: 'flex-start',
                  }}>
                    <span style={{ fontSize: 28, flexShrink: 0 }}>{role.icon}</span>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{role.name}</div>
                      <div style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: 6 }}>
                        {role.description}
                      </div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        <strong>职责：</strong> {role.responsibilities?.join(' · ')}
                      </div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        <strong>技能要求：</strong>
                        {role.required_skills?.map((s, j) => (
                          <span key={j} className="tag" style={{ marginLeft: 4 }}>{s}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Member input */}
          <div className="card">
            <h3>👤 添加队员</h3>
            <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
              <input
                className="search-input"
                placeholder="队员姓名"
                value={memberName}
                onChange={e => setMemberName(e.target.value)}
                style={{ flex: 1 }}
              />
              <select
                className="filter-select"
                value={preference}
                onChange={e => setPreference(e.target.value)}
                style={{ maxWidth: 130 }}
              >
                <option value="">偏好角色</option>
                {roles.map(r => (
                  <option key={r.name} value={r.name}>{r.icon} {r.name}</option>
                ))}
              </select>
            </div>
            <input
              className="search-input"
              placeholder="擅长技能（逗号分隔，如：数据分析, Python, 统计检验）"
              value={strengthInput}
              onChange={e => setStrengthInput(e.target.value)}
              style={{ marginBottom: 10 }}
            />
            <div className="btn-row" style={{ marginTop: 0 }}>
              <button
                className="secondary-btn"
                onClick={addMember}
                disabled={!memberName.trim()}
                style={{ marginTop: 0 }}
              >
                {editingIdx !== null ? '✏️ 更新队员' : '➕ 添加队员'}
              </button>
              {editingIdx !== null && (
                <button
                  className="secondary-btn"
                  onClick={() => {
                    setEditingIdx(null)
                    setMemberName('')
                    setStrengthInput('')
                    setPreference('')
                  }}
                  style={{ marginTop: 0, color: 'var(--text-muted)' }}
                >
                  ✕ 取消
                </button>
              )}
            </div>
          </div>

          {/* Member list */}
          {members.length > 0 && (
            <div className="card">
              <h3>📋 已添加队员（{members.length} 人）</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {members.map((m, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', gap: 10,
                    padding: '10px 12px', borderRadius: 'var(--radius-sm)',
                    border: editingIdx === i ? '2px solid var(--primary)' : '1px solid var(--card-border)',
                    background: editingIdx === i ? 'var(--primary-bg)' : 'var(--card-bg)',
                  }}>
                    <div style={{ fontSize: 20 }}>👤</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 13, fontWeight: 600 }}>{m.name}</div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        {m.strengths.map(s => (
                          <span key={s} className="tag" style={{ marginRight: 3 }}>{s}</span>
                        ))}
                        {m.preference && <span style={{ marginLeft: 4 }}>→ {m.preference}</span>}
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: 4 }}>
                      <button
                        className="tb-btn"
                        onClick={() => editMember(i)}
                        style={{ fontSize: 12, padding: '4px 8px' }}
                        title="编辑"
                      >
                        ✏️
                      </button>
                      <button
                        className="tb-btn"
                        onClick={() => removeMember(i)}
                        style={{ fontSize: 12, padding: '4px 8px', color: 'var(--danger)' }}
                        title="删除"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <button
                className="primary-btn"
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading ? '⏳ 分析中...' : '🔍 分析团队'}
              </button>
            </div>
          )}
        </div>

        {/* Right Panel: Results */}
        <div className="col-right">
          {loading && (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              <p style={{ fontSize: 48, marginBottom: 16 }}>⏳</p>
              <p>正在分析团队分工...</p>
            </div>
          )}

          {error && (
            <div className="card" style={{ borderColor: '#fca5a5', background: '#fef2f2' }}>
              <p style={{ color: 'var(--danger)', fontSize: 14 }}>❌ {error}</p>
            </div>
          )}

          {result && !loading && (
            <>
              {/* Role allocation */}
              <div className="card">
                <h3>🎯 角色分配建议</h3>
                {result.roles.map((alloc, i) => (
                  <div key={i} style={{
                    marginBottom: 14, padding: 14, borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--card-border)',
                    background: 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                      <span style={{ fontSize: 20 }}>👤</span>
                      <div>
                        <span style={{ fontWeight: 700, fontSize: 14 }}>{alloc.member}</span>
                        <span style={{
                          marginLeft: 8, fontSize: 11,
                          padding: '2px 8px', borderRadius: 4,
                          background: 'var(--primary-bg)', color: 'var(--primary-dark)',
                          fontWeight: 600,
                        }}>
                          {alloc.role}
                        </span>
                      </div>
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 8, lineHeight: 1.6 }}>
                      <strong>推荐理由：</strong> {alloc.reason}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      <strong>主要任务：</strong>
                      <ul style={{ paddingLeft: 18, margin: '4px 0' }}>
                        {alloc.tasks.map((t, j) => (
                          <li key={j} style={{ fontSize: 12, lineHeight: 1.6 }}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>

              {/* Collaboration tips */}
              {result.collaboration_tips?.length > 0 && (
                <div className="card" style={{ background: 'var(--success-bg)', borderColor: '#bbf7d0' }}>
                  <h3 style={{ color: '#15803d' }}>💡 协作建议</h3>
                  <ul style={{ paddingLeft: 18, margin: 0 }}>
                    {result.collaboration_tips.map((tip, i) => (
                      <li key={i} style={{ fontSize: 13, lineHeight: 1.7, color: '#166534', marginBottom: 4 }}>{tip}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Risk warnings */}
              {result.risk_warnings?.length > 0 && (
                <div className="card" style={{ background: '#fef2f2', borderColor: '#fca5a5' }}>
                  <h3 style={{ color: 'var(--danger)' }}>⚠️ 风险提示</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {result.risk_warnings.map((warn, i) => (
                      <div key={i} style={{
                        padding: '10px 12px', borderRadius: 'var(--radius-sm)',
                        background: '#fff', border: '1px solid #fecaca',
                        fontSize: 13, color: '#991b1b', lineHeight: 1.6,
                      }}>
                        ⚠️ {warn}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {!result && !loading && !error && (
            <div className="card hint-card" style={{ padding: '80px 20px', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: 14, lineHeight: 2 }}>
                👈 添加队员后点击"分析团队"<br />
                <span style={{ fontSize: 12 }}>
                  系统将根据每位队员的技能和偏好<br />
                  自动推荐最优团队分工
                </span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
