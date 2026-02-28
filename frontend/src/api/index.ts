import axios from 'axios'
import type { Question, MatchResult, InviteCode } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export async function verifyInviteCode(code: string): Promise<{ valid: boolean; token: string; message: string; share_id: string }> {
  const { data } = await api.post('/invite/verify', { code })
  return data
}

export async function getQuestions(token: string, beliefSystem: string = 'all'): Promise<Question[]> {
  const { data } = await api.get('/questions', {
    params: { belief_system: beliefSystem },
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

export async function submitAnswers(
  token: string,
  answers: Record<number, string>
): Promise<MatchResult> {
  const { data } = await api.post(
    '/test/submit',
    { answers },
    { headers: { Authorization: `Bearer ${token}` } }
  )
  return data
}

export async function getResult(shareId: string): Promise<MatchResult> {
  const { data } = await api.get(`/result/${shareId}`)
  return data
}

export async function generateInviteCodes(
  adminKey: string,
  count: number
): Promise<{ codes: string[] }> {
  const { data } = await api.post(
    '/admin/invite-codes',
    { count },
    { headers: { 'X-Admin-Key': adminKey } }
  )
  return data
}

export async function getInviteCodes(
  adminKey: string
): Promise<InviteCode[]> {
  const { data } = await api.get('/admin/invite-codes', {
    headers: { 'X-Admin-Key': adminKey },
  })
  return data
}

export async function recordShareVisit(shareId: string): Promise<{
  visitor_count: number
  required: number
  completed: boolean
  reward_code: string | null
  reward_code_used: boolean
}> {
  const { data } = await api.post(`/share/${shareId}/visit`)
  return data
}

export async function getShareProgress(shareId: string): Promise<{
  visitor_count: number
  required: number
  completed: boolean
  reward_code: string | null
  reward_code_used: boolean
}> {
  const { data } = await api.get(`/share/${shareId}/progress`)
  return data
}

export async function saveTestProgress(
  token: string,
  answers: Record<number, string>,
  currentIndex: number,
  cityScope: string,
  beliefSystem: string,
): Promise<void> {
  await api.post(
    '/test/progress',
    { answers, current_index: currentIndex, city_scope: cityScope, belief_system: beliefSystem },
    { headers: { Authorization: `Bearer ${token}` } }
  )
}

export async function getTestProgress(token: string): Promise<{
  answers: Record<number, string>
  current_index: number
  city_scope: string
  belief_system: string
}> {
  const { data } = await api.get('/test/progress', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return data
}

export interface ShowcaseItem {
  share_id: string
  city_name: string
  country: string
  score: number
  element: string
  zodiac: string
  tarot: string
  energy_type: string
  wuxing: string
  vibe: string
}

export async function getRandomShowcase(): Promise<{ items: ShowcaseItem[] }> {
  const { data } = await api.get('/result/showcase/random')
  return data
}
