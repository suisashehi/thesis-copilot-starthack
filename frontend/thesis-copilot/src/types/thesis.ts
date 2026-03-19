export interface Match {
  id: string
  title: string
  company: string
  companyInitial: string
  score: number
  tags: string[]
  matchReason: string
  summary: string
  contact: string
}

export interface CVData {
  uploaded: boolean
  keywords: string[]
}