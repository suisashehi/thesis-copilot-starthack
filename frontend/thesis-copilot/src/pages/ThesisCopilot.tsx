import { useState } from 'react'
import { Sparkles } from 'lucide-react'
import type { Match } from '../types/thesis'
import { MOCK_MATCHES } from '../data/mockMatches'
import { Sidebar } from '../components/Sidebar'
import { CVUploadCard } from '../components/CVUploadCard'
import { MemoryDumpCard } from '../components/MemoryDumpCard'
import { MatchCard } from '../components/MatchCard'
import { ActionDrawer } from '../components/ActionDrawer'

const aiGradient = {
  background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 60%, #7c3aed 100%)',
} as const

const CV_KEYWORDS = ['Python', 'Machine Learning', 'Data Science']

export function ThesisCopilot() {
  const [cvUploaded, setCvUploaded] = useState(false)
  const [memoryText, setMemoryText] = useState('')
  const [matches, setMatches] = useState<Match[]>([])
  const [loading, setLoading] = useState(false)
  const [activeMatch, setActiveMatch] = useState<Match | null>(null)

  const readyToSearch = cvUploaded || memoryText.trim().length > 5

  function handleCvUpload() {
    setCvUploaded(true)
  }

  function handleFindMatches() {
    if (!readyToSearch) return
    setLoading(true)
    setMatches([])
    setActiveMatch(null)
    setTimeout(() => {
      setMatches(MOCK_MATCHES)
      setLoading(false)
    }, 1400)
  }

  function handleMatchClick(match: Match) {
    setActiveMatch(activeMatch?.id === match.id ? null : match)
  }

  return (
    <div
      className="flex h-screen overflow-hidden"
      style={{ backgroundColor: 'var(--background)' }}
    >
      <Sidebar profileSynced={cvUploaded} />

      <main className="flex flex-1 flex-col overflow-y-auto">
        <div className="mx-auto w-full max-w-3xl px-8 py-8">

          {/* Title */}
          <h1 className="ds-title-lg mb-1" style={{ color: 'var(--foreground)' }}>
            Thesis Copilot
          </h1>
          <p className="ds-small mb-8" style={{ color: 'var(--muted-foreground)' }}>
            Drop your CV, describe your dream — get your perfect thesis match in seconds.
          </p>

          {/* Intake Zone */}
          <div className="mb-5 flex gap-4">
            <CVUploadCard
              onUpload={handleCvUpload}
              uploaded={cvUploaded}
              keywords={CV_KEYWORDS}
            />
            <MemoryDumpCard value={memoryText} onChange={setMemoryText} />
          </div>

          {/* CTA */}
          <button
            className="flex w-full items-center justify-center gap-2 rounded-2xl py-3.5 ds-label transition-opacity duration-150 hover:opacity-90 active:opacity-80 disabled:opacity-40"
            style={{ ...aiGradient, color: '#fff' }}
            onClick={handleFindMatches}
            disabled={!readyToSearch || loading}
          >
            <Sparkles size={16} />
            {loading ? 'Finding your matches…' : 'Find My Top Matches'}
          </button>

          {/* Matchmaker Zone */}
          {(matches.length > 0 || loading) && (
            <div className="mt-10">
              <h2 className="ds-title-sm mb-4" style={{ color: 'var(--foreground)' }}>
                Deine Top 3 Matchings
              </h2>

              {loading ? (
                <div className="space-y-3">
                  {[1, 2, 3].map((n) => (
                    <div
                      key={n}
                      className="h-20 animate-pulse rounded-2xl"
                      style={{ backgroundColor: 'var(--secondary)' }}
                    />
                  ))}
                </div>
              ) : (
                <div className="space-y-3">
                  {matches.map((m) => (
                    <MatchCard
                      key={m.id}
                      match={m}
                      active={activeMatch?.id === m.id}
                      onClick={() => handleMatchClick(m)}
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Action Drawer */}
      {activeMatch && (
        <ActionDrawer
          match={activeMatch}
          onClose={() => setActiveMatch(null)}
        />
      )}
    </div>
  )
}