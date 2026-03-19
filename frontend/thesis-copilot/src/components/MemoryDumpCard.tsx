import { Zap } from 'lucide-react'

interface Props {
  value: string
  onChange: (v: string) => void
}

export function MemoryDumpCard({ value, onChange }: Props) {
  return (
    <div
      className="flex-1 rounded-2xl p-5"
      style={{
        backgroundColor: 'var(--card)',
        border: '1px solid var(--border)',
      }}
    >
      <div className="mb-3 flex items-center gap-2">
        <Zap size={16} style={{ color: 'var(--muted-foreground)' }} />
        <span className="ds-label" style={{ color: 'var(--foreground)' }}>
          Memory Dump
        </span>
      </div>
      <textarea
        className="h-28 w-full resize-none bg-transparent p-0 outline-none ds-small"
        style={{ color: 'var(--foreground)' }}
        placeholder="Tell me about your research dream... e.g., 'I want to build a green-energy AI in Zurich.'"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  )
}