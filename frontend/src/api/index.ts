import axios from 'axios'
import type { Question, MatchResult, InviteCode } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export async function verifyInviteCode(code: string): Promise<{ valid: boolean; token: string; message: string }> {
  const { data } = await api.post('/invite/verify', { code })
  return data
}

export async function getQuestions(token: string): Promise<Question[]> {
  const { data } = await api.get('/questions', {
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
