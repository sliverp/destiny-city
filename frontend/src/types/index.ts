export interface Question {
  id: number
  order_num: number
  category: string
  content: string
  options: QuestionOption[]
}

export interface QuestionOption {
  id: string
  content: string
  weights: number[]
}

export interface City {
  id: number
  name: string
  country: string
  description: string
  element: string
  zodiac: string
  tarot: string
  energy_type: string
  wuxing: string
  vibe: string
}

export interface DimensionItem {
  dimension: string
  label: string
  icon: string
  value: number
  desc: string
}

export interface ElementAnalysis {
  element: string
  title: string
  core: string
  strengths: string
  shadow: string
  city_connection: string
}

export interface ZodiacAnalysis {
  zodiac: string
  ruling_planet: string
  quality: string
  keyword: string
  analysis: string
}

export interface TarotReading {
  card: string
  number: string
  keyword: string
  upright: string
  analysis: string
}

export interface WuxingAnalysis {
  wuxing: string
  nature: string
  season: string
  direction: string
  personality: string
  city_match: string
}

export interface EnergyReading {
  type: string
  analysis: string
}

export interface CareerAdvice {
  summary: string
  tags: string[]
}

export interface FullReport {
  destiny_summary: string
  element_analysis: ElementAnalysis
  zodiac_analysis: ZodiacAnalysis
  tarot_reading: TarotReading
  wuxing_analysis: WuxingAnalysis
  energy_reading: EnergyReading
  energy_profile: DimensionItem[]
  top_dimensions: DimensionItem[]
  career_advice: CareerAdvice
  city_description: string
}

export interface MatchResult {
  city: City
  score: number
  interpretation: string
  report?: FullReport
  runner_ups: Array<{
    city: City
    score: number
  }>
  share_id: string
}

export interface InviteCode {
  id: number
  code: string
  is_used: boolean
  used_by: string | null
  created_at: string
  used_at: string | null
}
