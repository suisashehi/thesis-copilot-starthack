import { useState, useEffect } from 'react'
import { X, Building2, Sparkles } from 'lucide-react'
import type { Match } from '../types/thesis'
import { MatchScoreBadge } from './ui/MatchScoreBadge'
import { useTypewriter } from '../hooks/useTypewriter'

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
  onClose: () => void
}

export function ActionDrawer({ match, onClose }: Props) {
  const [generating, setGenerating] = useState(false)
  const [draftText, setDraftText] = useState('')

  const proposalBody = `Subject: Application for "${match.title}" — Thesis Collaboration

Dear ${match.contact.split('·')[0].trim()},

My name is Virvi, and I am currently pursuing my studies with a specialisation in Machine Learning and Data Engineering. Having come across your project "${match.title}" at ${match.company}, I am writing to express my strong interest in contributing to this initiative.

${match.matchReason}. The intersection of ${match.tags.join(', ')} aligns precisely with the research direction I wish to pursue in my thesis.

I would be delighted to arrange a brief call to discuss how my background could serve the project's goals.

Kind regards,
Virvi`

  const { displayed } = useTypewriter(generating ? proposalBody : '', 12)

  useEffect(() => {
    if (generating && displayed === proposalBody) {
      setTimeout(() => {
        setDraftText(proposalBody)
        setGenerating(false)
      }, 0)
    }
  }, [displayed, generating, proposalBody])

  function handleGenerate() {
    setDraftText('')
    setGenerating(true)
  }

  return (
    <aside
      className="flex h-screen flex-col border-l"
      style={{
        width: 400,
        minWidth: 400,
        borderColor: 'var(--border)',
        backgroundColor: 'var(--card)',
      }}
    >
      {/* Header */}
      <div
        className="flex items-center gap-3 border-b px-5 py-4"
        style={{ borderColor: 'var(--border)' }}
      >
        <div
          className="flex size-10 shrink-0 items-center justify-center rounded-xl ds-title-sm font-semibold"
          style={{ ...aiGradient, color: '#fff' }}
        >
          {match.companyInitial}
        </div>
        <div className="min-w-0 flex-1">
          <p className="ds-label truncate" style={{ color: 'var(--foreground)' }}>
            {match.title}
          </p>
          <div className="flex items-center gap-1.5">
            <Building2 size={11} style={{ color: 'var(--muted-foreground)' }} />
            <p className="ds-caption" style={{ color: 'var(--muted-foreground)' }}>
              {match.company}
            </p>
          </div>
        </div>
        <button
          className="rounded-lg p-1.5 transition-colors duration-150"
          style={{ color: 'var(--muted-foreground)' }}
          onClick={onClose}
        >
          <X size={16} />
        </button>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto px-5 py-4">
        <div className="mb-4 flex items-center gap-2">
          <MatchScoreBadge score={match.score} />
          <span className="ds-caption" style={{ color: 'var(--muted-foreground)' }}>
            {match.matchReason}
          </span>
        </div>

        <div className="mb-4 flex flex-wrap gap-2">
          {match.tags.map((t) => (
            <span
              key={t}
              className="ds-caption rounded-full px-3 py-1"
              style={{
                backgroundColor: 'var(--secondary)',
                color: 'var(--muted-foreground)',
                border: '1px solid var(--border)',
              }}
            >
              {t}
            </span>
          ))}
        </div>

        <p className="ds-small leading-relaxed" style={{ color: 'var(--muted-foreground)' }}>
          {match.summary}
        </p>

        <p className="ds-caption mt-3" style={{ color: 'var(--muted-foreground)' }}>
          Contact:{' '}
          <span style={aiTextStyle}>{match.contact}</span>
        </p>
      </div>

      {/* Draft Creator */}
      <div
        className="border-t px-5 pb-5 pt-4"
        style={{ borderColor: 'var(--border)' }}
      >
        <p className="ds-label mb-3" style={{ color: 'var(--foreground)' }}>
          Draft Creator
        </p>

        {(generating || draftText) && (
          <textarea
            className="mb-3 h-52 w-full resize-none rounded-xl p-3 ds-caption leading-relaxed outline-none"
            style={{
              backgroundColor: 'var(--secondary)',
              color: 'var(--foreground)',
              border: '1px solid var(--border)',
              fontFamily: '"Courier New", monospace',
            }}
            value={generating ? displayed : draftText}
            onChange={(e) => setDraftText(e.target.value)}
            readOnly={generating}
          />
        )}

        <button
          className="flex w-full items-center justify-center gap-2 rounded-xl py-3 ds-label transition-opacity duration-150 hover:opacity-90 active:opacity-80"
          style={{ ...aiGradient, color: '#fff' }}
          onClick={handleGenerate}
          disabled={generating}
        >
          <Sparkles size={15} />
          {generating ? 'Generating…' : draftText ? 'Regenerate Proposal' : 'Generate AI Proposal'}
        </button>
      </div>
    </aside>
  )
}