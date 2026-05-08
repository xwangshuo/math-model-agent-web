const API_BASE = '/api'

// ─── 聊天（流式） ──────────────────────────────────

export async function chatStream(
  message: string,
  history: any[],
  model: string,
  filePath: string,
  onEvent: (event: any) => void,
  signal?: AbortSignal
): Promise<void> {
  const res = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history, model, file_path: filePath }),
    signal,
  })

  if (!res.ok) throw new Error(`HTTP ${res.status}`)

  const reader = res.body?.getReader()
  if (!reader) throw new Error('No response body')

  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed || !trimmed.startsWith('data: ')) continue
      try {
        const event = JSON.parse(trimmed.slice(6))
        onEvent(event)
        if (event.type === 'done' || event.type === 'error') return
      } catch { /* skip malformed */ }
    }
  }
}

// ─── 聊天（非流式，兼容） ───────────────────────────

export async function chatSend(message: string, history: any[], mode: string = 'chat') {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history, model: 'deepseek/deepseek-chat-v3.1' }),
  })
  return res.json()
}

// ─── 文件上传 ────────────────────────────────────────

export async function uploadFile(file: File): Promise<{ file_path: string; filename: string; analysis: string }> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(`上传失败: ${res.status}`)
  return res.json()
}

// ─── 会话管理 ────────────────────────────────────────

export async function getSessions(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/sessions`)
  const data = await res.json()
  return data.sessions || []
}

export async function saveSession(messages: any[], model: string, title?: string, sessionId?: string) {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages, model, title: title || '', session_id: sessionId || '' }),
  })
  return res.json()
}

export async function loadSession(sessionId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`)
  if (!res.ok) throw new Error('会话不存在')
  return res.json()
}

export async function deleteSession(sessionId: string) {
  await fetch(`${API_BASE}/sessions/${sessionId}`, { method: 'DELETE' })
}

// ─── 模型列表 ────────────────────────────────────────

export async function getModels(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/models`)
  const data = await res.json()
  return data.models || []
}

// ─── 数据分析（一键 EDA/异常值/缺失值） ─────────────

export async function analyzeData(filePath: string, analysisType: string, method?: string) {
  const res = await fetch(`${API_BASE}/data/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_path: filePath, analysis_type: analysisType, method: method || 'iqr' }),
  })
  if (!res.ok) throw new Error(`分析失败: ${res.status}`)
  return res.json()
}

// ─── 赛题库 ──────────────────────────────────────────

export async function searchProblems(params: {
  keyword?: string; competition?: string; year?: number;
  category?: string; difficulty?: string;
}): Promise<{ problems: any[]; total: number; filters: any }> {
  const q = new URLSearchParams()
  if (params.keyword) q.set('keyword', params.keyword)
  if (params.competition) q.set('competition', params.competition)
  if (params.year) q.set('year', String(params.year))
  if (params.category) q.set('category', params.category)
  if (params.difficulty) q.set('difficulty', params.difficulty)
  const res = await fetch(`${API_BASE}/problem-bank?${q}`)
  return res.json()
}

export async function getProblem(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/problem-bank/${id}`)
  if (!res.ok) throw new Error('赛题不存在')
  return res.json()
}

export async function getProblemContent(id: string): Promise<{ id: string; title: string; content: string }> {
  const res = await fetch(`${API_BASE}/problem-bank/${id}/content`)
  if (!res.ok) throw new Error('原题全文未收录')
  return res.json()
}

// ─── 选题决策 ─────────────────────────────────────────

export async function analyzeSelection(data: {
  problem_ids: string[]; team_strengths: string[];
  preferred_category: string; hours_available: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/topic-selection/analyze`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function getReadingTemplate(problemId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/problem-bank/${problemId}/reading-template`)
  return res.json()
}

export async function generateReadingTemplate(data: { title: string; description: string }): Promise<any> {
  const res = await fetch(`${API_BASE}/topic-selection/reading-template`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function analyzeProblem(title: string, description: string, context: string = '') {
  const res = await fetch(`${API_BASE}/analysis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, context }),
  })
  return res.json()
}

export async function recommendModel(problemType: string, description: string, dataFeatures: string = '') {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem_type: problemType, description, data_features: dataFeatures }),
  })
  return res.json()
}

export async function generateCode(modelName: string, problemDescription: string, dataDescription: string = '') {
  const res = await fetch(`${API_BASE}/code/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model_name: modelName, problem_description: problemDescription, data_description: dataDescription }),
  })
  return res.json()
}

export async function generatePaper(title: string, abstract: string, sections: any[]) {
  const res = await fetch(`${API_BASE}/paper/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, abstract, sections }),
  })
  return res.json()
}

// ─── 模型知识库 ─────────────────────────────────────

export async function listModels(params: {
  keyword?: string; category?: string;
}): Promise<{ models: any[]; total: number; categories: string[] }> {
  const q = new URLSearchParams()
  if (params.keyword) q.set('keyword', params.keyword)
  if (params.category) q.set('category', params.category)
  const res = await fetch(`${API_BASE}/models?${q}`)
  return res.json()
}

export async function getModelDetail(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/models/${id}`)
  if (!res.ok) throw new Error('模型不存在')
  return res.json()
}
