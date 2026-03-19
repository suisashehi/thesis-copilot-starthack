const aiGradient = {
  background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 60%, #7c3aed 100%)',
} as const

interface Props {
  score: number
}

export function MatchScoreBadge({ score }: Props) {
  return (
    <span
      className="ds-badge rounded-full px-3 py-1"
      style={{ ...aiGradient, color: '#fff', whiteSpace: 'nowrap' }}
    >
      {score}% Match
    </span>
  )
}