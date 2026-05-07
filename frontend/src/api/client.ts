const API_BASE = '/api'

export async function chatSend(message: string, history: any[], mode: string = 'chat') {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history, mode }),
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
