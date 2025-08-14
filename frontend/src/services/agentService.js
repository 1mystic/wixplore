import api from './api'
export const runAgents = async (payload) => {
  const res = await api.post('/agents/run', payload)
  return res.data
}
