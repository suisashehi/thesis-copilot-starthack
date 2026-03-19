import { ChevronRight } from 'lucide-react'
import type { Match } from '../types/thesis'
import { MatchScoreBadge } from './ui/MatchScoreBadge'

const aiGradient = {
  background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 60%, #7c3aed 100%)',
} as const

const aiTextStyle = {
  background: 'linear-gradient(135deg, #7c3aed, #2563eb)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
} as const

interface Props {
  match: Match
  active: boolean
  onClick: () => void
}

export function MatchCard({ match, active, onClick }: Props) {
  return (
    <button
      className="group flex w-full items-center gap-4 rounded-2xl p-4 text-left transition-all duration-200"
      style={{
        backgroundColor: active ? 'var(--accent)' : 'var(--card)',
        border: active ? '1px solid rgba(124,58,237,0.2)' : '1px solid var(--border)',
        boxShadow: active ? '0 4px 24px rgba(124,58,237,0.10)' : 'none',
      }}
      onClick={onClick}
    >
      {/* Company avatar */}
      <div
        className="flex size-11 shrink-0 items-center justify-center rounded-xl ds-title-sm font-semibold"
        style={{ ...aiGradient, color: '#fff' }}
      >
        {match.companyInitial}
      </div>

      {/* Content */}
      <div className="min-w-0 flex-1">
        <p className="ds-title-cards truncate" style={{ color: 'var(--foreground)' }}>
          {match.title}
        </p>
        <p className="ds-caption mt-0.5" style={{ color: 'var(--muted-foreground)' }}>
          {match.company}
        </p>
        <p className="ds-caption mt-1" style={aiTextStyle}>
          {match.matchReason}
        </p>
      </div>

      {/* Score + chevron */}
      <div className="flex shrink-0 flex-col items-end gap-2">
        <MatchScoreBadge score={match.score} />
        <ChevronRight
          size={14}
          className="transition-transform duration-150 group-hover:translate-x-0.5"
          style={{ color: 'var(--muted-foreground)' }}
        />
      </div>
    </button>
  )
}