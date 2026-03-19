import { useRef, useState, useCallback } from 'react'
import { Upload } from 'lucide-react'

const aiTextStyle = {
  background: 'linear-gradient(135deg, #7c3aed, #2563eb)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
} as const

const aiGradient = {
  background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 60%, #7c3aed 100%)',
} as const

interface Props {
  onUpload: () => void
  uploaded: boolean
  keywords: string[]
}

export function CVUploadCard({ onUpload, uploaded, keywords }: Props) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragging(false)
      onUpload()
    },
    [onUpload]
  )

  return (
    <div
      className="flex-1 rounded-2xl p-5 transition-all duration-200"
      style={{
        backgroundColor: 'var(--card)',
        border: uploaded
          ? '2px solid #7c3aed'
          : dragging
          ? '2px dashed #7c3aed'
          : '2px dashed var(--border)',
        boxShadow: uploaded ? '0 0 0 4px rgba(124,58,237,0.08)' : 'none',
      }}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >
      <div className="mb-3 flex items-center gap-2">
        <Upload size={16} style={{ color: uploaded ? '#7c3aed' : 'var(--muted-foreground)' }} />
        <span className="ds-label" style={{ color: 'var(--foreground)' }}>
          CV Upload
        </span>
      </div>

      {!uploaded ? (
        <button
          className="flex w-full flex-col items-center gap-2 py-6"
          onClick={() => inputRef.current?.click()}
        >
          <Upload size={24} style={{ color: 'var(--muted-foreground)' }} />
          <span className="ds-small" style={{ color: 'var(--muted-foreground)' }}>
            Drop your CV here or{' '}
            <span style={aiTextStyle} className="font-medium">click to upload</span>
          </span>
          <input
            ref={inputRef}
            type="file"
            className="hidden"
            accept=".pdf,.doc,.docx"
            onChange={onUpload}
          />
        </button>
      ) : (
        <div className="space-y-2">
          <p className="ds-caption" style={{ color: 'var(--muted-foreground)' }}>
            Extracted keywords:
          </p>
          <div className="flex flex-wrap gap-2">
            {keywords.map((kw) => (
              <span
                key={kw}
                className="ds-badge rounded-full px-3 py-1"
                style={{ ...aiGradient, color: '#fff' }}
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}