import { useState, useEffect, useRef } from 'react'

interface Problem {
  id: string
  label: string
  title: string
  competition: string
  year: number
  difficulty: string
  category: string
  description: string
  models: string[]
}

interface Phase {
  id: string
  name: string
  description: string
  tasks: string[]
}

interface SimulationSession {
  id: string
  problem_ids: string[]
  hours: number
  start_time: string
  end_time: string
  current_phase: string
  status: string
}

interface SubmitResult {
  feedback: string
}

export default function Simulation() {
  const [step, setStep] = useState<'setup' | 'progress'>('setup')
  const [problems, setProblems] = useState<Problem[]>([])
  const [selectedIds, setSelectedIds] = useState<string[]>([])
  const [hours, setHours] = useState(72)
  const [session, setSession] = useState<SimulationSession | null>(null)
  const [phases, setPhases] = useState<Phase[]>([])
  const [currentPhaseIdx, setCurrentPhaseIdx] = useState(0)
  const [phaseTasks, setPhaseTasks] = useState<Record<string, boolean>>({})
  const [phaseContent, setPhaseContent] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [loadingProblems, setLoadingProblems] = useState(false)
  const [startingSim, setStartingSim] = useState(false)
  const [countdown, setCountdown] = useState('')
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    loadProblems()
    loadPhases()
    return () => { if (timerRef.current) clearInterval(timerRef.current) }
  }, [])

  const loadProblems = async () => {
    setLoadingProblems(true)
    try {
      const res = await fetch('/api/problem-bank')
      const data = await res.json()
      setProblems(data.problems || data)
    } catch { /* ignore */ }
    setLoadingProblems(false)
  }

  const loadPhases = async () => {
    try {
      const res = await fetch('/api/simulation/phases')
      const data = await res.json()
      setPhases(data.phases || data)
    } catch { /* ignore */ }
  }

  const toggleProblem = (id: string) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

  const startSimulation = async () => {
    if (selectedIds.length === 0) return
    setStartingSim(true)
    try {
      const res = await fetch('/api/simulation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem_ids: selectedIds, hours }),
      })
      const data = await res.json()
      setSession(data)
      setStep('progress')
      setCurrentPhaseIdx(0)
      setPhaseTasks({})
      setPhaseContent('')
      setFeedback('')
      startCountdown(data.end_time)
    } catch { /* ignore */ }
    setStartingSim(false)
  }

  const startCountdown = (endTime: string) => {
    if (timerRef.current) clearInterval(timerRef.current)
    const end = new Date(endTime).getTime()
    timerRef.current = setInterval(() => {
      const now = Date.now()
      const diff = end - now
      if (diff <= 0) {
        setCountdown('00:00:00')
        if (timerRef.current) clearInterval(timerRef.current)
        return
      }
      const h = Math.floor(diff / 3600000)
      const m = Math.floor((diff % 3600000) / 60000)
      const s = Math.floor((diff % 60000) / 1000)
      setCountdown(`${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`)
    }, 1000)
  }

  const toggleTask = (task: string) => {
    setPhaseTasks(prev => ({ ...prev, [task]: !prev[task] }))
  }

  const handleSubmit = async () => {
    if (!session || !phaseContent.trim()) return
    setSubmitting(true)
    setFeedback('')
    const phaseId = phases[currentPhaseIdx]?.id || `phase-${currentPhaseIdx + 1}`
    try {
      const res = await fetch(`/api/simulation/${session.id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phase: phaseId, content: phaseContent }),
      })
      const data: SubmitResult = await res.json()
      setFeedback(data.feedback)
    } catch {
      setFeedback('❌ 提交失败，请检查后端服务')
    }
    setSubmitting(false)
  }

  const currentPhase = phases[currentPhaseIdx]

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>🏋️ 实战训练（模拟竞赛）</h2>
        <p>72小时模拟竞赛 — 随机抽题、分阶段提醒、AI 点评</p>
      </div>

      {/* Step 1: Setup */}
      {step === 'setup' && (
        <div className="two-col-layout">
          <div className="col-left">
            <div className="card">
              <h3>📋 选择赛题</h3>
              {loadingProblems ? (
                <p className="loading-hint">⏳ 加载赛题...</p>
              ) : (
                <div className="problem-list">
                  {problems.length === 0 && <p className="empty-hint">暂无可用赛题</p>}
                  {problems.map(p => (
                    <div
                      key={p.id}
                      className={`problem-card ${selectedIds.includes(p.id) ? 'selected' : ''}`}
                      onClick={() => toggleProblem(p.id)}
                    >
                      <div className="problem-card-header">
                        <span className="prob-badge">{p.competition} {p.year}</span>
                        <span className={`diff-badge diff-${p.difficulty?.toLowerCase()}`}>{p.difficulty}</span>
                        <span className="prob-category">{p.category}</span>
                      </div>
                      <div className="prob-title">{p.label} · {p.title}</div>
                      <div className="prob-desc">{p.description}</div>
                      <div className="prob-models">{p.models?.slice(0, 3).join(' · ')}</div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 8 }}>
                        <input
                          type="checkbox"
                          checked={selectedIds.includes(p.id)}
                          onChange={() => toggleProblem(p.id)}
                          style={{ accentColor: 'var(--primary)' }}
                        />
                        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                          {selectedIds.includes(p.id) ? '已选' : '选择此赛题'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="col-right">
            <div className="card">
              <h3>⚙️ 模拟设置</h3>

              <label>可用时间（小时）</label>
              <input
                type="range"
                min={24}
                max={120}
                step={6}
                value={hours}
                onChange={e => setHours(Number(e.target.value))}
              />
              <span className="range-label">{hours} 小时</span>

              <div style={{ marginTop: 16, padding: 12, background: 'var(--primary-bg)', borderRadius: 'var(--radius-sm)' }}>
                <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  <strong>模拟流程：</strong><br />
                  Day 1 — 选题分析（理解问题、查阅资料）<br />
                  Day 2 — 建模求解（构建模型、求解验证）<br />
                  Day 3 — 论文写作（撰写论文、修改完善）
                </p>
              </div>

              <button
                className="primary-btn"
                onClick={startSimulation}
                disabled={startingSim || selectedIds.length === 0}
              >
                {startingSim
                  ? '⏳ 创建模拟...'
                  : `🚀 开始模拟（${selectedIds.length} 题）`
                }
              </button>
            </div>

            {!startingSim && selectedIds.length === 0 && (
              <div className="card hint-card" style={{ padding: '40px 20px' }}>
                <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                  👈 选择至少一道赛题开始模拟
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Step 2: In Progress */}
      {step === 'progress' && (
        <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          {/* Progress bar + countdown */}
          <div className="card" style={{ margin: '16px 20px', padding: '14px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16, flex: 1 }}>
              {phases.map((ph, i) => (
                <div key={ph.id} style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1 }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: '50%',
                    background: i < currentPhaseIdx ? 'var(--success)' : i === currentPhaseIdx ? 'var(--primary)' : '#f1f3f5',
                    color: i <= currentPhaseIdx ? '#fff' : 'var(--text-muted)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 12, fontWeight: 700, transition: 'all 0.3s',
                  }}>
                    {i < currentPhaseIdx ? '✓' : i + 1}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 12, fontWeight: 600, color: i === currentPhaseIdx ? 'var(--primary)' : 'var(--text)' }}>{ph.name}</div>
                    <div style={{
                      height: 4, borderRadius: 2,
                      background: i < currentPhaseIdx ? 'var(--success)' : i === currentPhaseIdx ? 'var(--primary)' : '#f1f3f5',
                      marginTop: 2, transition: 'all 0.3s',
                    }} />
                  </div>
                  {i < phases.length - 1 && (
                    <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>→</span>
                  )}
                </div>
              ))}
            </div>
            <div style={{
              textAlign: 'center', padding: '6px 18px', borderRadius: 'var(--radius-sm)',
              background: 'var(--primary-bg)', border: '1px solid #c7d2fe', flexShrink: 0,
            }}>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>剩余时间</div>
              <div style={{ fontSize: 22, fontWeight: 700, color: 'var(--primary-dark)', fontFamily: 'var(--font-mono)' }}>
                {countdown || '--:--:--'}
              </div>
            </div>
          </div>

          {/* Phase tabs */}
          <div className="card" style={{ margin: '0 20px', padding: 0, overflow: 'hidden' }}>
            <div style={{ display: 'flex' }}>
              {phases.map((ph, i) => (
                <button
                  key={ph.id}
                  style={{
                    flex: 1, padding: '12px 16px', border: 'none',
                    background: i === currentPhaseIdx ? 'var(--primary-bg)' : 'transparent',
                    color: i === currentPhaseIdx ? 'var(--primary-dark)' : i < currentPhaseIdx ? 'var(--success)' : 'var(--text-secondary)',
                    fontWeight: i === currentPhaseIdx ? 600 : 400,
                    cursor: 'pointer', fontSize: 13,
                    borderBottom: i === currentPhaseIdx ? '2px solid var(--primary)' : '2px solid transparent',
                    transition: 'all 0.2s',
                  }}
                  onClick={() => {
                    setCurrentPhaseIdx(i)
                    setPhaseContent('')
                    setFeedback('')
                  }}
                >
                  {i < currentPhaseIdx ? '✓ ' : ''}{ph.name}
                </button>
              ))}
            </div>
          </div>

          <div className="two-col-layout" style={{ flex: 1, minHeight: 0 }}>
            {/* Left: Phase info + tasks */}
            <div className="col-left">
              {currentPhase && (
                <>
                  <div className="card">
                    <h3>{currentPhase.name}</h3>
                    <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: 10 }}>
                      {currentPhase.description}
                    </p>
                  </div>

                  <div className="card">
                    <h3>✅ 阶段任务清单</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                      {currentPhase.tasks.map((task, i) => (
                        <label
                          key={i}
                          style={{
                            display: 'flex', alignItems: 'center', gap: 10,
                            padding: '10px 12px', borderRadius: 'var(--radius-sm)',
                            background: phaseTasks[task] ? 'var(--success-bg)' : '#f8fafc',
                            border: `1px solid ${phaseTasks[task] ? '#bbf7d0' : 'var(--card-border)'}`,
                            cursor: 'pointer', transition: 'all 0.2s',
                            fontSize: 13, color: phaseTasks[task] ? '#166534' : 'var(--text)',
                          }}
                        >
                          <input
                            type="checkbox"
                            checked={!!phaseTasks[task]}
                            onChange={() => toggleTask(task)}
                            style={{ accentColor: 'var(--success)' }}
                          />
                          <span style={{ textDecoration: phaseTasks[task] ? 'line-through' : 'none', flex: 1 }}>
                            {task}
                          </span>
                          {phaseTasks[task] && <span style={{ fontSize: 12 }}>✅</span>}
                        </label>
                      ))}
                    </div>
                    <div style={{ marginTop: 10, fontSize: 12, color: 'var(--text-muted)' }}>
                      已完成 {Object.values(phaseTasks).filter(Boolean).length} / {currentPhase.tasks.length} 项
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Right: Submission + Feedback */}
            <div className="col-right">
              <div className="card">
                <h3>📝 提交阶段成果</h3>
                <textarea
                  className="template-textarea"
                  placeholder={`输入${currentPhase?.name || ''}的成果内容...`}
                  rows={10}
                  value={phaseContent}
                  onChange={e => setPhaseContent(e.target.value)}
                />
                <button
                  className="primary-btn"
                  onClick={handleSubmit}
                  disabled={submitting || !phaseContent.trim()}
                >
                  {submitting ? '⏳ 提交中...' : '📤 提交阶段成果'}
                </button>
              </div>

              {feedback && (
                <div className="card" style={{
                  background: feedback.startsWith('❌') ? '#fef2f2' : 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)',
                  borderColor: feedback.startsWith('❌') ? '#fca5a5' : '#c7d2fe',
                }}>
                  <h3 style={{ color: feedback.startsWith('❌') ? 'var(--danger)' : 'var(--primary-dark)' }}>
                    🤖 AI 点评
                  </h3>
                  <div className="principle-content" style={{ fontSize: 13, lineHeight: 1.7 }}>
                    {feedback.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>
              )}

              {!feedback && (
                <div className="card hint-card" style={{ padding: '40px 20px' }}>
                  <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                    提交阶段成果后将获得 AI 点评反馈
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
